import os
import yara
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename


class Outpost:
    def __init__(self):
        self.outposts = ""
    def add_outpost(self, data):
        self.outposts = self.outposts + data

execute_outposts = Outpost()

def scan(file_to_scan):
    try:
        x = True
        dir_name = './rules/'

        execute_outposts.outposts = ""

        for file in os.listdir(dir_name):
            file_path = dir_name + file

            rules = yara.compile(filepath=file_path)

            matches = rules.match(file_to_scan)
            
            if matches and x == True:
                execute_outposts.add_outpost("||MALWARE DETECTED||")
                execute_outposts.add_outpost(f"[+] {file_to_scan} file scanned!")
                x = False
            if matches:
                for match in matches:
                    execute_outposts.add_outpost(f"- Rule: {match.rule}")
        
        if x == True:
            execute_outposts.outposts = ""
            execute_outposts.add_outpost("||NO MALWARE DETECTED||")

    except:
        execute_outposts.outposts = ""
        execute_outposts.add_outpost("[*] SOMETHING WENT WRONG...")


UPLOAD_FOLDER = './uploads/'

app = Flask(__name__, template_folder='./')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
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
            malfile_path = url_for('download_file', name=filename)
            scan("." + malfile_path)
            os.remove("." + malfile_path)

    return render_template('index.html', output=execute_outposts.outposts)

if __name__ == '__main__':
    app.run(host="localhost", port=8000)