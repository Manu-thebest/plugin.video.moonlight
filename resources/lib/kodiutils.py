# -*- coding: utf-8 -*-
"""Utilidades comunes: acceso a ajustes del addon y logging."""
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
