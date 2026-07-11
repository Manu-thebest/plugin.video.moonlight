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


def try_restore_kodi_window():
    """
    Kodi no tiene un builtin oficial para 'restaurar' tras Minimize. Como
    mejor esfuerzo, probamos wmctrl y xdotool (si estan instalados) para
    devolver el foco a la ventana de Kodi. En sesiones Wayland puras, o si
    ninguna de las dos herramientas esta instalada, esto simplemente no hace
    nada (no falla ni bloquea el addon).
    """
    prefix = ['flatpak-spawn', '--host'] if os.environ.get('FLATPAK_ID') else []
    attempts = (
        prefix + ['wmctrl', '-a', 'Kodi'],
        prefix + ['xdotool', 'search', '--name', 'Kodi', 'windowactivate'],
    )
    for cmd in attempts:
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=3)
            if result.returncode == 0:
                log('Ventana de Kodi restaurada con: ' + ' '.join(cmd))
                return True
        except Exception:
            continue
    log('No se pudo restaurar automaticamente la ventana de Kodi '
        '(wmctrl/xdotool no disponibles, o sesion Wayland sin soporte)')
    return False
