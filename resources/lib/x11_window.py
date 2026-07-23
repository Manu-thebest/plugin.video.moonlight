# -*- coding: utf-8 -*-
"""
Minimiza / restaura la ventana de Kodi desde el HOST via libwnck.

Se ejecuta con el python3 del host (flatpak-spawn --host python3 ...).
Usa Wnck.Window.minimize(), que internamente llama a XIconifyWindow
(ICCCM) — el mismo mecanismo que el boton de minimizar de MATE/Marco.

wmctrl -b add,hidden NO funciona con Marco: ignora la peticion EWMH
de estado HIDDEN. Por eso este script existe.

Uso: python3 x11_window.py [minimize|restore] [nombre_ventana]
"""
import sys

import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else 'minimize'
    match = sys.argv[2] if len(sys.argv) > 2 else 'Kodi'

    screen = Wnck.Screen.get_default()
    screen.force_update()

    target = None
    for w in screen.get_windows():
        name = w.get_name() or ''
        if name == match:
            target = w
            break
        if target is None and match.lower() in name.lower():
            target = w

    if target is None:
        print('VENTANA NO ENCONTRADA: ' + match)
        return 1

    if action == 'minimize':
        target.minimize()
    else:
        target.unminimize(0)
        target.activate(0)

    print(action.upper() + ' OK: ' + (target.get_name() or ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
