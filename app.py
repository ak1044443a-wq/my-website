from flask import Flask, request, render_template, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST', 'GET'])
def download():
    # Form se aaye ya JSON se, dono handle karega
    if request.method == 'GET':
        return "Method not allowed, use POST", 405
        
    data = request.get_json(silent=True) or request.form
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'www.youtube.com_cookies.txt',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Direct download link
            direct_url = info.get('url')
            # Agar direct url nahi to best format nikal lo
            if not direct_url and info.get('formats'):
                direct_url = info['formats'][-1]['url']
                
            return jsonify({
                'title': info.get('title'),
                'url': direct_url,
                'formats': info.get('formats', [])[-3:]
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
