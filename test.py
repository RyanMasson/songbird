# import yin
import numpy as np
import librosa
import math
from scipy.io.wavfile import write
import pitch_shifter



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
test_buf4, sr = librosa.load("sound_samples/trumpet.wav")
halo, sr = librosa.load("sound_samples/halo.wav")
halo = halo[0:330750]
sr = 44100


shifter = pitch_shifter.pitch_shifter(halo)
intended_freqs, tuned_freqs = shifter.get_freqs(0.2)
tuned_audio = shifter.shift_audio()

scaled = np.int16(tuned_audio/np.max(np.abs(tuned_audio)) * 32767)
write('sound_samples/halo_tuned_new.wav', 22050, tuned_audio)