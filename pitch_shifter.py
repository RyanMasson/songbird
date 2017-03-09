# Class that
import numpy as np
import yin
import math
import librosa

class pitch_shifter:

    fundamentals = [3951.07,
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

    def __init__(self, raw_audio, window_size=1024, sr = 44100, fundamentals = fundamentals):
        self.fundamentals = fundamentals.reverse()
        num_notes = len(fundamentals)
        # Tuning boundaries based on fundamentals
        # Used to categorize intended frequencies to tuned counterpart
        # Test frequency 27.0 Hz should map to 27.5 (index 1 in the fundamentals array).
        # The first boundary that the test frequency is greater than (26.728 Hz, index 1 in the boundary array)
        # So the proper assignment for the test frequency is the value at index 1 in fundamentals array.
        boundaries = [(fundamentals[i - 1] + fundamentals[i]) / 2 for i in range(1, num_notes)]
        boundaries.insert(0, 20)  # 20 is lower bound of tolerable frequencies
        boundaries.insert(num_notes, 4100)  # 4100 is upper bound of tolerable frequencies
        self.boundaries = boundaries

        self.sr = sr
        self.raw_audio = raw_audio
        self.window_size = window_size
        no_samples = self.raw_audio.shape[0]
        self.num_windows = int(math.floor(float(no_samples) / window_size))

    def get_freqs(self, threshold):
        '''
        Using the audio given to class, find intended pitch values and return "tuned" pitch values
        :param threshold: ??? TODO
        :param sr: int representing sample rate
        :return: (array of intended fundamental frequencies, array of "tuned" fundamental frequencies)
        '''

        intended_fund_freqs = np.empty(0)
        tuned_fund_freqs = np.empty(0)

        for i in np.arange(0, self.num_windows):

            freq = yin.get_pitch(self.raw_audio[i * self.window_size: (i + 1) * self.window_size], threshold, self.sr)

            if pitch < 0 or pitch > 5000:
                pitch = 0
            intended_fund_freqs = np.append(intended_fund_freqs, freq)

            tf_idx = next(idx for idx, value in enumerate(self.boundaries) if value > pitch)

            tuned_fund_freqs = np.append(tuned_fund_freqs, self.fundamentals[tf_idx])

        self.intended_fund_freqs = intended_fund_freqs
        self.tuned_fund_freqs = tuned_fund_freqs

        return (intended_fund_freqs, tuned_fund_freqs)

    def half_steps_between(self, f1, f2, system="eq-temp"):
        if system == "eq-temp":
            n_half_steps = 12*math.log((f2/f1),2)
        return n_half_steps

    def shift_audio(self):
        self.tuned_audio = np.zeros(len(self.raw_audio))

        for i in np.arange(0, self.num_windows):

            n_half_steps = self.half_steps_between(self.intended_fund_freqs[i], self.tuned_fund_freqs)
            start = i * self.window_size
            end = (i + 1) * self.window_size
            self.tuned_audio[start:end] = librosa.effects.pitch_shift(self.raw_audio[start:end], self.sr, n_steps = n_half_steps)

        return self.tuned_audio
