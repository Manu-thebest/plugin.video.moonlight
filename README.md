# Moonlight Game Streaming — Kodi Addon

[![Kodi](https://img.shields.io/badge/Kodi-20+-brightgreen)](https://kodi.tv)
[![Platform](https://img.shields.io/badge/platform-Linux-blue)](https://kodi.tv)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Moonlight](https://img.shields.io/badge/Moonlight-Flatpak-9cf)](https://flathub.org/apps/com.moonlight_stream.Moonlight)

**Moonlight Game Streaming** es un addon para Kodi que permite listar y lanzar juegos desde un host [Sunshine](https://github.com/LizardByte/Sunshine) vía [Moonlight](https://moonlight-stream.org) (Flatpak). Compatible con Kodi nativo y Kodi Flatpak.

---

## 📋 Tabla de contenidos

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Ajustes](#ajustes)
- [Estructura del código](#estructura-del-código)
- [Solución de problemas](#solución-de-problemas)
- [Historial de versiones](#historial-de-versiones)
- [Licencia](#licencia)

---

## 📖 Descripción

Este addon actúa como un puente entre Kodi y Moonlight:

1. **Lista juegos** — Obtiene la lista de aplicaciones/juegos configurados en Sunshine.
2. **Emparejamiento** — Facilita el pairing con el host Sunshine mediante PIN.
3. **Streaming** — Lanza Moonlight con todos los parámetros de vídeo/audio configurados.
4. **Wake-on-LAN** — Enciende el PC host si está apagado.

### Características principales

| Característica | Detalle |
|---------------|---------|
| **Listado** | Solo texto, sin depender de APIs externas (SteamGridDB, etc.) |
| **Minimizar Kodi** | Usa `Minimize` builtin + `wmctrl`/`xdotool` para restaurar |
| **Compatibilidad Flatpak** | Detecta si Kodi corre en Flatpak y usa `flatpak-spawn --host` |
| **Audio SDL** | Configurable: `pulse`, `pipewire`, `alsa` o automático |
| **WOL** | Wake-on-LAN integrado, sin scripts externos |
| **Plug & Play** | Sin dependencias externas más allá de Moonlight Flatpak |

---

## ⚙️ Requisitos

### Hardware / Software

| Componente | Requisito |
|------------|-----------|
| **Kodi** | v20 (Nexus) o superior |
| **Sistema** | Linux (probado en Debian/Ubuntu, Arch) |
| **Moonlight** | Flatpak: `com.moonlight_stream.Moonlight` |
| **Sunshine** | En ejecución en el PC host (puerto 47989-47990) |
| **PC host** | Con Sunshine y juegos configurados |

### Instalación de Moonlight Flatpak

```bash
# Instalar Moonlight
flatpak install flathub com.moonlight_stream.Moonlight

# Si Kodi corre como Flatpak, necesitas permisos:
flatpak override --user tv.kodi.Kodi --talk-name=org.freedesktop.Flatpak
```

### Herramientas opcionales (para restaurar ventana de Kodi)

```bash
# Para que Kodi recupere el foco tras el streaming
sudo apt install wmctrl xdotool   # Debian/Ubuntu
sudo pacman -S wmctrl xdotool     # Arch
```

---

## 📦 Instalación

### Desde ZIP (recomendado)

1. Descarga el [último release](https://github.com/Manu-thebest/plugin.video.moonlight/releases)
2. En Kodi: **Add-ons → Instalar desde ZIP** → seleccionar el archivo
3. Ve a **Add-ons → Programas → Moonlight Game Streaming**

### Desde el repositorio

```bash
git clone https://github.com/Manu-thebest/plugin.video.moonlight.git
cd plugin.video.moonlight
zip -r ../plugin.video.moonlight.zip .
# Transferir el ZIP a Kodi e instalar desde ZIP
```

---

## 🔧 Configuración

### 1. Configurar el host Sunshine

Abre los ajustes del addon y rellena:

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| **IP del host** | `192.168.1.43` | IP del PC con Sunshine |
| **MAC (WOL)** | `10:FF:E0:7D:ED:1B` | Para Wake-on-LAN |
| **PIN** | `1234` | PIN que introducirás en Sunshine |

### 2. Emparejar con Sunshine

1. En los ajustes del addon, pulsa **"Emparejar ahora"**
2. Ve a `https://<IP_DEL_HOST>:47990` desde un navegador
3. Introduce el PIN que configuraste
4. Vuelve a Kodi y confirma

### 3. Configurar streaming

Ajusta resolución, FPS, bitrate y códec según tu red y hardware.

---

## 🎮 Uso

1. Abre **Moonlight Game Streaming** desde Programas
2. Espera a que se listen los juegos del host
3. Pulsa sobre un juego para iniciar streaming
4. Kodi se minimiza automáticamente
5. Al cerrar Moonlight, Kodi restaura su ventana

### Menú contextual

En cada juego disponible puedes:

| Acción | Descripción |
|--------|-------------|
| **Actualizar lista** | Refresca la lista de juegos |
| **Ajustes** | Abre la configuración del addon |

---

## ⚙️ Ajustes detallados

### Sección: Sunshine (PC host)

| ID | Tipo | Defecto | Descripción |
|----|------|---------|-------------|
| `host_ip` | ipaddress | `192.168.1.43` | Dirección IP del host Sunshine |
| `host_mac` | text | — | Dirección MAC para Wake-on-LAN |
| `pair_pin` | text | `1234` | PIN de emparejamiento (4 dígitos) |
| `connect_timeout` | number | `8` | Timeout al listar juegos (segundos) |

### Sección: Streaming (Moonlight)

| ID | Tipo | Defecto | Descripción |
|----|------|---------|-------------|
| `moonlight_flatpak_id` | text | `com.moonlight_stream.Moonlight` | ID del Flatpak de Moonlight |
| `resolution` | select | `1080p` | `720p`, `1080p`, `1440p`, `4K`, `Personalizada` |
| `custom_resolution` | text | `1920x1080` | Solo si resolución = Personalizada |
| `fps` | select | `60` | `30`, `60`, `90`, `120` |
| `bitrate` | number | `20000` | Bitrate en Kbps |
| `codec` | select | `auto` | `auto`, `H.264`, `HEVC`, `AV1` |
| `display_mode` | select | `fullscreen` | `fullscreen`, `windowed`, `borderless` |
| `audio_config` | select | `stereo` | `stereo`, `5.1-surround`, `7.1-surround` |
| `audio_driver` | select | `pulse` | `pulse`, `pipewire`, `alsa`, `Automático` |
| `audio_on_host` | bool | false | Reproducir audio también en el host |
| `vsync` | bool | true | V-Sync |
| `hdr` | bool | false | HDR |
| `yuv444` | bool | false | YUV 4:4:4 |
| `game_optimization` | bool | true | Optimizaciones de Sunshine (sops) |
| `quit_after` | bool | true | Cerrar juego en host al terminar |
| `keep_awake` | bool | true | Evitar que la pantalla se apague |
| `mute_kodi` | bool | true | Silenciar Kodi durante streaming |

### Sección: Avanzado

| ID | Tipo | Defecto | Descripción |
|----|------|---------|-------------|
| `debug_logging` | bool | false | Registro de depuración en kodi.log |
| `extra_args` | text | — | Argumentos extra para Moonlight CLI |

---

## 📁 Estructura del código

```
plugin.video.moonlight/
├── addon.xml              # Metadatos del addon (v1.0.3)
├── default.py             # Router principal + menú
├── icon.png               # Icono 256×256
├── fanart.jpg             # Fanart 1920×1080
└── resources/
    ├── settings.xml       # Definición de ajustes (formato antiguo)
    └── lib/
        ├── __init__.py
        ├── moonlight.py   # Wrapper CLI de Moonlight (list, pair, stream, quit)
        ├── kodiutils.py   # Utilidades: settings, logging, restauración de ventana
        └── wol.py         # Envío de paquetes Wake-on-LAN
```

### Flujo de llamadas

```
Kodi (menú)
  └─ default.py :: router()
       ├─ route_list()    ──> moonlight.list_games(host)
       ├─ route_stream()  ──> moonlight.stream(host, game)
       ├─ route_pair()    ──> moonlight.pair(host, pin)
       └─ route_wol()     ──> wol.send_magic_packet(mac)
```

### moonlight.py

Wrapper completo de la CLI de `moonlight-qt`:

| Función | Comando Moonlight | Descripción |
|---------|-------------------|-------------|
| `list_games(host)` | `moonlight list <host>` | Lista apps del host |
| `pair(host, pin)` | `moonlight pair <host> -pin <pin>` | Empareja con el host |
| `stream(host, app)` | `moonlight stream <host> <app>` | Inicia streaming |
| `quit_running(host)` | `moonlight quit <host>` | Cierra sesión activa |

Características:
- **Detección automática Flatpak**: usa `flatpak-spawn --host` si Kodi corre en Flatpak.
- **Parsing robusto**: filtra URLs, líneas de log y ruido de la salida de `moonlight list`.
- **Argumentos toggle**: `-vsync`/`-no-vsync`, `-hdr`/`-no-hdr`, etc.

### kodiutils.py

Utilidades comunes:

| Función | Descripción |
|---------|-------------|
| `get_setting(id)` | Obtiene ajuste como string |
| `get_setting_bool(id)` | Obtiene ajuste booleano |
| `get_setting_int(id)` | Obtiene ajuste numérico |
| `log(msg, level)` | Log condicional (solo si debug activado) |
| `try_restore_kodi_window()` | Restaura ventana de Kodi tras Minimize |

### wol.py

Implementación ligera de Wake-on-LAN sin dependencias externas:

```python
send_magic_packet("10:FF:E0:7D:ED:1B")       # Broadcast por defecto
send_magic_packet("10:FF:E0:7D:ED:1B",        # Broadcast específico
                  broadcast_ip="192.168.1.255",
                  port=9)
```

---

## 🔍 Solución de problemas

### "No se pudo conectar con el host"

- Verifica que Sunshine esté ejecutándose: `sudo systemctl status sunshine`
- Comprueba que no hay cortafuegos bloqueando el puerto 47989-47990
- Aumenta el timeout de conexión en Ajustes > Avanzado

### "No se encontraron juegos"

- ¿Hay apps configuradas en Sunshine? (Sunshine Web UI → Applications)
- Activa el registro de depuración y revisa `kodi.log` para ver la salida cruda de `moonlight list`

### El audio no suena hasta minimizar/restaurar Moonlight

- Cambia el **Controlador de audio SDL** a `pulse` o `pipewire` según tu sistema
- Este es un problema conocido de Moonlight-Qt; el ajuste `SDL_AUDIODRIVER` suele resolverlo

### Moonlight no se lanza

- Verifica que el Flatpak está instalado: `flatpak list | grep Moonlight`
- Si Kodi corre en Flatpak, asegúrate del override: `flatpak override --user tv.kodi.Kodi --talk-name=org.freedesktop.Flatpak`

### La ventana de Kodi no se restaura

- Instala `wmctrl` y `xdotool` (ver [requisitos](#herramientas-opcionales-para-restaurar-ventana-de-kodi))
- En Wayland puro, estas herramientas no funcionan; el addon simplemente no restaura (no bloquea)

---

## 📜 Historial de versiones

### v1.0.3 (actual)
- Kodi se minimiza al lanzar Moonlight (`builtin Minimize`)
- Intenta restaurar ventana al terminar (`wmctrl`/`xdotool`)
- Nuevo ajuste: **Controlador de audio SDL** (`SDL_AUDIODRIVER`)
- Corrección de audio que no sonaba hasta minimizar/restaurar

### v1.0.2
- Corregido listado de juegos: se eliminó `list -csv` (mezclaba URLs con nombres)
- Parseo mejorado: descarta URLs y líneas de log

### v1.0.1
- Eliminadas carátulas (SteamGridDB) para simplificar
- Lista de solo texto con icono del addon

### v1.0.0
- Conexión y emparejamiento con Sunshine
- Lanzamiento de Moonlight vía Flatpak
- Soporte `flatpak-spawn` para Kodi Flatpak
- Wake-on-LAN

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-caracteristica`
3. Commit: `git commit -m 'Añade nueva característica'`
4. Push: `git push origin feature/nueva-caracteristica`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está licenciado bajo **MIT License**. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

<p align="center">
  <img src="icon.png" width="128" alt="Moonlight Game Streaming">
  <br>
  <sub>Hecho con ❤️ para la comunidad de Kodi</sub>
</p>
