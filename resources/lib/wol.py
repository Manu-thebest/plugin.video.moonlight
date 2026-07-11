# -*- coding: utf-8 -*-
"""Envio de paquetes magicos Wake-on-LAN para encender el PC host."""
import socket
import re


def send_magic_packet(mac_address, broadcast_ip='255.255.255.255', port=9):
    mac_clean = re.sub(r'[^0-9A-Fa-f]', '', mac_address)
    if len(mac_clean) != 12:
        raise ValueError('Direccion MAC no valida: ' + mac_address)

    mac_bytes = bytes.fromhex(mac_clean)
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        sock.sendto(magic_packet, (broadcast_ip, port))
    finally:
        sock.close()
