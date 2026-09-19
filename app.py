from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "Link daal yrrr!"

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join("downloads", filename)
    os.makedirs("downloads", exist_ok=True)

    options = {
        'format': 'best[ext=mp4]',
        'outtmpl': filepath,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        return send_file(filepath, as_attachment=True, download_name="video.mp4")
    except Exception as e:
        return f"Error: {e} - Link sahi hai na check kar"

if __name__ == '__main__':
    app.run(debug=True)

