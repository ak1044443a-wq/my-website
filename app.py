from flask import Flask, request, render_template, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL nahi mila'}), 400

    # cookies.txt ka path
    cookie_file = 'cookies.txt'
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'cookiefile': cookie_file if os.path.exists(cookie_file) else None,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if not video_url:
                # direct url ke liye format nikalna
                formats = info.get('formats', [])
                if formats:
                    video_url = formats[-1]['url']
            
            return jsonify({
                'title': info.get('title'),
                'download_url': video_url,
                'thumbnail': info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
