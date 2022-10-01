import pyaudio
import time
import wave
import numpy as np

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

def analyze():
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=
                    p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True)
    stream.start_stream()

    chunk = 2048

    # open up a wave
    wf = wave.open(stream, 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(chunk)
    # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format=
                    p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=RATE,
                    output=True)

    # read some data
    data = wf.readframes(chunk)
    # play stream and find the frequency of each chunk
    while len(data) == chunk * swidth:
        # write data out to the audio stream
        stream.write(data)
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), \
                                             data)) * window
        # Take the fft and square each value
        fftData = abs(np.fft.rfft(indata)) ** 2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which + x1) * RATE / chunk
            print("The freq is %f Hz." % (thefreq))
        else:
            thefreq = which * RATE / chunk
            print("The freq is %f Hz." % (thefreq))
        # read some more data
        data = wf.readframes(chunk)
    if data:
        stream.write(data)
    stream.close()
    p.terminate()


while True:
    print(dict.getMicrophoneList())
    print("type 1 for playback, 2 for recording, 3 for analyzing audio or stop to stop")
    x=input()
    if x=="1":
        playback()
    if x=="2":
        print("How many seconds?")
        y =int(input())
        record(y)
    if x=="3":
        analyze()
    if x=="stop":
        print("stopping")
        break