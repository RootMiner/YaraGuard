import os
from assets.fileHasher import fileHasher
from werkzeug.utils import secure_filename
from scanners.YaraScanner import yaraScan
from scanners.VTscanner import virusTotalWeb
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template


class Outpost:
    def __init__(self): self.outposts = []

    def add_outpost(self, print_statement):
        self.outposts.append(print_statement)


execute_outposts = Outpost()


def scanYara(file_path):
    global isYara
    isYara = False
    isYara = yaraScan(file_path)
    if isYara:
        execute_outposts.add_outpost(
            "|| MALWARE DETECTED || ---- By YARA RULE ||")


def scanVTotal(malfile_path):
    global isVT
    isVT = False
    file_hash = fileHasher(malfile_path)
    isVT = virusTotalWeb(file_hash)
    if isVT:
        execute_outposts.add_outpost(
            "|| MALWARE DETECTED  || ---- By VIRUS TOTAL ||")


UPLOAD_FOLDER = './uploads/'

app = Flask(__name__, template_folder='./')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:

        if request.method == 'POST':

            execute_outposts.outposts.clear()

            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                global malfile_path
                malfile_path = url_for('download_file', name=filename)
                scanYara("." + malfile_path)
                scanVTotal("." + malfile_path)
                os.remove("." + malfile_path)

            print(isVT, isYara)

            if isVT == False:
                execute_outposts.outposts.clear()
                execute_outposts.add_outpost("|| MALWARE NOT DETECTED ||")


    except:
        if not execute_outposts.outposts:
            execute_outposts.outposts.clear()
            execute_outposts.add_outpost("[!] SOMETHING WENT WRONG ")

    return render_template('index.html', output=execute_outposts.outposts)


if __name__ == '__main__':
    app.run(host="localhost", port=8000)
