from flask import Flask, request, render_template_string
import yt_dlp
import os

app = Flask(__name__)

HTML = """
<form method="post">
<input name="url" placeholder="YouTube link dalo" style="width:80%;padding:10px">
<button>Download</button>
</form>
<p>{{msg}}</p>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""
    if request.method == "POST":
        url = request.form.get("url")
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': '/tmp/%(title)s.%(ext)s',
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'player_skip': ['webpage', 'configs']
                    }
                },
                'nocheckcertificate': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                msg = f"Ho gaya! File: {info['title']}"
        except Exception as e:
            msg = f"Error: {str(e)}"
    return render_template_string(HTML, msg=msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
