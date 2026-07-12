# 🌙 Moonlight Game Streaming — Kodi Addon

**plugin.video.moonlight** — Addon de Kodi para listar y lanzar juegos desde un host **Sunshine** vía **Moonlight** (Flatpak).

## ✨ Características

- 🔍 **Lista juegos** — Consulta el host Sunshine y muestra los juegos disponibles (texto plano, compatible con Kodi Matrix/Nexus).
- 🎮 **Streaming con un clic** — Lanza Moonlight (Flatpak) con la resolución, FPS, bitrate y códec que configures.
- 🔗 **Emparejamiento integrado** — Asistente para emparejar con Sunshine desde el propio addon.
- ⚡ **Wake-on-LAN** — Enciende el PC host enviando un paquete mágico.
- 🪟 **Ocultación nativa de Kodi** — Usa `playercorefactory.xml` (mecanismo oficial de Kodi para reproductores externos), sin hacks de ventanas.
- 🔧 **Multiplataforma** — Funciona tanto con Kodi nativo como con Kodi Flatpak.

## 📋 Requisitos

- **Kodi** 19 (Matrix) o superior (Python 3)
- **Sunshine** instalado en el PC host ([sunshine-stream.com](https://sunshine-stream.com))
- **Moonlight** instalado vía Flatpak en el equipo Kodi:
  ```bash
  flatpak install com.moonlight_stream.Moonlight
  ```
- **Permisos Flatpak** (si Kodi corre como Flatpak):
  ```bash
  flatpak override --user tv.kodi.Kodi --talk-name=org.freedesktop.Flatpak
  ```

## 📦 Instalación

1. Descarga el ZIP desde [Releases](https://github.com/Manu-thebest/plugin.video.moonlight/releases)
2. En Kodi: **Add-ons → Instalar desde zip** → selecciona el archivo
3. Ve a **Ajustes del addon** y configura:
   - **IP del host** donde corre Sunshine (ej. `192.168.1.43`)
   - **Resolución, FPS, bitrate** según tu red y preferencias
   - (Opcional) **MAC** del host para Wake-on-LAN

## 🎮 Cómo usar

1. Abre el addon desde **Programas → Moonlight Game Streaming**
2. Selecciona un juego de la lista
3. ¡A jugar! Kodi se oculta automáticamente y Moonlight inicia el streaming

## ⚙️ Ajustes

| Sección | Parámetros |
|---------|-----------|
| **Sunshine (PC host)** | IP, MAC, PIN de emparejamiento, timeout |
| **Streaming (Moonlight)** | Resolución, FPS, bitrate, códec, modo pantalla, audio, HDR, V-Sync |
| **Avanzado** | Depuración, argumentos extra |

## 🐳 Compatibilidad con contenedores

El addon detecta automáticamente si Kodi corre dentro de un sandbox Flatpak:
- **Kodi Flatpak** → usa `flatpak-spawn --host` para lanzar Moonlight
- **Kodi nativo** → llama a `flatpak run` directamente

## 📝 Historial de versiones

- **1.1.0** — Arquitectura nativa de reproductor externo (playercorefactory.xml)
- **1.0.3** — Versión inicial con gestión manual de ventanas

## 📄 Licencia

MIT
