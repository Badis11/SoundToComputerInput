import pyaudio
import time

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