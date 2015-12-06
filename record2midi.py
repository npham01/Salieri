#
# record2midi.py
# Nick Pham
# CS50 final project, 2015
#
# This program will record a 10 second sample of audio from an audio
# interface.  Then, the program will call the two aubio command-line tools
# to provide annotations which will be used in printmidi.py to generate
# a midi file.
#
# recording functionality based on PyAudio source distribution example,
# seen at https://people.csail.mit.edu/hubert/pyaudio/#docs
#
# midi conversion uses command-line-tools from the aubio library, seen
# at https://aubio.org/manpages/latest/aubionotes.1.html and
# https://aubio.org/manpages/latest/aubiotrack.1.html

# libraries
import subprocess
import aubio
import pyaudio
import wave

# definitions
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

# open the stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# initialize array to store data
frames = []

# while the chuncks can still be read, read them into the array
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

# close stream
stream.stop_stream()
stream.close()
p.terminate()

# write to wav file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# call aubionotes command line tool to determine notes
subprocess.call(['aubionotes', '-i', 'output.wav'])
print "\n"

# call aubiotrack command line tool to determine tempo
subprocess.call(['aubiotrack', '-i', 'output.wav'])
