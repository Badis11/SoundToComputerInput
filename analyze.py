import pyaudio
import wave
import numpy as np
from scipy.fft import *
from scipy.io import wavfile

def analyze():
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    def freq(file, start_time, end_time):

        # Open the file and convert to mono
        sr, data = wavfile.read(file)
        if data.ndim > 1:
            data = data[:, 0]
        else:
            pass

        # Return a slice of the data from start_time to end_time
        dataToRead = data[int(start_time * sr / 1000): int(end_time * sr / 1000) + 1]

        # Fourier Transform
        N = len(dataToRead)
        yf = rfft(dataToRead)
        xf = rfftfreq(N, 1 / sr)

        # Uncomment these to see the frequency spectrum as a plot
        # plt.plot(xf, np.abs(yf))
        # plt.show()

        # Get the most dominant frequency and return it
        idx = np.argmax(np.abs(yf))
        freq = xf[idx]
        return freq

    while True:
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 0.05
        WAVE_OUTPUT_FILENAME = "analyze.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)


        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(freq("analyze.wav", 0, 50))
