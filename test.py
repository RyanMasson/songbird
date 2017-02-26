import yin
import numpy as np
import librosa
import math
from scipy.io.wavfile import write



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

# print yin.get_pitch(test_buf3[0:1024], 0.0005, sr)

length = halo.shape[0]
print length
segment_size = 1024
num_segs = int(math.floor(float(length)/ segment_size))
print num_segs

rec_song = np.empty(0)
for i in np.arange(0,num_segs):
    pitch = yin.get_pitch(halo[i*segment_size: (i+1)*segment_size], 0.2, sr)
    if pitch < 0 or pitch > 5000:
        pitch = 0

    recreation = make_sinewave(pitch, 0.02322, sr)
    rec_song = np.concatenate((rec_song, recreation))

scaled = np.int16(rec_song/np.max(np.abs(rec_song)) * 32767)
write('sound_samples/halo_tracked.wav', 44100, scaled)