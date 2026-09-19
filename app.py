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

    cookie_file = 'cookies.txt'
    
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'cookiefile': cookie_file if os.path.exists(cookie_file) else None,
        'quiet': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            download_url = None
            if info.get('formats'):
                # sabse acchi quality wala format lo
                best = None
                for f in info['formats']:
                    if f.get('url'):
                        best = f
                if best:
                    download_url = best['url']
            else:
                download_url = info.get('url')

            return jsonify({
                'title': info.get('title'),
                'download_url': download_url,
                'thumbnail': info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
