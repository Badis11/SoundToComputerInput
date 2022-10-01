import pyaudio
import time
import wave

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
    while stream.is_active():
        time.sleep(0.1)
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

while True:
    print("type 1 for playback, 2 for recording or stop to stop")
    x=input()
    if x=="1":
        playback()
    if x=="2":
        print("How many seconds?")
        y =int(input())
        record(y)
    if x=="stop":
        print("stopping")
        break