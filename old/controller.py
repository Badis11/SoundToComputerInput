import pyaudio
import wave
import numpy as np
from scipy.fft import *
from scipy.io import wavfile
import math
import pyautogui

scale_downcut = 500
scale_upcut = 1000

def analyze():
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    def freq(file, start_time, end_time):

        sr, data = wavfile.read(file)
        if data.ndim > 1:
            data = data[:, 0]
        else:
            pass

        dataToRead = data[int(start_time * sr / 1000): int(end_time * sr / 1000) + 1]

        N = len(dataToRead)
        yf = rfft(dataToRead)
        xf = rfftfreq(N, 1 / sr)

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

        #print(math.trunc(freq("analyze.wav", 0, 50)))
        eq=math.trunc(freq("analyze.wav", 0, 50))
        if eq==0:
            pass
        if eq <= scale_downcut:
            eq = eq*2
        if eq >= scale_upcut:
            eq = eq/2

        return math.trunc(eq)
        #print(math.trunc(eq))

while True:
    if analyze()<500:
         note = 0
         print(note)
    elif analyze()<540:
         note = "C"
         print(note)
    elif analyze()<565:
        note = "C#"
        print(note)
    elif analyze()<610:
        note = "D"
        print(note)
    elif analyze()<640:
        note = "D#"
        print(note)
    elif analyze()<675:
        note = "E"
        print(note)
    elif analyze()<710:
        note = "F"
        print(note)
    elif analyze()<750:
        note = "F#"
        print(note)
    elif analyze()<810:
        note = "G"
        print(note)
    elif analyze()<860:
        note = "G#"
        print(note)
    elif analyze()<900:
        note = "A"
        print(note)
    elif analyze()<950:
        note = "A#"
        print(note)
    elif analyze()<1200:
        note = "B"
        print(note)
