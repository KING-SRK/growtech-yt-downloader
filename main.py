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
        'cookiefile': 'cookies.txt',  # তোমার দেওয়া কুকি ফাইল
        # 'ffmpeg_location' সরিয়ে দিয়েছি কারণ Render-এ এটা অটোমেটিক থাকে
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'no_warnings': True,
        'nocheckcertificate': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # ফাইলপাথ ঠিকভাবে পাওয়ার জন্য prepare_filename ব্যবহার করা হলো
        filename = ydl.prepare_filename(info)
        base, ext = os.path.splitext(filename)
        return base + '.mp3'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            file_path = download_mp3(url)
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            # এরর মেসেজটা একটু পরিষ্কারভাবে দেখাবে
            return f"Error: {str(e)}"
    return render_template('index.html')

if __name__ == '__main__':
    # পোর্ট এবং হোস্ট সেট করা হলো যাতে ক্লাউডে সুবিধা হয়
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)