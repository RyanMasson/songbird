# Class that
import numpy as np
import yin
import math
import librosa

class pitch_shifter:

    def __init__(self, raw_audio, fundamentals, window_size=4096, sr = 22050, max_freq=350):

        # if system != "eq-temp":
        #     raise ParameterError('Define other tuning system')

        self.fundamentals = fundamentals[::-1]
        num_notes = len(fundamentals)

        # Tuning boundaries based on fundamentals
        # Used to categorize intended frequencies to tuned counterpart
        # Test frequency 27.0 Hz should map to 27.5 (index 1 in the fundamentals array).
        # The first boundary that the test frequency is greater than (26.728 Hz, index 1 in the boundary array)
        # So the proper assignment for the test frequency is the value at index 1 in fundamentals array.
        boundaries = [(self.fundamentals[i - 1] + self.fundamentals[i]) / 2 for i in range(1, num_notes)]
        boundaries.insert(0, 20)  # 20 is lower bound of tolerable frequencies
        boundaries.insert(num_notes, 4100)  # 4100 is upper bound of tolerable frequencies
        self.boundaries = boundaries

        self.sr = sr
        self.raw_audio = raw_audio
        self.window_size = window_size
        self.no_samples = self.raw_audio.shape[0]
        dumm_nw = int(math.floor(float(self.no_samples) / window_size))
        print dumm_nw
        self.hop_size = window_size / 2
        self.num_windows = int(math.floor(float(self.no_samples) / self.hop_size)) - 1
        print self.num_windows

    def get_freqs(self, threshold):
        '''
        Using the audio given to class, find intended pitch values and return "tuned" pitch values
        :param threshold: ??? TODO
        :param sr: int representing sample rate
        :return: (array of intended fundamental frequencies, array of "tuned" fundamental frequencies)
        '''
        intended_fund_freqs = np.empty(self.num_windows)
        tuned_fund_freqs = np.empty(self.num_windows)

        st_pos = 0
        i = 0
        while st_pos < (self.no_samples - self.window_size):

            freq = yin.get_pitch(self.raw_audio[st_pos : st_pos + self.window_size], threshold, self.sr)

            if freq < 0 or freq > 5000:
                freq = 0
            intended_fund_freqs[i] = freq

            tf_idx = [idx for idx, bound in enumerate(self.boundaries) if freq < bound]
            if tf_idx == []:
                tf_idx = 0
            else:
                tf_idx = tf_idx[0]
            tuned_fund_freqs[i] = self.fundamentals[tf_idx - 1]

            st_pos = st_pos + self.hop_size
            i += 1

        self.intended_fund_freqs = intended_fund_freqs
        self.tuned_fund_freqs = tuned_fund_freqs

    def half_steps_between(self, f1, f2, system="eq-temp"):
        if system == "eq-temp":
            if f1 == 0:
                return 0
            n_half_steps = 12*math.log((f2/f1), 2)
        return n_half_steps

    def shift_audio(self):

        self.tuned_audio = np.zeros(len(self.raw_audio))

        st_pos = 0
        idx = 0
        while st_pos < (self.no_samples - self.window_size):

            n_half_steps = self.half_steps_between(self.intended_fund_freqs[idx], self.tuned_fund_freqs[idx])
            end_pos = st_pos + self.window_size
            windowed = self.raw_audio[st_pos:end_pos] * np.hanning(self.window_size)
            self.tuned_audio[st_pos:end_pos] = self.tuned_audio[st_pos:end_pos] +\
                                               librosa.effects.pitch_shift(windowed,
                                                                           self.sr,
                                                                           n_steps = n_half_steps)

            st_pos = st_pos + self.hop_size
            idx += 1


        return self.tuned_audio
