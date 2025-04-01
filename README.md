# YouTube Audio Downloader

Este script permite baixar áudios de vídeos ou playlists do YouTube e salvar no formato MP3 com capas embutidas automaticamente.

## 📌 Funcionalidades

- Baixa áudios de vídeos ou playlists do YouTube.
- Converte os áudios para MP3 com qualidade 192kbps.
- Baixa e adiciona automaticamente a thumbnail do vídeo como capa do MP3.
- Garante que os arquivos sejam salvos no caminho especificado.

## 📌 Feat 01/04/2025

- Adicionado data e horario atual
- Adicionado forma para baixar o video
- Adicionado perguntas para baixar o Mp4 podendo ser selecionado em (quality:. MKV/AV1/VP9) e (Compatibility:. MP4/H.264) se o video não possuir o MP4/H.264 ele ira baixar a maior qualidade do video

## 🛠️ Instalação

### 1. Instalar o Python

Se você ainda não tem o Python instalado, baixe e instale a versão mais recente do site oficial:
🔗 [Download Python](https://www.python.org/downloads/)

### 2. Instalar as bibliotecas necessárias

Antes de executar o script, instale as dependências necessárias executando o seguinte comando:

```sh
pip install yt-dlp pillow eyed3 requests
```

Se estiver no Linux ou MacOS, talvez seja necessário instalar o `ffmpeg`:

```sh
sudo apt install ffmpeg  # Para Debian/Ubuntu
brew install ffmpeg      # Para macOS
```

No Windows, você pode baixar o `ffmpeg` [aqui](https://ffmpeg.org/download.html) e adicionar ao PATH.

## 🚀 Como Usar

1. Clone este repositório ou baixe o script:

```sh
git clone https://github.com/VictorYahagui/mp3-dowloader.git
cd seu-repositorio
```

2. Execute o script no terminal ou prompt de comando:

```sh
python downloader.py
```

3. Cole os links dos vídeos ou playlists do YouTube quando solicitado.

4. O download será iniciado e os arquivos serão salvos no diretório especificado.

## 🔧 Problemas e Soluções

Se encontrar erros durante o download:

- Verifique se o `ffmpeg` está instalado corretamente.
- Certifique-se de que as bibliotecas estão atualizadas:
  ```sh
  pip install --upgrade yt-dlp pillow eyed3 requests
  ```

## 📜 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para contribuir e modificar!

---

Criado por VictorYahagui apenas por necessidade
