from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import shutil
import subprocess
import zipfile
import json
from access_control.plot_analyzer import analyze_plot

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
@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    if 'zipfile' not in request.files:
        return "No file part", 400
    zipfile_obj = request.files['zipfile']
    if zipfile_obj.filename == '':
        return "No selected file", 400

    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_images.zip')
    zipfile_obj.save(zip_path)

    # Extract the zip file
    extracted_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_images')
    if os.path.exists(extracted_folder):
        shutil.rmtree(extracted_folder)
    os.makedirs(extracted_folder, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)

    preprocessing_data = {}
    final_output_data = {}

    # ✅ Recursive scan for images
    for root, dirs, files in os.walk(extracted_folder):
        for image_name in files:
            image_path = os.path.join(root, image_name)
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"\n📊 Processing image: {image_path}")
                analyze_plot(image_path, preprocessing_data, final_output_data)
                print("📥 After analyze_plot:", preprocessing_data, final_output_data)
            else:
                print(f"⚠️ Skipping non-image file: {image_name}")

    preprocessing_json_path = os.path.join(ACCESS_CONTROL_FOLDER, 'preprocessing.json')
    final_output_json_path = os.path.join(ACCESS_CONTROL_FOLDER, 'final_output.json')

    with open(preprocessing_json_path, 'w') as f:
        json.dump(preprocessing_data, f, indent=4)

    with open(final_output_json_path, 'w') as f:
        json.dump(final_output_data, f, indent=4)

    print("\n✅ Preprocessing Data:")
    print(json.dumps(preprocessing_data, indent=4))
    print("\n✅ Final Output Data:")
    print(json.dumps(final_output_data, indent=4))

    return jsonify({
        "message": "Analysis complete!",
        "preprocessing": preprocessing_data,
        "final_output": final_output_data
    })

@app.route('/download')
def download_outputs():
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.json')
    if not os.path.exists(file_path):
        return "Error: output.json not found. Ensure the process completed successfully.", 404
    return send_from_directory(app.config['OUTPUT_FOLDER'], 'output.json')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)




