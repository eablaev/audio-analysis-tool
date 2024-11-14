import numpy as np
import essentia.standard as es

from flask import Flask, request, jsonify, render_template
from io import BytesIO
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)

def find_BPM(audio):
    #low-pass filter to focus on low end kick info
    low_pass_filter = es.LowPass(cutoffFrequency=300.0)  # Adjust cutoff frequency as needed
    audio_filtered = low_pass_filter(audio)

    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm, confidence, _, _, _ = rhythm_extractor(audio_filtered)

    #if bpm is an array take the first element
    if isinstance(bpm, np.ndarray):
        for value in bpm:
            print(f'values:${value}')
        bpm_value = bpm[0]
    else:
        print('else')
        bpm_value = bpm

    # if confidence is an array and take the first element
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
    # low-pass filter to remove high-frequency noise 
    low_pass_filter = es.LowPass(cutoffFrequency=3000.0)  # Adjust cutoff frequency as needed
    audio_filtered = low_pass_filter(audio)
    key_extractor = es.KeyExtractor()
    key, scale, confidence = key_extractor(audio_filtered)

    print(f'Key is: {key}, Scale is: {scale}, Confidence: {confidence:.2f}')
    return key, scale
import tempfile

def analyze_audio(file_stream):
    # Create a temporary file from the in-memory audio stream
    with tempfile.NamedTemporaryFile(suffix='.wav') as temp_audio_file:
        temp_audio_file.write(file_stream.getvalue())
        temp_audio_file.flush()  # Ensure data is written

        # creating an instance of MonoLoader
         # allows the MonoLoader instance to access and load the audio data 
        # from that file when you call it later with audio = loader().
        loader = es.MonoLoader(filename=temp_audio_file.name)
        audio = loader()

        # Normalize audio for consistency
        audio = audio / np.max(np.abs(audio))  # Normalize to [-1, 1]
        tempo = find_BPM(audio)
        root, scale = find_Key(audio)

    # Return tempo and key as a formatted string
    key = f'{root} {scale}'
    return tempo, key



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



    # Check if the uploaded file is of a valid type
    if file.filename.endswith(('.mp3', '.wav', '.aac', '.flac','.m4a')):
        filename = secure_filename(file.filename)  # Sanitize the filename
        file_stream = BytesIO(file.read())  # Read the file into memory as a stream
        tempo, key_name = analyze_audio(file_stream)
        return jsonify({'tempo': tempo, 'key': key_name, 'filename': filename})
    else:
        return 'Invalid file type. Please upload an audio file.', 400  # Invalid file type response

if __name__ == '__main__':
    app.run(debug=True)

