from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'video' not in request.files:
            return "No file part"
        file = request.files['video']
        if file.filename == '':
            return "No selected file"
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # تقسيم الفيديو إلى clips صغيرة كل 30 ثانية
        clip_folder = os.path.join(app.config['UPLOAD_FOLDER'], "clips")
        os.makedirs(clip_folder, exist_ok=True)
        cmd = f'ffmpeg -i "{filepath}" -c copy -map 0 -segment_time 30 -f segment "{clip_folder}/clip%03d.mp4"'
        subprocess.call(cmd, shell=True)
        
        clips = os.listdir(clip_folder)
        clips = [f"uploads/clips/{c}" for c in clips]
        return render_template("index.html", clips=clips)

    return render_template("index.html", clips=[])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)