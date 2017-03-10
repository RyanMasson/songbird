from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, send_from_directory
import librosa
from scipy.io.wavfile import write
import numpy as np
from werkzeug.utils import secure_filename
import os
import sys
from songbird import app, wavs

backend = Blueprint('backend', __name__)

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
            test(wavs.path(filename))
            return wavs.url(filename)

    return

'''
Test function that will slow down the given wav file at the given path
'''
def test(path):
    aud = librosa.load(path)[0]
    sig = librosa.effects.time_stretch(aud, 0.5)
    write(path, 22050, sig)