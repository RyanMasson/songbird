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
q_tones_funds = [4066.84, 3951.07, 3838.59, 3729.31, 3623.14,
                 3520.00, 3419.79, 3322.44, 3227.85, 3135.96,
                 3046.69, 2959.96, 2875.69, 2793.83, 2714.29,
                 2637.02, 2561.95, 2489.02, 2418.16, 2349.32,
                 2282.44, 2217.46, 2154.33, 2093.00, 2033.42,
                 1975.53, 1919.29, 1864.66, 1811.57, 1760.00,
                 1709.90, 1661.22, 1613.93, 1567.98, 1523.34,
                 1479.98, 1437.85, 1396.91, 1357.15, 1318.51,
                 1280.97, 1244.51, 1209.08, 1174.66, 1141.22,
                 1108.73, 1077.17, 1046.50, 1016.71, 987.77,
                 959.65, 932.33, 905.79, 880.0, 854.95, 830.61,
                 806.96, 783.99, 761.67, 739.99, 718.92, 698.46,
                 678.57,659.46, 678.57, 659.26, 640.49, 622.25,
                 604.54, 587.33, 570.61, 554.37, 538.58, 523.25,
                 508.36, 493.88, 479.82, 466.16, 452.89, 440.0,
                 427.47, 415.30, 403.48, 392.00, 380.84, 369.99,
                 359.46, 349.23, 339.29, 320.24, 311.13, 302.27,
                 293.66, 285.30, 277.18, 269.29, 261.63, 254.18,
                 246.94, 239.91, 233.08, 226.45, 220.00, 213.74,
                 207.65, 201.74, 196.00, 190.42, 185.00, 179.73,
                 174.61, 169.64, 164.81, 160.12, 155.56, 151.13,
                 146.83, 142.65, 138.59, 134.65, 130.81, 127.09,
                 123.47, 119.96, 116.54, 113.22, 110.00, 106.87,
                 103.83, 100.87, 98.00, 95.21, 92.50, 89.87, 87.31,
                 84.82, 82.41, 80.06, 77.78, 75.78, 75.57, 73.42, 71.33,
                 69.30, 67.32, 65.41, 63.54, 61.74, 59.98, 58.27, 56.61,
                 55.00, 53.43, 51.91, 50.44, 49.00, 47.60, 46.25, 44.93,
                 43.65, 42.41, 41.20, 40.03, 38.89, 37.78, 36.71, 35.66,
                 34.65, 33.66, 32.70, 31.77, 30.87, 29.99, 29.14, 28.31,
                 27.50, 26.72, 25.96, 25.22, 24.50, 23.80, 23.12, 22.47,
                 21.83, 21.21]
absurd_funds_low = [950, 850, 750, 650, 550,
                    450, 350, 250, 150, 50]

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
            return wavs.url(test(wavs.path(filename), absurd_funds_low))
            # return wavs.url(filename)

    return

'''
Test function that will slow down the given wav file at the given path
'''
def test(path, tuning_system):
    aud = librosa.load(path)[0]
    sr = 22050
    threshold = 0.2
    shifter = pitch_shifter.pitch_shifter(aud, tuning_system, window_size=4096, max_freq=1024)
    shifter.get_freqs(threshold)
    tuned_audio = shifter.shift_audio()
    tuned_audio = np.int16(tuned_audio/np.max(np.abs(tuned_audio)) * 32767)
    filename, file_extension = os.path.splitext(path)
    filepath = filename + '_new' + file_extension
    write(filepath, 22050, tuned_audio)
    return os.path.basename(filepath)