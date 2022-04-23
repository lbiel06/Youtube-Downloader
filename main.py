from flask import Flask, render_template, request, send_file
import subprocess
import time


def download_video(url: str, file: str, path: str) -> bool:
    try:
        subprocess.check_output(['yt-dlp', '-P', path, '-o', file, url])
        return True
    except subprocess.CalledProcessError:
        return False


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

    else:
        url = request.form.get('url')
        if not url:
            return 'ERROR'

        unique_string = str(time.time()).replace('.', '_')
        filename = f'video_{unique_string}.mp4'
        path = f'videos/{filename}'
        # print(url, filename, path)

        if download_video(url, filename, 'videos'):
            return send_file(path, as_attachment=True)
        return render_template('home.html', message='is-invalid')


if __name__ == '__main__':
    app.run()