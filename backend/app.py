from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../')
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file = request.files['audioFile']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return 'File uploaded successfully!'


if __name__ == '__main__':
    app.run(debug=True)