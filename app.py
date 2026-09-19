from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>YouTube Downloader</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;text-align:center;padding:20px;background:#f5f5f5}
input{width:80%;padding:12px;margin:10px;font-size:16px}
button{padding:12px 20px;background:red;color:white;border:none;font-size:16px;border-radius:5px}
#result{margin-top:20px}
</style>
</head>
<body>
<h2>🔴 YouTube Video Downloader</h2>
<input id="url" placeholder="YouTube link paste karo...">
<br>
<button onclick="download()">Download</button>
<div id="result"></div>
<script>
async function download(){
 let url=document.getElementById('url').value;
 document.getElementById('result').innerHTML="Loading...";
 let form=new FormData(); form.append('url',url);
 let res=await fetch('/download',{method:'POST',body:form});
 let data=await res.json();
 if(data.error){document.getElementById('result').innerHTML="<p style=color:red>"+data.error+"</p>"}
 else{
  document.getElementById('result').innerHTML=`<h3>${data.title}</h3><img src="${data.thumbnail}" width="300"><br><br><a href="${data.download_url}" target="_blank"><button>Click to Download Video</button></a>`;
 }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL nahi mila'}), 400

    cookie_file = 'cookies.txt'
    ydl_opts = {
        'noplaylist': True,
        'cookiefile': cookie_file if os.path.exists(cookie_file) else None,
        'quiet': True,
        'extractor_args': {'youtube': {'player_client': ['android']}},
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            best_url = info.get('url')
            if not best_url and info.get('formats'):
                best_url = info['formats'][-1]['url']
            return jsonify({
                'title': info.get('title'),
                'download_url': best_url,
                'thumbnail': info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
