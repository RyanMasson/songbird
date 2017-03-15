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
a440_funds =  [3951.07,
                        3729.31,
                        3520,
                        3322.44,
                        3135.96,
                        2959.96,
                        2793.83,
                        2637.02,
                        2489.02,
                        2349.32,
                        2217.46,
                        2093,
                        1975.53,
                        1864.66,
                        1760,
                        1661.22,
                        1567.98,
                        1479.98,
                        1396.91,
                        1318.51,
                        1244.51,
                        1174.66,
                        1108.73,
                        1046.5,
                        987.767,
                        932.328,
                        880,
                        830.609,
                        783.991,
                        739.989,
                        698.456,
                        659.255,
                        622.254,
                        587.33,
                        554.365,
                        523.251,
                        493.883,
                        466.164,
                        440,
                        415.305,
                        391.995,
                        369.994,
                        349.228,
                        329.628,
                        311.127,
                        293.665,
                        277.183,
                        261.626,
                        246.942,
                        233.082,
                        220,
                        207.652,
                        195.998,
                        184.997,
                        174.614,
                        164.814,
                        155.563,
                        146.832,
                        138.591,
                        130.813,
                        123.471,
                        116.541,
                        110,
                        103.826,
                        97.9989,
                        92.4986,
                        87.3071,
                        82.4069,
                        77.7817,
                        73.4162,
                        69.2957,
                        65.4064,
                        61.7354,
                        58.2705,
                        55,
                        51.9131,
                        48.9994,
                        46.2493,
                        43.6535,
                        41.2034,
                        38.8909,
                        36.7081,
                        34.6478,
                        32.7032,
                        30.8677,
                        29.1352,
                        27.5,
                        25.9565]
absurd_funds =  [3951.07,
                        3135.96,
                        2489.02,
                        1975.53,
                        1567.98,
                        1244.51,
                        987.767,
                        783.991,
                        622.254,
                        493.883,
                        391.995,
                        311.127,
                        246.942,
                        195.998,
                        155.563,
                        123.471,
                        97.9989,
                        77.7817,
                        61.7354,
                        48.9994,
                        38.8909,
                        30.8677]
absurd_funds_low = [350, 300, 250, 200, 150, 100, 50]

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
def test(path, tuning_system):
    aud = librosa.load(path)[0]
    sr = 22050
    threshold = 0.2
    shifter = pitch_shifter.pitch_shifter(aud, max_freq=350, fundamentals=tuning_system)
    shifter.get_freqs(threshold)
    tuned_audio = shifter.shift_audio()
    tuned_audio = np.int16(tuned_audio/np.max(np.abs(tuned_audio)) * 32767)
    write(path, 22050, tuned_audio)