# SouthPark Downloader

## Descripción

Este script permite descargar episodios de SouthPark desde streams en formato HLS (`.m3u8`) protegidos con cookies de sesión. Descarga el video y el audio por separado, los combina usando `ffmpeg`, añade metadata con el idioma del audio y organiza los archivos descargados en carpetas según temporada y capítulo.

---

## Requisitos

* **Python 3** instalado.
* **yt-dlp** instalado y accesible desde la terminal (puedes instalarlo con `pip install yt-dlp`).
* **ffmpeg** instalado y accesible desde la terminal.
  ([https://ffmpeg.org/download.html](https://ffmpeg.org/download.html))
* Archivo `cookies.txt` en la misma carpeta que el script, exportado desde tu navegador.

---

## Uso

1. Coloca el archivo `cookies.txt` exportado en la misma carpeta que el script.

2. Ejecuta el script:

```bash
python southpark_downloader.py
```

3. El script te pedirá:

   * Número de temporada (por ejemplo, `1` o `10`).
   * Número de capítulo (por ejemplo, `1` o `12`).
   * Nombre del capítulo (ejemplo: `Cartman consigue una sonda anal`).
   * Código del idioma del audio en formato ISO 639-2 (`spa` para español, `eng` para inglés, etc.).
   * URL del video (archivo `.m3u8` de video).
   * URL del audio (archivo `.m3u8` de audio).

4. El script descargará video y audio por separado, los combinará con `ffmpeg`, agregará el metadata de idioma y guardará el archivo final en:

```
SouthPark/Season XX/Chapter_XX_NombreIdioma.mp4
```

donde `XX` es el número con ceros a la izquierda (ej. `Season 01`, `Chapter_01`).

---

## Cómo obtener el archivo `cookies.txt`

Para acceder a streams protegidos, necesitas cookies válidas que la página usa para autorizar la descarga.

* En Firefox o Chrome, abre la página oficial de SouthPark en la región permitida.
* Inicia sesión si es necesario.
* Usa una extensión como **EditThisCookie** (Chrome) o exporta las cookies con las DevTools (`Application > Cookies > export`).
* Guarda las cookies en formato Netscape en un archivo llamado `cookies.txt`.
* El archivo debe contener cookies válidas y no expiradas para el dominio `southpark.lat` o el dominio de streaming.
  
---

## Cómo obtener las URLs de video y audio (.m3u8)

1. Abre la página del episodio en tu navegador.
2. Usa las DevTools (F12) y ve a la pestaña `Network`.
3. Filtra por `m3u8`.
4. Reproduce el episodio, y busca las solicitudes de archivos `.m3u8` que carguen video y audio.
5. Copia la URL del archivo `m3u8` que corresponda al video (generalmente el de mayor resolución) y la URL del audio (normalmente un stream separado).
6. Usa esas URLs como entrada para el script.

---

## Notas importantes

* Los enlaces `.m3u8` suelen tener tokens de expiración. Si recibes error `403 Forbidden`, probablemente expiraron y debes obtener nuevos.
* La calidad del video depende del link que uses; asegúrate de usar la URL que corresponda a la calidad deseada.
* La sincronización entre audio y video puede variar ligeramente (desfase de 1-2 segundos).
* El script requiere que `yt-dlp` y `ffmpeg` estén instalados y configurados en la variable PATH para funcionar.

---

## Estructura del script

* Descarga video y audio por separado con `yt-dlp`.
* Combina audio y video con `ffmpeg`, copiando video y recodificando audio a AAC.
* Añade el código de idioma al audio en los metadatos.
* Organiza episodios en carpetas por temporada.
* Limpia archivos temporales tras combinación.
