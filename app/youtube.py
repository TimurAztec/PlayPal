import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


def search_and_download_music(query, output_path):
    search_url = f"ytsearch:{query}"
    cookies_file = os.path.join(os.getcwd(), "cookies.txt")

    if not os.path.exists(cookies_file):
        raise FileNotFoundError(f"Cookies file not found: {cookies_file}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'cookiefile': cookies_file,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=True)

            keywords = ['official music video', 'music video', 'song', 'track', 'audio', 'lyrics']
            is_music = False

            tags = info.get('tags', [])
            if any(keyword in tag.lower() for tag in tags for keyword in keywords):
                is_music = True

            categories = info.get('categories', [])
            if 'Music' in categories:
                is_music = True

            if not is_music:
                raise ValueError("Failed to find music source with such name.")

            file_path = ydl.prepare_filename(info)
            if '.NA' in file_path:
                file_path = file_path.replace('.NA', '.mp3')

            if not os.path.exists(file_path):
                base_name = os.path.basename(file_path).replace('.mp3', '')
                found_file = None
                for file in os.listdir(output_path):
                    if base_name in file:
                        found_file = os.path.join(output_path, file)
                        break
                if not found_file:
                    raise ValueError("Failed to generate MP3 file.")
                return found_file

            return file_path

    except DownloadError as e:
        raise ValueError(f"Error downloading audio: {str(e)}")
