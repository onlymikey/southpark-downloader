import os
import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode != 0:
        print("Error ejecutando comando:", command)
        print(result.stderr.decode())
        raise Exception("Error en comando")
    return result.stdout.decode()

def download_stream(url, output, cookies_path):
    command = f'yt-dlp --cookies "{cookies_path}" -o "{output}" "{url}"'
    print(f"Ejecutando: {command}")
    run_command(command)

def combine_multiple_audio(video_file, audio_tracks, output_file):
    inputs = [f'-i "{video_file}"'] + [f'-i "{a["file"]}"' for a in audio_tracks]
    
    maps = ['-map 0:v'] + [f'-map {i+1}:a' for i in range(len(audio_tracks))]
    
    metadata = []
    for idx, a in enumerate(audio_tracks):
        metadata.append(f'-metadata:s:a:{idx} language={a["lang"]}')
    
    command = (
        f'ffmpeg -y {" ".join(inputs)} '
        f'-c:v copy -c:a aac {" ".join(maps)} {" ".join(metadata)} "{output_file}"'
    )
    print("Combinando audio y video con ffmpeg...")
    run_command(command)

def main():
    base_folder = "SouthPark"
    os.makedirs(base_folder, exist_ok=True)

    # Datos del episodio
    season = int(input("Número de temporada: ").strip())
    chapter = int(input("Número de capítulo: ").strip())
    chapter_name = input("Nombre del capítulo: ").strip()

    season_str = f"Season {season:02d}"
    chapter_str = f"Chapter_{chapter:02d}"

    season_folder = os.path.join(base_folder, season_str)
    os.makedirs(season_folder, exist_ok=True)

    video_url = input("URL del video (m3u8): ").strip()
    cookies_path = os.path.join(os.getcwd(), "cookies.txt")
    video_temp = os.path.join(season_folder, "video_temp.mp4")

    print("Descargando video...")
    download_stream(video_url, video_temp, cookies_path)

    # Lista de pistas de audio
    audio_tracks = []
    add_more = True
    track_num = 1

    while add_more:
        audio_url = input(f"URL del audio #{track_num} (m3u8): ").strip()
        audio_lang = input(f"Idioma del audio #{track_num} (ISO 639-2, ej: spa, eng): ").strip()
        audio_temp = os.path.join(season_folder, f"audio_temp_{track_num}.mp4")

        print(f"Descargando audio #{track_num}...")
        download_stream(audio_url, audio_temp, cookies_path)

        audio_tracks.append({"file": audio_temp, "lang": audio_lang})

        more = input("¿Agregar otro idioma de audio? (s/n): ").strip().lower()
        if more != "s":
            add_more = False
        track_num += 1

    safe_chapter_name = chapter_name.replace(" ", "_")
    final_name = f"{chapter_str}_{safe_chapter_name}.mkv"
    final_path = os.path.join(season_folder, final_name)

    combine_multiple_audio(video_temp, audio_tracks, final_path)

    # Limpieza
    os.remove(video_temp)
    for a in audio_tracks:
        os.remove(a["file"])

    print(f"Archivo final creado: {final_path}")

if __name__ == "__main__":
    main()
