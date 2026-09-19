from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>YT Downloader</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:system-ui;text-align:center;padding:20px;background:#111;color:#fff}
input{width:90%;max-width:400px;padding:14px;border-radius:10px;border:none;font-size:16px}
button{padding:14px 24px;background:#ff0000;color:#fff;border:none;border-radius:10px;font-size:16px;margin-top:12px}
img{border-radius:10px;margin-top:10px}
.card{background:#222;padding:20px;border-radius:15px;margin-top:20px;display:inline-block}
</style>
</head>
<body>
<h2>🔴 YouTube Downloader</h2>
<input id="url" placeholder="YouTube link yaha paste karo">
<br>
<button onclick="go()">Download</button>
<div id="r"></div>
<script>
async function go(){
 let u=document.getElementById('url').value;
 if(!u){alert('Link daalo pehle');return;}
 document.getElementById('r').innerHTML='<p>Loading...</p>';
 let f=new FormData(); f.append('url',u);
 let res=await fetch('/download',{method:'POST',body:f});
 let d=await res.json();
 if(d.error){document.getElementById('r').innerHTML='<p style=color:#ff6b6b>'+d.error+'</p>'}
 else{
  document.getElementById('r').innerHTML=`<div class=card><h3>${d.title}</h3><img src="${d.thumbnail}" width="320"><br><br><a href="${d.download_url}" target="_blank"><button>⬇️ Download Now</button></a></div>`;
 }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/download', methods=['POST'])
def dl():
    url = request.form.get('url')
    ydl_opts = {'noplaylist': True, 'quiet': True, 'extractor_args': {'youtube': {'player_client': ['android']}}}
    # agar cookies.txt hai toh use karega
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            best = info.get('url')
            if not best and info.get('formats'):
                best = info['formats'][-1]['url']
            return jsonify({'title': info.get('title'), 'thumbnail': info.get('thumbnail'), 'download_url': best})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
