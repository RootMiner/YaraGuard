import os
import yara
from sys import argv
from rich import print
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

def scan(file_to_scan):
    try:
        a = 0
        dir_name = './rules/'

        for file in os.listdir(dir_name):
                file_path = dir_name + file

                rules = yara.compile(filepath=file_path)

                matches = rules.match(file_to_scan)

                if matches and a == 0:
                    render_template('index.html', console_output='malware detected')
                    # print("\n\n[bold red]       ||>>> Malware Detected <<<||[/bold red]\n\n")
                    render_template('index.html', console_output='malware detected')
                    # print(f"[bold red][+][/bold red] the file [bold green]{file_to_scan}[/bold green] matches the [bold cyan]Yara rules[/bold cyan]:")
                    a = 1
                if matches:
                    for match in matches:
                        render_template('index.html', console_output='malware detected')
                        # print(f"- Rule: [bold yellow]{match.rule}[/bold yellow]")
                        
        if a == 0:
            render_template('index.html', console_output='no malware detected')
            # print("\n\n[bold green]       ||>>> No Malware Detected <<<||[/bold green]\n\n")
    except:
        print("[bold red][*]something went wrong![/bold red] \n\n[bold green]python3[/bold green] [bold yellow]scan.py[/bold yellow] [bold cyan]{file to scan}[/bold cyan]")


UPLOAD_FOLDER = './uploads/'

app = Flask(__name__, template_folder='./')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            malfile_path = url_for('download_file', name=filename)
            scan("." + malfile_path)
            os.remove("." + malfile_path)

    return render_template('index.html')



if __name__ == '__main__':
    app.run(host="localhost", port=8000)