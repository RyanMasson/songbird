# import yin
import numpy as np
import librosa
import math
from scipy.io.wavfile import write
import pitch_shifter
import time


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


# test_buf = np.random.rand(2048)
# test_buf2 = np.ones(2048)
# test_buf3 = make_sinewave(200, 1.0, 44100)
# test_buf4, sr = librosa.load("sound_samples/trumpet.wav")
halo, sr = librosa.load("sound_samples/halo.wav")
halo = halo[0:(10*22050)]
sr = 22050

print "starting performance timer"
start = time.time()
shifter = pitch_shifter.pitch_shifter(halo)
shifter.get_freqs(0.2)
end1 = time.time()
print 'find frequencies and mapping: ', str(end1 - start)
tuned_audio = shifter.shift_audio()
end2 = time.time()
print 'tune audio sample: ', str(end2 - end1)

scaled = np.int16(tuned_audio/np.max(np.abs(tuned_audio)) * 32767)
write('sound_samples/halo_tuned_new.wav', 22050, tuned_audio)
