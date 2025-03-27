import yt_dlp
import os
from PIL import Image
from io import BytesIO
import eyed3
import requests

# Solicita o caminho para salvar os arquivos
save_path = input("Cole o caminho da pasta onde deseja salvar os arquivos: ")
os.makedirs(save_path, exist_ok=True)

# Solicita os links dos vídeos ou playlists (separados por vírgula)
urls = input("Cole os links dos vídeos ou playlists separados por vírgula: ").split(',')

# Lista para armazenar os vídeos que falharam
erros = []

def adicionar_capa_ao_mp3(mp3_path, image_path):
    try:
        if not os.path.exists(mp3_path):
            print(f"⚠️ Arquivo MP3 não encontrado: {mp3_path}")
            return

        audiofile = eyed3.load(mp3_path)
        if audiofile.tag is None:
            audiofile.initTag()

        with open(image_path, "rb") as img_file:
            audiofile.tag.images.set(3, img_file.read(), "image/jpeg")  # 3 é o código para a capa
        audiofile.tag.save()
        print(f"🖼️ Capa adicionada ao MP3: {mp3_path}")
    except Exception as e:
        print(f"⚠️ Erro ao adicionar capa ao MP3: {e}")

def baixar_thumbnail(title, thumbnail_url):
    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            # Converte a imagem para JPEG
            image = Image.open(BytesIO(response.content))
            image = image.convert("RGB")  # Converte para o formato RGB
            image_path = os.path.join(save_path, f"{title}_thumbnail.jpg")
            image.save(image_path, "JPEG")  # Salva a imagem como .jpg
            print(f"📸 Capa salva como JPG: {image_path}")
            return image_path
    except Exception as e:
        print(f"⚠️ Erro ao baixar thumbnail para {title}: {e}")
        return None

def baixar_video(video_url, index, total):
    try:
        print(f"🎵 ({index}/{total}) Baixando: {video_url}")
        
        audio_options = {
            'format': 'bestaudio/best',  # Seleciona o melhor formato de áudio
            'extractaudio': True,       # Extrai apenas o áudio
            'audioformat': 'mp3',        # Converte para MP3
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'noplaylist': True,         # Impede que arquivos extras sejam baixados se for uma playlist
            'writethumbnail': True,     # Baixa a thumbnail
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',  # Extrai o áudio usando FFmpeg
                    'preferredcodec': 'mp3',      # Define o codec como MP3
                    'preferredquality': '192',   # Define a qualidade do áudio
                },
                {
                    'key': 'FFmpegMetadata',     # Adiciona metadados ao arquivo
                },
                {
                    'key': 'EmbedThumbnail',     # Incorpora a thumbnail no arquivo de áudio
                },
            ],
        }

        with yt_dlp.YoutubeDL(audio_options) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Desconhecido')

        mp3_path = os.path.join(save_path, f"{title}.mp3")
        
        # Verifica se o arquivo MP3 foi criado
        if os.path.exists(mp3_path):
            print(f"✅ Download concluído: {title}\n")
        else:
            print(f"⚠️ Arquivo MP3 não foi criado: {title}\n")

    except Exception as e:
        print(f"❌ Erro ao baixar {video_url}: {e}")
        erros.append({"title": title if 'title' in locals() else "Desconhecido", "url": video_url})

for url in urls:
    url = url.strip()
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        if 'entries' in info and isinstance(info['entries'], list):
            total_videos = len(info['entries'])
            print(f"📂 Playlist detectada: {info.get('title', 'Desconhecida')} ({total_videos} vídeos)")
            for i, video in enumerate(info['entries'], start=1):
                if 'url' in video:
                    baixar_video(video['url'], i, total_videos)
        else:
            baixar_video(url, 1, 1)

    except Exception as e:
        print(f"❌ Erro ao processar URL {url}: {e}")
        erros.append({"title": "Desconhecido", "url": url})

if erros:
    print("\n🚨 Vídeos que não foram baixados:")
    for erro in erros:
        print(f"❌ {erro['title']} - {erro['url']}")
else:
    print("\n✅ Todos os vídeos foram baixados com sucesso!")