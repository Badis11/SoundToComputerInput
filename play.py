# This should work as a module

import pyaudio
import wave

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
