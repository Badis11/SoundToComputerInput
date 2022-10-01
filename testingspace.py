'''import pyaudio
import wave
import numpy as np

chunk = 2048
print("1")
# open up a wave
wf = wave.open('output.wav', 'rb')
swidth = wf.getsampwidth()
RATE = wf.getframerate()
print("1")
# use a Blackman window
window = np.blackman(chunk)
# open stream
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)
print("1")
# read some data
data = wf.readframes(chunk)
# play stream and find the frequency of each chunk
print("1")
while len(data) == chunk*swidth:
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    print("1")
    # find the maximum
    which = fftData[1:].argmax() + 1
    print("1")
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/chunk
        print("The freq is %f Hz." % (thefreq))
    else:
        thefreq = which*RATE/chunk
        print("The freq is %f Hz." % (thefreq))
    # read some more data
    data = wf.readframes(chunk)
if data:
    stream.write(data)
stream.close()
p.terminate()
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
x="100hz.wav"
fft_data= np.fft.fft(x)
freqs = np.fft.fftfreq(len(x))

peak_coefficient = np.argmax(np.abs(fft_data))
peak_freq = freqs[peak_coefficient]

samplerate, data = wavfile.read("10khz.wav")
print(f"Sample rate: {samplerate}")

length = data.shape[0] / samplerate
print(f"length = {length}s")
from apu import APU
apu = APU()
print(apu.getMicrophoneList())
print(apu.test())'''
'''
#https://fazals.ddns.net/spectrum-analyser-part-1/

import numpy as np #importing Numpy with an alias np
import pyaudio as pa
import struct
import matplotlib.pyplot as plt

CHUNK = 1024 * 1
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100 # in Hz

p = pa.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)



fig, (ax,ax1) = plt.subplots(2)
x_fft = np.linspace(0, RATE, CHUNK)
x = np.arange(0,2*CHUNK,2)
line, = ax.plot(x, np.random.rand(CHUNK),'r')
line_fft, = ax1.semilogx(x_fft, np.random.rand(CHUNK), 'b')
ax.set_ylim(-32000,32000)
ax.ser_xlim = (0,CHUNK)
ax1.set_xlim(20,RATE/2)
ax1.set_ylim(0,1)

while 1:
    data = stream.read(CHUNK)
    dataInt = struct.unpack(str(CHUNK) + 'h', data)
    print(x_fft)'''

import pyaudio
import wave
import sys

CHUNK = 1024



wf = wave.open("aotkq.wav", 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while len(data):
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()