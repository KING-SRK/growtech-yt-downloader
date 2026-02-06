from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# গান সেভ করার ফোল্ডার তৈরি
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'cookiefile': 'cookies.txt',
        'ffmpeg_location': r'C:\Users\Joy & Bijoy\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin', 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            file_path = download_mp3(url)
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)