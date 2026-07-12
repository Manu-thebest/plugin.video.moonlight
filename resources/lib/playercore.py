# -*- coding: utf-8 -*-
"""
Integra el lanzamiento de Moonlight con el mecanismo NATIVO de Kodi para
reproductores externos (playercorefactory.xml), documentado aqui:
https://kodi.wiki/view/External_players

En vez de minimizar/restaurar la ventana de Kodi a mano (poco fiable segun el
gestor de ventanas), se define un "ExternalPlayer" con <hidexbmc>true</hidexbmc>,
que es la forma en que el propio Kodi oculta su ventana mientras el programa
externo esta activo y la recupera el solo al terminar. El comando exacto
(con host, juego y todos los parametros de streaming) se escribe en el
<filename>/<args> del player cada vez, justo antes de lanzar, para que
recoja siempre los ajustes actuales.
"""
import os
import xml.etree.ElementTree as ET
import xbmc
import xbmcvfs
import kodiutils as ku
import moonlight

PLAYER_NAME = 'MoonlightExternal'
PROTOCOL = 'moonlightstream'


def _pcf_path():
    return xbmcvfs.translatePath('special://userdata/playercorefactory.xml')


def _quote(arg):
    return '"' + arg.replace('\\', '\\\\').replace('"', '\\"') + '"'


def update_playercorefactory(host, app_name):
    """
    Crea o actualiza userdata/playercorefactory.xml con nuestro reproductor
    externo y su regla, dejando intacto cualquier otro reproductor/regla que
    ya hubiera. Devuelve True si se pudo escribir el fichero.
    """
    path = _pcf_path()
    argv = moonlight.build_stream_argv(host, app_name)
    exe, rest = argv[0], argv[1:]
    args_text = ' '.join(_quote(a) for a in rest)

    root = None
    if xbmcvfs.exists(path):
        try:
            root = ET.parse(path).getroot()
        except Exception as e:
            ku.log('playercorefactory.xml existente no se pudo leer, se regenera: ' + str(e),
                   xbmc.LOGWARNING)
    if root is None:
        root = ET.Element('playercorefactory')

    players = root.find('players')
    if players is None:
        players = ET.SubElement(root, 'players')
    existing = players.find("player[@name='%s']" % PLAYER_NAME)
    if existing is not None:
        players.remove(existing)
    player = ET.SubElement(players, 'player')
    player.set('name', PLAYER_NAME)
    player.set('type', 'ExternalPlayer')
    player.set('video', 'true')
    player.set('audio', 'false')
    ET.SubElement(player, 'filename').text = exe
    ET.SubElement(player, 'args').text = args_text
    ET.SubElement(player, 'hidexbmc').text = 'true'

    rules = root.find('rules')
    if rules is None:
        rules = ET.SubElement(root, 'rules')
        rules.set('action', 'prepend')
    existing_rule = rules.find("rule[@player='%s']" % PLAYER_NAME)
    if existing_rule is not None:
        rules.remove(existing_rule)
    rule = ET.SubElement(rules, 'rule')
    rule.set('name', PLAYER_NAME)
    rule.set('protocols', PROTOCOL)
    rule.set('player', PLAYER_NAME)

    try:
        ET.ElementTree(root).write(path, encoding='UTF-8', xml_declaration=True)
    except Exception as e:
        ku.log('No se pudo escribir playercorefactory.xml: ' + str(e), xbmc.LOGERROR)
        return False

    ku.log('playercorefactory.xml actualizado (%s): filename=%s args=%s' % (path, exe, args_text))
    return True
