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
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'cookiefile': cookie_file if os.path.exists(cookie_file) else None,
        'quiet': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # direct download link
            download_url = None
            if 'url' in info:
                download_url = info['url']
            elif 'formats' in info and info['formats']:
                # best mp4 wala format dhoondo
                for f in reversed(info['formats']):
                    if f.get('ext') == 'mp4' and f.get('url'):
                        download_url = f['url']
                        break
                if not download_url:
                    download_url = info['formats'][-1]['url']

            return jsonify({
                'title': info.get('title'),
                'download_url': download_url,
                'thumbnail': info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
