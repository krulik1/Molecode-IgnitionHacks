from flask import Flask, request, render_template, send_from_directory
import os
from proteinLoadModel import predict
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Create all the folders for file storage:
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PROCESSED_FOLDER = os.path.join(os.getcwd(), 'processed')
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

# Create the web app:
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    processed_files = {filename: open(os.path.join(app.config['PROCESSED_FOLDER'], filename)).read() for filename in os.listdir(app.config['PROCESSED_FOLDER'])}
    return render_template('index.html', files=uploaded_files, processed_files=processed_files)

# upload files
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
        processed_files = {filename: open(os.path.join(app.config['PROCESSED_FOLDER'], filename)).read() for filename in os.listdir(app.config['PROCESSED_FOLDER'])}
        return render_template('index.html', files=uploaded_files, processed_files=processed_files)
    
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True)
    else:
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
        processed_files = {filename: open(os.path.join(app.config['PROCESSED_FOLDER'], filename)).read() for filename in os.listdir(app.config['PROCESSED_FOLDER'])}
        return render_template('index.html', files=uploaded_files, processed_files=processed_files, message='File not found')


# delete files
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
        processed_files = {filename: open(os.path.join(app.config['PROCESSED_FOLDER'], filename)).read() for filename in os.listdir(app.config['PROCESSED_FOLDER'])}
        return render_template('index.html', files=uploaded_files, processed_files=processed_files, message='File deleted')
    else:
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
        processed_files = {filename: open(os.path.join(app.config['PROCESSED_FOLDER'], filename)).read() for filename in os.listdir(app.config['PROCESSED_FOLDER'])}
        return render_template('index.html', files=uploaded_files, processed_files=processed_files, message='File not found')

@app.route('/delete_processed/<filename>', methods=['POST'])
def delete_processed_file(filename):
    file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
        processed_files = {filename: open(os.path.join(app.config['PROCESSED_FOLDER'], filename)).read() for filename in os.listdir(app.config['PROCESSED_FOLDER']) if filename.endswith('.txt')}
        return render_template('index.html', files=uploaded_files, processed_files=processed_files, message='File deleted')
    else:
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
        processed_files = {filename: open(os.path.join(app.config['PROCESSED_FOLDER'], filename)).read() for filename in os.listdir(app.config['PROCESSED_FOLDER']) if filename.endswith('.txt')}
        return render_template('index.html', files=uploaded_files, processed_files=processed_files, message='File not found')

# submit files into function of interest
@app.route('/process/<filename>', methods=['POST'])
@app.route('/process/<filename>', methods=['POST'])
def process_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        accuracy_percentage = fun(file_path)
        # Write the accuracy to a new file in the PROCESSED_FOLDER
        with open(os.path.join(app.config['PROCESSED_FOLDER'], filename + '.txt'), 'w') as f:
            f.write(f'There is a: {accuracy_percentage}% accuracy that your protein degrades cholesterol.')
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
        processed_files = {filename: open(os.path.join(app.config['PROCESSED_FOLDER'], filename)).read() for filename in os.listdir(app.config['PROCESSED_FOLDER']) if filename.endswith('.txt')}
        return render_template('index.html', files=uploaded_files, processed_files=processed_files, message=f'File processed with accuracy: {accuracy_percentage}%')
    else:
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
        processed_files = {filename: open(os.path.join(app.config['PROCESSED_FOLDER'], filename)).read() for filename in os.listdir(app.config['PROCESSED_FOLDER']) if filename.endswith('.txt')}
        return render_template('index.html', files=uploaded_files, processed_files=processed_files, message='File not found')
## NOTE, this portion of the code will connect to the machine learning model, currently placeholder
def fun(file_path):
    #Converts a fasta with a string of AAs into a csv of hydrophobicity values

    out = 100*predict(file_path)[0][0] # extract prediction value from 
    out = round(out, 2)

    return out


# run the web app
if __name__ == '__main__':
    app.run()
