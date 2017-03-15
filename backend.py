from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, send_from_directory
import librosa
from scipy.io.wavfile import write
import numpy as np
from werkzeug.utils import secure_filename
import os
import sys
from songbird import app, wavs
import pitch_shifter

backend = Blueprint('backend', __name__)

@backend.route('/_deletewavs', methods=['GET'])
def delete_files():
    path = os.path.join(app.root_path, 'static/uploads/wavs/')
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    return ''

@backend.route('/_uploadandsongify', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = wavs.save(file)
            # test(wavs.path(filename))
            return wavs.url(filename)

    return

'''
Test function that will slow down the given wav file at the given path
'''
def test(path):
    aud = librosa.load(path)[0]
    sr = 22050
    threshold = 0.2
    shifter = pitch_shifter.pitch_shifter(aud)
    shifter.get_freqs(threshold)
    tuned_audio = shifter.shift_audio()
    tuned_audio = np.int16(tuned_audio/np.max(np.abs(tuned_audio)) * 32767)
    write(path, 22050, tuned_audio)