# Implementation of Yin Algorithm for Pitch Tracking
# 02/25/2017
import numpy as np
import librosa
# import scipy


class pitch_tracker:

    def __init__(self, buffer_size, threshold):

        self.buffer_size = buffer_size
        self.half_buffer_size = buffer_size / 2
        self.threshold = threshold
        self.probability = 0.0

        self.yin_buffer = np.zeros(self.half_buffer_size)

    def yin_difference(self, sig_buffer):
        '''
        Step 1: Calculates the squared difference of the signal with
        shifted version of itself.
        :param buffer: buffer of samples to analyse
        :return: None
        '''
        for tau in np.arange(self.half_buffer_size):
            for i in np.arange(self.half_buffer_size):
                delta = sig_buffer[i] - sig_buffer[i + tau]
                self.yin_buffer[tau] += delta * delta


    def yin_cmnd(self):
        '''s
        Step 2: Calculate the cumulative mean on the normalized difference
        calculated in step one. "Finds" which tau (shift) value produces
        the smallest difference.
        :return: None
        '''
        running_sum = 0.0
        self.yin_buffer[0] = 1

        for tau in np.arange(self.half_buffer_size):
            running_sum += self.yin_buffer[tau]
            self.yin_buffer[tau] *= tau / running_sum


    def yin_abs_threshold(self):
        '''
        Step 3: Search through normalized cumulative mean array
        and find values that are over the threshold.
        :return: Shift (tau) with best estimated autocorellation. -1 if
            no suitable value found over threshold.
        '''

        # Find values in cmnd that exceed threshold
        # Start at index 2 since first two elements always exceed threshold
        tau = 2
        while tau < self.half_buffer_size:

            if self.yin_buffer[tau] < self.threshold:

                while (tau + 1 < self.half_buffer_size) and (self.yin_buffer[tau + 1] < self.yin_buffer[tau]):
                    tau += 1

                self.probability = 1 - self.yin_buffer[tau]
                break
            tau += 1

        if (tau == self.half_buffer_size) or (self.yin_buffer[tau] >= self.threshold):
            tau = -1
            self.probability = 0

        return tau

    def yin_parabolic_interpolation(self, tau_estimate):
        '''
        Step 5: Interpolate the shift value (tau) to improve pitch estimate.
        :param tau_estimate: tau value with best estimate of autocorrelation
        :return: None
        '''

        x0 = 0
        x2 = 0

        # First polynomial coefficient
        if tau_estimate < 1:
            x0 = tau_estimate
        else:
            x0 = tau_estimate - 1

        # Second polynomial coefficient
        if tau_estimate + 1 < self.half_buffer_size:
            x2 = tau_estimate + 1
        else:
            x2 = tau_estimate

        # Algorithm to parabolically interpolate shift value tau to better estimate
        if x0 == tau_estimate:
            if self.yin_buffer[tau_estimate] <= self.yin_buffer[x2]:
                better_tau = tau_estimate
            else:
                better_tau = x2
        elif x2 == tau_estimate:
            if self.yin_buffer[tau_estimate] <= self.yin_buffer[x0]:
                better_tau = tau_estimate
            else:
                better_tau = x0
        else:
            s0 = self.yin_buffer[x0]
            s1 = self.yin_buffer[tau_estimate]
            s2 = self.yin_buffer[x2]
            better_tau = tau_estimate + (s2 - s0) / (2 * (2 * s1- s2 - s0))

        return better_tau