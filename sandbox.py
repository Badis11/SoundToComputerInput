import pyaudio
import time
import wave
import numpy as np
from scipy.fft import *
from scipy.io import wavfile

def playback():
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        return (in_data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    stream_callback=callback)
    stream.start_stream()

    print("to end type stop")

    while True:
        time.sleep(0.1)
        if 1==1:
            print()
        stop=input()
        if stop=="stop":
            stream.stop_stream()
            break

def record(seconds):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = seconds
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play(file):

    CHUNK = 1024
    file=file+'.wav'
    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    print("to end mid-file you need to rerun script")

    while len(data):
        stream.write(data)
        data = wf.readframes(CHUNK)
        stop=0
        if stop == "stop":
            stream.stop_stream()
            break
    stream.stop_stream()
    stream.close()

    p.terminate()

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

        print(freq("analyze.wav", 0, 50))



while True:
    print("type 1 for playback, 2 for recording, 3 for playing a wav file, 4 for analyzing audio or stop to stop")
    x=input()
    if x=="1":
        playback()
    if x=="2":
        print("How many seconds?")
        y =int(input())
        record(y)
    if x=="3":
        print("which .wav file (You need to provide entire path without the extension (e.g. C:Users/song))")
        file=input()
        play(file)
    if x=="4":
        analyze()
    if x=="stop":
        print("stopping")
        break