from flask import Flask, render_template, request, send_file, after_this_request
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
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # ডেটা এক্সট্রাক্ট করা
        info = ydl.extract_info(url, download=True)
        if info is None:
            raise Exception("Video info could not be retrieved.")
            
        # সঠিক ফাইল পাথ তৈরি করা
        filename = ydl.prepare_filename(info)
        base, ext = os.path.splitext(filename)
        mp3_filename = base + '.mp3'
        
        return mp3_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            file_path = download_mp3(url)
            
            # ডাউনলোড শেষ হওয়ার পর ফাইল ডিলিট করার ব্যবস্থা (সার্ভার পরিষ্কার রাখতে)
            @after_this_request
            def remove_file(response):
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as error:
                    app.logger.error(f"Error removing file: {error}")
                return response

            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return f"Error: {str(e)}"
            
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)