import os
import subprocess
from datetime import datetime

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

def combine_audio_video(video_file, audio_file, output_file, language_code):
    # Opción para añadir metadata del idioma al audio
    command = (
        f'ffmpeg -y -i "{video_file}" -i "{audio_file}" '
        f'-c:v copy -c:a aac -metadata:s:a:0 language={language_code} "{output_file}"'
    )
    print(f"Combinando audio y video con ffmpeg...")
    run_command(command)

def main():
    # Carpeta base
    base_folder = "SouthPark"
    os.makedirs(base_folder, exist_ok=True)

    # Inputs
    season = input("Número de temporada: ").strip()
    chapter = input("Número de capítulo: ").strip()
    chapter_name = input("Nombre del capítulo: ").strip()
    audio_language = input("Idioma del audio (código ISO 639-2, ejemplo: spa, eng): ").strip()

    # Formato con ceros a la izquierda si es menor a 10
    season_num = int(season)
    chapter_num = int(chapter)
    season_str = f"Season {season_num:02d}"
    chapter_str = f"Chapter_{chapter_num:02d}"

    # Carpeta para la temporada
    season_folder = os.path.join(base_folder, season_str)
    os.makedirs(season_folder, exist_ok=True)

    # Archivos temporales de video y audio
    video_temp = os.path.join(season_folder, "video_temp.mp4")
    audio_temp = os.path.join(season_folder, "audio_temp.mp4")

    # URLs
    video_url = input("URL del video (m3u8): ").strip()
    audio_url = input("URL del audio (m3u8): ").strip()

    # Cookies
    cookies_path = os.path.join(os.getcwd(), "cookies.txt")

    try:
        print("Descargando video...")
        download_stream(video_url, video_temp, cookies_path)

        print("Descargando audio...")
        download_stream(audio_url, audio_temp, cookies_path)

        # Nombre final del archivo
        # Ejemplo: Chapter_01_Cartman consigue una sonda anal_spa.mp4
        safe_chapter_name = chapter_name.replace(" ", "_")
        final_name = f"{chapter_str}_{safe_chapter_name}_{audio_language}.mp4"
        final_path = os.path.join(season_folder, final_name)

        print("Combinando audio y video...")
        combine_audio_video(video_temp, audio_temp, final_path, audio_language)

        # Eliminar archivos temporales
        os.remove(video_temp)
        os.remove(audio_temp)

        print(f"Descarga y combinación completadas: {final_path}")

    except Exception as e:
        print("Ocurrió un error:", e)

if __name__ == "__main__":
    main()
