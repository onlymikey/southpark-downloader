
# SouthPark Downloader

## Description

This script allows you to download SouthPark episodes from HLS streams (`.m3u8`) protected with session cookies. It downloads video and audio separately, merges them using `ffmpeg`, adds metadata with the audio language, and organizes the downloaded files into folders by season and episode.

---

## Requirements

* **Python 3** installed.
* **yt-dlp** installed and accessible from the terminal (you can install it with `pip install yt-dlp`).
* **ffmpeg** installed and accessible from the terminal.  
  ([https://ffmpeg.org/download.html](https://ffmpeg.org/download.html))
* `cookies.txt` file in the same folder as the script, exported from your browser.

---

## Usage

1. Place the exported `cookies.txt` file in the same folder as the script.

2. Run the script:

```bash
python southpark_downloader.py
````

3. The script will ask you for:

   * Season number (e.g., `1` or `10`).
   * Episode number (e.g., `1` or `12`).
   * Episode name (example: `Cartman gets an anal probe`).
   * Audio language code in ISO 639-2 format (`spa` for Spanish, `eng` for English, etc.).
   * Video URL (video `.m3u8` file).
   * Audio URL (audio `.m3u8` file).

4. The script will download video and audio separately, merge them with `ffmpeg`, add the language metadata, and save the final file in:

```
SouthPark/Season XX/Chapter_XX_EpisodeName_LanguageCode.mp4
```

where `XX` is the zero-padded number (e.g., `Season 01`, `Chapter_01`).

---

## How to get the `cookies.txt` file

To access protected streams, you need valid cookies that the site uses to authorize downloads.

* In Firefox or Chrome, open the official SouthPark site for your allowed region.
* Log in if necessary.
* Use an extension like **EditThisCookie** (Chrome) or export cookies using DevTools (`Application > Cookies > export`).
* Save the cookies in Netscape format in a file named `cookies.txt`.
* The file must contain valid, unexpired cookies for the domain `southpark.lat` or the streaming domain.

---

## How to get the video and audio URLs (.m3u8)

1. Open the episode page in your browser.
2. Open DevTools (F12) and go to the `Network` tab.
3. Filter by `m3u8`.
4. Play the episode and look for `.m3u8` requests loading video and audio streams.
5. Copy the URL for the video `.m3u8` file (usually the highest resolution) and the audio `.m3u8` URL (typically a separate stream).
6. Use those URLs as input to the script.

---

## Important notes

* `.m3u8` URLs usually contain expiration tokens. If you get a `403 Forbidden` error, the URLs likely expired and you need to obtain new ones.
* Video quality depends on the URL you use; make sure to pick the one that matches your desired quality.
* Audio and video synchronization may vary slightly (1-2 seconds offset).
* The script requires `yt-dlp` and `ffmpeg` installed and configured in your PATH to work.

---

## Script structure

* Downloads video and audio separately using `yt-dlp`.
* Merges audio and video with `ffmpeg`, copying video and re-encoding audio to AAC.
* Adds the language code to the audio metadata.
* Organizes episodes into folders by season.
* Cleans up temporary files after merging.

