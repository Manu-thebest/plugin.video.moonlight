#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moonlight Game Streaming - addon de Kodi.

Lista (solo texto) los juegos disponibles en un host Sunshine y lanza
Moonlight (Flatpak) para hacer streaming del juego elegido, con los
parametros configurados en los ajustes del addon.
"""
import sys
import os
import urllib.parse

ADDON_PATH = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(ADDON_PATH, 'resources', 'lib')
if LIB_PATH not in sys.path:
    sys.path.insert(0, LIB_PATH)

import xbmc
import xbmcgui
import xbmcplugin
import kodiutils as ku
import moonlight
import wol

HANDLE = int(sys.argv[1]) if len(sys.argv) > 1 else -1
BASE_URL = sys.argv[0] if len(sys.argv) > 0 else 'plugin://plugin.video.moonlight/'


def build_url(**kwargs):
    return BASE_URL + '?' + urllib.parse.urlencode(kwargs)


def route_list():
    host = ku.get_setting('host_ip')
    if not host:
        xbmcgui.Dialog().ok('Moonlight', 'Configura primero la IP del host en los ajustes del addon.')
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
        return

    xbmcgui.Dialog().notification('Moonlight', 'Buscando juegos en ' + host + '...',
                                   xbmcgui.NOTIFICATION_INFO, 2000)
    ok, games = moonlight.list_games(host)

    if not ok:
        xbmcgui.Dialog().notification('Moonlight', 'No se pudo conectar con ' + host,
                                       xbmcgui.NOTIFICATION_ERROR, 4000)
        li = xbmcgui.ListItem(label='No se pudo conectar. Pulsa para reintentar.')
        xbmcplugin.addDirectoryItem(HANDLE, build_url(action='list'), li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
        return

    if not games:
        li = xbmcgui.ListItem(label='(Sin juegos encontrados. Pulsa para reintentar.)')
        xbmcplugin.addDirectoryItem(HANDLE, build_url(action='list'), li, isFolder=False)

    addon_icon = ku.ADDON.getAddonInfo('icon')

    for name in games:
        li = xbmcgui.ListItem(label=name)
        li.setArt({'icon': addon_icon, 'thumb': addon_icon})
        li.addContextMenuItems([
            ('Actualizar lista', 'Container.Refresh'),
            ('Ajustes de Moonlight', 'Addon.OpenSettings(%s)' % ku.ADDON_ID),
        ])
        xbmcplugin.addDirectoryItem(HANDLE, build_url(action='stream', game=name), li, isFolder=False)

    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def route_stream(game_name):
    if not game_name:
        return
    host = ku.get_setting('host_ip')
    mute_pref = ku.get_setting_bool('mute_kodi')
    was_muted = xbmc.getCondVisibility('Player.Muted')
    if mute_pref and not was_muted:
        xbmc.executebuiltin('Mute')

    xbmcgui.Dialog().notification('Moonlight', 'Iniciando ' + game_name + '...',
                                   xbmcgui.NOTIFICATION_INFO, 2000)

    xbmc.executebuiltin('Minimize')
    xbmc.sleep(600)

    rc = moonlight.stream(host, game_name)

    ku.try_restore_kodi_window()

    if mute_pref and not was_muted:
        xbmc.executebuiltin('Mute')

    if rc != 0:
        xbmcgui.Dialog().notification(
            'Moonlight',
            'Moonlight termino con un aviso (codigo %s). Activa el log de depuracion si quieres mas detalle.' % rc,
            xbmcgui.NOTIFICATION_WARNING, 5000)


def route_pair():
    host = ku.get_setting('host_ip')
    pin = ku.get_setting('pair_pin') or '1234'
    if not host:
        xbmcgui.Dialog().ok('Moonlight', 'Configura primero la IP del host.')
        return

    proceed = xbmcgui.Dialog().yesno(
        'Emparejar con ' + host,
        'En cuanto pulses "Empezar", ve a https://' + host + ':47990 desde un navegador '
        'e introduce el PIN: ' + pin + '\n\nTienes unos 30 segundos antes de que caduque.',
        yeslabel='Empezar', nolabel='Cancelar')
    if not proceed:
        return

    ok, msg = moonlight.pair(host, pin)
    if ok:
        xbmcgui.Dialog().ok('Emparejamiento completado', 'Emparejado correctamente con ' + host + '.')
    else:
        xbmcgui.Dialog().ok(
            'Emparejamiento fallido',
            'No se pudo emparejar con ' + host + '.\n\nComprueba que introdujiste el PIN ' + pin +
            ' a tiempo en https://' + host + ':47990 y vuelve a intentarlo.\n\nDetalle: ' + msg[:200])


def route_wol():
    mac = ku.get_setting('host_mac')
    if not mac:
        xbmcgui.Dialog().ok('Moonlight', 'Configura primero la MAC del host en los ajustes.')
        return
    try:
        wol.send_magic_packet(mac)
        xbmcgui.Dialog().notification('Moonlight', 'Paquete Wake-on-LAN enviado a ' + mac,
                                       xbmcgui.NOTIFICATION_INFO, 3000)
    except Exception as e:
        xbmcgui.Dialog().notification('Moonlight', 'Error enviando WOL: ' + str(e),
                                       xbmcgui.NOTIFICATION_ERROR, 4000)


def router(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    action = params.get('action')

    if action == 'stream':
        route_stream(params.get('game', ''))
    elif action == 'pair':
        route_pair()
    elif action == 'wol':
        route_wol()
    else:
        route_list()


if __name__ == '__main__':
    router(sys.argv[2][1:] if len(sys.argv) > 2 else '')
