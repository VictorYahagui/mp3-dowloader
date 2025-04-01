import yt_dlp
import os
from PIL import Image
from io import BytesIO
import eyed3
import requests

def ask_video_preference():
    while True:
        preference = input("Do you prefer 'quality' (best possible, may be MKV/AV1) or 'compatibility' (MP4/H.264)? (quality/compatibility): ").lower()
        if preference in ['quality', 'compatibility']:
            return preference
        print("Invalid option. Please type 'quality' or 'compatibility'.")

def ask_download_option():
    while True:
        option = input("Do you want to download as MP3 (audio only) or MP4 (video with audio)? (mp3/mp4): ").lower()
        if option in ['mp3', 'mp4']:
            return option
        print("Invalid option. Please type 'mp3' or 'mp4'.")

def ask_save_path():
    save_path = input("Paste the folder path where you want to save the files: ")
    os.makedirs(save_path, exist_ok=True)
    return save_path

def ask_urls():
    urls = input("Paste the video or playlist links separated by commas: ").split(',')
    return [url.strip() for url in urls if url.strip()]

def add_cover_to_mp3(mp3_path, image_path):
    try:
        if not os.path.exists(mp3_path):
            print(f"⚠️ MP3 file not found: {mp3_path}")
            return

        audiofile = eyed3.load(mp3_path)
        if audiofile.tag is None:
            audiofile.initTag()

        with open(image_path, "rb") as img_file:
            audiofile.tag.images.set(3, img_file.read(), "image/jpeg")
        audiofile.tag.save()
        print(f"🖼️ Cover added to MP3: {mp3_path}")
    except Exception as e:
        print(f"⚠️ Error adding cover to MP3: {e}")

def download_thumbnail(title, thumbnail_url, save_path):
    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image = image.convert("RGB")
            image_path = os.path.join(save_path, f"{title}_thumbnail.jpg")
            image.save(image_path, "JPEG")
            print(f"📸 Thumbnail saved as JPG: {image_path}")
            return image_path
    except Exception as e:
        print(f"⚠️ Error downloading thumbnail for {title}: {e}")
        return None

def download_mp3(video_url, save_path, index, total):
    try:
        print(f"🎵 ({index}/{total}) Downloading audio: {video_url}")
        
        audio_options = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'writethumbnail': True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'FFmpegMetadata',
                },
                {
                    'key': 'EmbedThumbnail',
                },
            ],
        }

        with yt_dlp.YoutubeDL(audio_options) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Unknown')

        mp3_path = os.path.join(save_path, f"{title}.mp3")
        
        if os.path.exists(mp3_path):
            print(f"✅ Audio downloaded successfully: {title}\n")
        else:
            print(f"⚠️ MP3 file was not created: {title}\n")

        return True

    except Exception as e:
        print(f"❌ Error downloading audio {video_url}: {e}")
        return False

def download_mp4(video_url, save_path, index, total, preference='compatibility'):
    try:
        print(f"🎬 ({index}/{total}) Downloading video ({preference} mode): {video_url}")
        
        # Configurações base
        base_options = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'writethumbnail': True,
            'postprocessors': [
                {
                    'key': 'EmbedThumbnail',
                },
                {
                    'key': 'FFmpegMetadata',
                },
            ],
        }

        if preference == 'compatibility':
            # Ordem de prioridade para compatibilidade:
            # 1. MP4 com H.264
            # 2. Qualquer MP4
            # 3. Melhor formato disponível (fallback)
            format_selector = (
                'bestvideo[ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/'
                'bestvideo[ext=mp4]+bestaudio[ext=m4a]/'
                'bestvideo+bestaudio/best'
            )
            base_options['merge_output_format'] = 'mp4'
            base_options['postprocessors'].insert(0, {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            })
        else:
            # Modo qualidade máxima
            format_selector = 'bestvideo+bestaudio/best'

        video_options = {**base_options, 'format': format_selector}

        with yt_dlp.YoutubeDL(video_options) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Unknown')

        # Verifica o arquivo baixado
        downloaded_files = [f for f in os.listdir(save_path) if f.startswith(title)]
        if downloaded_files:
            final_path = os.path.join(save_path, downloaded_files[0])
            print(f"✅ Video downloaded successfully: {downloaded_files[0]}\n")
            return True

        print(f"⚠️ Video file was not created: {title}\n")
        return False

    except Exception as e:
        print(f"❌ Error downloading video {video_url}: {e}")
        return False

def process_urls(urls, save_path, option, video_preference=None):
    failed_downloads = []
    
    for url in urls:
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                info = ydl.extract_info(url, download=False)

            if 'entries' in info and isinstance(info['entries'], list):
                total_videos = len(info['entries'])
                print(f"📂 Playlist detected: {info.get('title', 'Unknown')} ({total_videos} videos)")
                for i, video in enumerate(info['entries'], start=1):
                    if 'url' in video:
                        if option == 'mp3':
                            if not download_mp3(video['url'], save_path, i, total_videos):
                                failed_downloads.append({"title": video.get('title', 'Unknown'), "url": video['url']})
                        else:
                            if not download_mp4(video['url'], save_path, i, total_videos, video_preference):
                                failed_downloads.append({"title": video.get('title', 'Unknown'), "url": video['url']})
            else:
                if option == 'mp3':
                    if not download_mp3(url, save_path, 1, 1):
                        failed_downloads.append({"title": info.get('title', 'Unknown'), "url": url})
                else:
                    if not download_mp4(url, save_path, 1, 1, video_preference):
                        failed_downloads.append({"title": info.get('title', 'Unknown'), "url": url})

        except Exception as e:
            print(f"❌ Error processing URL {url}: {e}")
            failed_downloads.append({"title": "Unknown", "url": url})
    
    return failed_downloads

def main():
    print("=== YouTube Downloader ===")
    option = ask_download_option()
    
    video_preference = None
    if option == 'mp4':
        video_preference = ask_video_preference()
    
    save_path = ask_save_path()
    urls = ask_urls()
    
    failed_downloads = process_urls(urls, save_path, option, video_preference)
    
    if failed_downloads:
        print("\n🚨 Videos that failed to download:")
        for failed in failed_downloads:
            print(f"❌ {failed['title']} - {failed['url']}")
    else:
        print("\n✅ All videos downloaded successfully!")

if __name__ == "__main__":
    main()