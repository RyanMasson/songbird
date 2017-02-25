import yin
import numpy as np
import librosa

# test comment

def make_sinewave(f, t, sr):
    """
    Parameters
    ----------
    f:  float
        Frequency of sine wave
    t:  float
        Duration in seconds
    sr: int
        Sample rate

    Returns
    -------
    np.ndarray
        Array of floats containing the signal
    """
    t = np.arange(0, t * sr) / sr
    x = np.sin(2 * np.pi * f * t)
    return x


test_buf = np.random.rand(2048)
test_buf2 = np.ones(2048)
test_buf3 = make_sinewave(200, 1.0, 44100)

ypt = yin.pitch_tracker(2048, 0.05)
ypt.yin_difference(test_buf3)
ypt.yin_cmnd()
tau = ypt.yin_abs_threshold()
better_tau = ypt.yin_parabolic_interpolation(tau)
print better_tau
