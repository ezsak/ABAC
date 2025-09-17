from flask import Flask, render_template, request, send_from_directory
import os
import shutil
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ACCESS_CONTROL_FOLDER = 'access_control'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.json')
        file.save(input_path)

        # Step 1: Convert input.json to config.ini
        try:
            subprocess.run(['python3', os.path.join(ACCESS_CONTROL_FOLDER, 'input.py')], check=True)
        except subprocess.CalledProcessError:
            return "Error: Failed to process input.json with input.py.", 500

        # Step 2: Run gen.py to generate outputs
        try:
            subprocess.run(['python3', os.path.join(ACCESS_CONTROL_FOLDER, 'gen.py')], check=True)
        except subprocess.CalledProcessError:
            return "Error: Failed to generate outputs with gen.py.", 500

        return "Files generated successfully! <a href='/download'>Download Outputs</a>"
    
@app.route('/download')
def download_outputs():
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.json')
    if not os.path.exists(file_path):
        return "Error: output.json not found. Ensure the process completed successfully.", 404
    return send_from_directory(app.config['OUTPUT_FOLDER'], 'output.json')

if __name__ == '__main__':
    app.run(debug=True)