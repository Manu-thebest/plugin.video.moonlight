# -*- coding: utf-8 -*-
"""
Wrapper para invocar Moonlight (Flatpak: com.moonlight_stream.Moonlight) desde
el addon de Kodi.

Referencia de la CLI de moonlight-qt (acciones: list, quit, stream, pair):
https://github.com/moonlight-stream/moonlight-qt/blob/master/app/cli/commandlineparser.cpp
"""
import os
import subprocess
import xbmc
import kodiutils as ku

DEFAULT_FLATPAK_ID = 'com.moonlight_stream.Moonlight'


def _flatpak_app_id():
    return ku.get_setting('moonlight_flatpak_id') or DEFAULT_FLATPAK_ID


def _base_command(extra_flatpak_run_flags=None):
    """
    Construye el prefijo del comando para lanzar Moonlight.

    Si Kodi corre dentro de un sandbox Flatpak (variable de entorno FLATPAK_ID
    presente), un subprocess normal NO puede lanzar otro Flatpak: hay que usar
    'flatpak-spawn --host' para salir del sandbox y ejecutar en el host. Si
    Kodi corre nativo (sin Flatpak), llamamos a 'flatpak run' directamente.

    extra_flatpak_run_flags: flags opcionales para 'flatpak run' (por ejemplo
    ['--env=SDL_AUDIODRIVER=pulse']), insertadas antes del ID de la app.
    """
    app_id = _flatpak_app_id()
    extra = extra_flatpak_run_flags or []
    flatpak_id = os.environ.get('FLATPAK_ID')
    if flatpak_id:
        cmd = ['flatpak-spawn', '--host', 'flatpak', 'run'] + extra + [app_id]
        ku.log('Kodi corre en Flatpak (%s) -> usando flatpak-spawn --host' % flatpak_id)
    else:
        cmd = ['flatpak', 'run'] + extra + [app_id]
        ku.log('Kodi corre nativo -> llamando a flatpak directamente')
    return cmd


def _toggle_arg(name, value):
    return ['-' + name] if value else ['-no-' + name]


def _resolution_args():
    res = ku.get_setting('resolution')
    mapping = {'720p': '-720', '1080p': '-1080', '1440p': '-1440', '4K': '-4K'}
    if res in mapping:
        return [mapping[res]]
    custom = ku.get_setting('custom_resolution') or '1920x1080'
    return ['-resolution', custom]


def list_games(host):
    """Devuelve (ok, [nombres_de_juego]) usando 'moonlight list <host>'."""
    args = _base_command() + ['list', host]
    ku.log('Listando juegos: ' + ' '.join(args))
    try:
        result = subprocess.run(
            args, capture_output=True, text=True,
            timeout=ku.get_setting_int('connect_timeout', 8))
    except subprocess.TimeoutExpired:
        ku.log('Timeout listando juegos en ' + host, xbmc.LOGERROR)
        return False, []
    except FileNotFoundError as e:
        ku.log('No se encontro el comando flatpak/flatpak-spawn: ' + str(e), xbmc.LOGERROR)
        return False, []
    except Exception as e:
        ku.log('Error listando juegos: ' + str(e), xbmc.LOGERROR)
        return False, []

    ku.log('Salida cruda de "list": ' + repr(result.stdout))
    if result.returncode != 0:
        ku.log('moonlight list devolvio codigo %s: %s' % (result.returncode, result.stderr), xbmc.LOGERROR)
        return False, []

    return True, _parse_game_list(result.stdout)


def _parse_game_list(raw_output):
    """
    Interpreta la salida de 'moonlight list <host>' (en principio, un nombre
    de app por linea). Descarta lineas vacias, URLs/enlaces (esa es la causa
    de que antes aparecieran "links raros" en vez de nombres) y mensajes de
    log o conexion que no son nombres de juego.

    Si el formato real sigue sin coincidir, activa el registro de depuracion
    (Ajustes > Avanzado) y mira la linea "Salida cruda de list" en kodi.log
    para ajustar esto con el dato exacto.
    """
    noise_keywords = (
        'error', 'warning', 'connecting', 'searching', 'trying',
        'certificate', 'failed', 'timeout', 'usage:', 'moonlight ',
    )
    games = []
    for raw_line in raw_output.splitlines():
        line = raw_line.strip().strip(',;').strip('"')
        if not line:
            continue
        if '://' in line or line.lower().startswith('www.'):
            continue
        if any(kw in line.lower() for kw in noise_keywords):
            continue
        games.append(line)
    return games


def pair(host, pin):
    """Empareja con el host usando un PIN elegido por el usuario (-pin)."""
    args = _base_command() + ['pair', host, '-pin', str(pin)]
    ku.log('Emparejando: ' + ' '.join(args))
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=35)
    except subprocess.TimeoutExpired:
        return False, 'Tiempo de espera agotado'
    except Exception as e:
        return False, str(e)

    output = (result.stdout or '') + (result.stderr or '')
    ku.log('Salida de pairing: ' + output)
    success = result.returncode == 0 and 'fail' not in output.lower()
    return success, output.strip()


def stream(host, app_name):
    """Lanza el streaming de app_name usando todos los parametros de ajustes."""
    flatpak_flags = []
    audio_driver = ku.get_setting('audio_driver')
    if audio_driver and audio_driver.strip().lower() not in ('automático', 'automatico', 'auto', ''):
        flatpak_flags.append('--env=SDL_AUDIODRIVER=' + audio_driver.strip().lower())

    args = _base_command(flatpak_flags) + ['stream', host, app_name]
    args += _resolution_args()
    args += ['-fps', ku.get_setting('fps') or '60']
    args += ['-bitrate', ku.get_setting('bitrate') or '20000']
    args += ['-video-codec', ku.get_setting('codec') or 'auto']
    args += ['-display-mode', ku.get_setting('display_mode') or 'fullscreen']
    args += ['-audio-config', ku.get_setting('audio_config') or 'stereo']
    args += _toggle_arg('vsync', ku.get_setting_bool('vsync'))
    args += _toggle_arg('hdr', ku.get_setting_bool('hdr'))
    args += _toggle_arg('yuv444', ku.get_setting_bool('yuv444'))
    args += _toggle_arg('game-optimization', ku.get_setting_bool('game_optimization'))
    args += _toggle_arg('audio-on-host', ku.get_setting_bool('audio_on_host'))
    args += _toggle_arg('quit-after', ku.get_setting_bool('quit_after'))
    args += _toggle_arg('keep-awake', ku.get_setting_bool('keep_awake'))

    extra = ku.get_setting('extra_args')
    if extra:
        args += extra.split()

    ku.log('Ejecutando stream: ' + ' '.join(args))
    try:
        result = subprocess.run(args)
        return result.returncode
    except Exception as e:
        ku.log('Error lanzando streaming: ' + str(e), xbmc.LOGERROR)
        return -1


def quit_running(host):
    """Cierra la app/juego en ejecucion en el host (accion 'quit')."""
    args = _base_command() + ['quit', host]
    try:
        subprocess.run(args, capture_output=True, text=True, timeout=15)
        return True
    except Exception as e:
        ku.log('Error al cerrar sesion: ' + str(e), xbmc.LOGERROR)
        return False
