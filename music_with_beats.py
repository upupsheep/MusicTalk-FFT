import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile  # get the api
import librosa
import librosa.display  # Display click waveform
import numpy as np
import math
import os.path

filepath = 'night.wav'
filename = filepath[:-4]
fs, data = wavfile.read(filepath)  # load the data, fs samples/sec
firstTrack_data = data.T[
    0]  # two channel soundtrack, get the first track by transpose
music_length = math.floor(len(data) / fs)
# print(music_length)

N = fs
# time_probe = 0
outputFile = filename + '.txt'

# 1. Get the file path to the included audio example
# Sonify detected beat events
y, sr = librosa.load(filepath)

tempo, beats = librosa.beat.beat_track(y=y, sr=sr)  # tempo: BPM

# Use timing instead of frame indices
times = librosa.frames_to_time(beats, sr=sr)

if os.path.isfile(outputFile) == False:
    fo = open(outputFile, 'w')

    last_time = 0
    for time_probe in times:
        beats_window = time_probe - last_time
        N = int(beats_window * fs)
        # N = 44100
        start = int(time_probe * N)  # starting point of sampling
        print("N: ", N)
        print("beats_window: ", beats_window)
        print("time_probe: ", time_probe)
        print("last_time, ", last_time)
        df = 1.0 / beats_window  # usr sampling rate
        freq = [df * n for n in range(0, N)]  # N element
        data_window = firstTrack_data[start:start + N]
        # c = fft(data_window) * 2 / (N)
        c = fft(data_window)
        # symmetry, only need to show half
        dd = int(len(c) / 2)
        # only frequency <= 5000Hz will be showed
        while freq[dd] > 5000:
            dd -= 10
        # update time probe
        last_time = time_probe

        # max amplitude of all frequency
        max_amplitude = max(abs(c[:dd - 1]))
        # frequency of that max amplitude
        max_freq = np.argmax(abs(c[:dd - 1]))
        print("time: ")
        print(time_probe)
        print(max_amplitude)
        print(max_freq)
        print(freq[max_freq])
        # write out to [filepath].txt
        fo.writelines(
            str(time_probe) + "," + str(max_amplitude) + "," + str(max_freq) +
            "\n")
        # time_probe = time_probe + 1

    fo.close()
