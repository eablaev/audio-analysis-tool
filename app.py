from flask import Flask, request, jsonify, render_template
import os
import librosa
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import numpy as np


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')  # Corrected path inside static folder



def analyze_audio(file_path):
    y, sr = librosa.load(file_path)

    spectrum = librosa.feature.melspectrogram(y=y, sr=sr)
    db_spectrum = librosa.amplitude_to_db(spectrum, ref=np.max)

     # Visualize the Mel spectrogram
    plt.figure(figsize=(10, 4))
    plt.imshow(db_spectrum, aspect='auto', origin='lower')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Mel Frequency')
    
    # Show the plot
   # Save the plot to a file instead of showing it
    plot_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'mel_spectrogram.png')
    print(plot_filename)
    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.close()  # Close the plot to free up memory


    return db_spectrum, plot_filename 




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded file
    file = request.files.get('audioFile')  # Using get to safely access the file
    
    # Check if a file was uploaded
    if not file:
        return 'No file part', 400  # Return if no file part found in the request

    # Check if the filename is empty
    if file.filename == '':
        return 'No selected file', 400  # Return if no file was selected

    # Create the upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Check if the uploaded file is of a valid type
    if file.filename.endswith(('.mp3', '.wav')):
        filename = secure_filename(file.filename)  # Sanitize the filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        db_spectrum, plot_filename = analyze_audio(file_path)
        return render_template('index.html', plot_filename=plot_filename)
    else:
        return 'Invalid file type. Please upload an MP3 or WAV file.', 400  # Invalid file type response

if __name__ == '__main__':
    app.run(debug=True)
