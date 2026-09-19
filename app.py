from flask import Flask, render_template, request, send_file
import yt_dlp
import os, uuid

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url') or request.form.get('uri')
    if not url:
        return "Link daal yrrr!"

    filename = f"{uuid.uuid4()}.mp4"
    os.makedirs("downloads", exist_ok=True)
    filepath = os.path.join("downloads", filename)

    options = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': filepath,
        'noplaylist': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        return send_file(filepath, as_attachment=True, download_name="video.mp4")
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
