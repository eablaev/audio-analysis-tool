import numpy as np
import essentia.standard as es

from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')  # Corrected path inside static folder


def find_BPM(audio):
    # Apply a low-pass filter to remove high-frequency noise (optional)
    low_pass_filter = es.LowPass(cutoffFrequency=300.0)  # Adjust cutoff frequency as needed
    audio_filtered = low_pass_filter(audio)

    # Rhythm extractor
    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm, confidence, _, _, _ = rhythm_extractor(audio_filtered)

    # Check if bpm is an array and take the first element
    if isinstance(bpm, np.ndarray):
        for value in bpm:
            print(f'values:${value}')
        bpm_value = bpm[0]
    else:
        bpm_value = bpm

    # Check if confidence is an array and take the first element
    if isinstance(confidence, np.ndarray):
        confidence_value = confidence[0]
    else:
        confidence_value = confidence

    # Print the estimated BPM and confidence, along with a warning if confidence is low
    if confidence_value < 0.5:  # Adjust threshold as necessary
        print(f"Warning: Low confidence in BPM estimation: {confidence_value:.2f}")

    print(f"Estimated BPM: {bpm_value:.2f}, Confidence: {confidence_value:.2f}")
    return bpm_value

def find_Key(audio):
    # Apply a low-pass filter to remove high-frequency noise (optional)
    low_pass_filter = es.LowPass(cutoffFrequency=600.0)  # Adjust cutoff frequency as needed
    audio_filtered = low_pass_filter(audio)
    key_extractor = es.KeyExtractor()
    key, scale, confidence = key_extractor(audio_filtered)

    print(f'Key is: {key}, Scale is: {scale}, Confidence: {confidence:.2f}')
    return key, scale

def analyze_audio(file_path):
    # Load the audio file
    loader = es.MonoLoader(filename=file_path)
    audio = loader()

    # Optional: Normalize the audio to improve consistency
    audio = audio / np.max(np.abs(audio))  # Normalize to [-1, 1]
    tempo = find_BPM(audio)
    root, scale = find_Key(audio)

    key = f'{root} {scale}'

    return tempo, key

    

# # Test the function with an audio file
# file_path = 'static/uploads/96.mp3'
# bpm, key = analyze_audio(file_path)
# print("Detected BPM:", round(bpm))
# print("Detected Key:", key)


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
        tempo, key_name = analyze_audio(file_path)
        return render_template('index.html', tempo=tempo, key=key_name)
    else:
        return 'Invalid file type. Please upload an MP3 or WAV file.', 400  # Invalid file type response

if __name__ == '__main__':
    app.run(debug=True)

