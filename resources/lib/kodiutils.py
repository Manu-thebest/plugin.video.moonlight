# -*- coding: utf-8 -*-
"""Utilidades comunes: acceso a ajustes del addon, logging y ventana de Kodi."""
import os
import subprocess
import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')


def get_setting(setting_id, default=''):
    try:
        value = ADDON.getSettingString(setting_id)
    except Exception:
        value = ADDON.getSetting(setting_id)
    return value if value else default


def get_setting_bool(setting_id):
    try:
        return ADDON.getSettingBool(setting_id)
    except Exception:
        return ADDON.getSetting(setting_id).lower() == 'true'


def get_setting_int(setting_id, default=0):
    try:
        return ADDON.getSettingInt(setting_id)
    except Exception:
        try:
            return int(ADDON.getSetting(setting_id))
        except (ValueError, TypeError):
            return default


def debug_enabled():
    return get_setting_bool('debug_logging')


def log(message, level=xbmc.LOGDEBUG):
    if level == xbmc.LOGDEBUG and not debug_enabled():
        return
    xbmc.log('[%s] %s' % (ADDON_ID, message), level)


def _x11_window_action(action):
    """
    Minimiza o restaura la ventana de Kodi ejecutando x11_window.py con el
    python3 del HOST (via flatpak-spawn cuando Kodi es Flatpak).

    libwnck usa XIconifyWindow (ICCCM), que es lo unico que funciona con
    Marco/MATE: wmctrl -b add,hidden es ignorado por ese gestor de ventanas.
    """
    script = os.path.join(ADDON.getAddonInfo('path'),
                          'resources', 'lib', 'x11_window.py')
    prefix = ['flatpak-spawn', '--host'] if os.environ.get('FLATPAK_ID') else []
    cmd = prefix + ['python3', script, action]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        out = (result.stdout or '').strip()
        if result.returncode == 0:
            log('Ventana Kodi %s: %s' % (action, out), xbmc.LOGINFO)
            return True
        log('Fallo al hacer %s de la ventana: %s %s'
            % (action, out, (result.stderr or '').strip()), xbmc.LOGWARNING)
    except Exception as e:
        log('Error al hacer %s de la ventana: %s' % (action, e), xbmc.LOGWARNING)
    return False


def try_minimize_kodi_window():
    """Minimiza Kodi antes de lanzar Moonlight."""
    if _x11_window_action('minimize'):
        xbmc.sleep(300)
        return True
    # Fallback: builtin de Kodi (en algunos entornos basta)
    xbmc.executebuiltin('Minimize')
    xbmc.sleep(400)
    log('libwnck no disponible; solo se aplico el builtin Minimize de Kodi')
    return False


def try_restore_kodi_window():
    """Desminimiza y activa la ventana de Kodi al terminar Moonlight."""
    if not _x11_window_action('restore'):
        xbmc.executebuiltin('ActivateWindow(home)')