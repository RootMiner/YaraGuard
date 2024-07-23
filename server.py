import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template

# custom import
from scanners.YaraScanner import yaraScan
# from assets.fileHasher import fileHasher
# from scanners.VTscanner import virusTotalWeb
# from scanners.VTscanner import virusTotalAPI


class Outpost:
    def __init__(self): 
        self.outposts = []
    def add_outpost(self, print_statement):
        self.outposts.append(print_statement)

execute_outposts = Outpost()


def scanYara(file_path):
    global isYara
    isYara = False
    isYara = yaraScan(file_path)
    if isYara:
        execute_outposts.add_outpost("|| MALWARE DETECTED -- By YARA RULE")


# def scanVTotal(malfile_path):
#     global isVT
#     isVT = False
#     file_hash = fileHasher(malfile_path)
#     # use one at a time, cause api gives rate limit and web gives captha block
#     isVT = virusTotalWeb(file_hash)
#     # isVT = virusTotalAPI(file_hash)

#     if isVT:
#         execute_outposts.add_outpost("|| MALWARE DETECTED  -- By VIRUS TOTAL")

UPLOAD_FOLDER   = './uploads/'
TEMPLATE_FOLDER = './template/'

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/', methods=['GET','POST'])
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
                # scanVTotal("." + malfile_path)
                os.remove("." + malfile_path)

            if isYara == False:
                execute_outposts.outposts.clear()
                execute_outposts.add_outpost("|| NO MALWARE DETECTED ||")

    except:
        if not execute_outposts.outposts:
            execute_outposts.outposts.clear()
            execute_outposts.add_outpost("[!] PLEASE SELECT A FILE TO UPLOAD ")

    return render_template('index.html', output=execute_outposts.outposts)


if __name__ == '__main__': 
    app.secret_key = 'test_key'
    app.run(host='0.0.0.0', debug=True)
