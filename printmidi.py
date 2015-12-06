#
# printmidi.py
# Nick Pham
# CS50 final project, 2015
#
# This program takes the annotations from record2midi.py and converts
# them to a midi that can be used to drive a synthesizer or run a score
# generating software such as MuseScore.  This file calls record2midi.py.
#
# Usage: python printmidi.py [outfile name]
#
# If an outfile name is not provided, the midi file generated will default
# to "output.midi".  IMPORTANT: outfile name must end with '.midi'
#
# conversion to standard midi file based on example from midiutil library
# found at https://code.google.com/p/midiutil/

# libraries
import subprocess
import csv
import os
import getopt
import sys
import requests
from midiutil.MidiFile import MIDIFile

# definitions
SECSperMIN = 60

# determine file name
if len(sys.argv) != 1:
    print "usage: printmidi.py"

# call the record2midi.py program and record its output in a file
os.system('python record2midi.py > out.txt')

# open the file and read the tab separated list into
with open('out.txt') as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)

# display values in terminal
# The first couple lines are the time of the first sample, and the time of
# first note.  The subsequent lines that have three values in each array
# are the MIDI note value, time on, and time off.  The rest of the list
# contains the aubiotrack data that will be used to generate the tempo

# determine tempo
i = len(d) - 1
time_dif = 0
beat_count = 0

# skip any empty arrays
while len(d[i]) == 0:
    i -= 1

# extract the aubiotrack data
while len(d[i]) == 1 and len(d[i - 1]) == 1 and float(d[i][0]) > float(d[i - 1][0]):
    time_dif += float(d[i][0]) - float(d[i - 1][0])
    beat_count += 1
    i -= 1

# calculate bpm
bpm = beat_count * SECSperMIN / (time_dif)
print "bpm =", bpm

# Create the MIDIFile Object
MyMIDI = MIDIFile(1)

# Add track name and tempo. The first argument to addTrackName and
# addTempo is the time to write the event.
track = 0
time = 0
MyMIDI.addTrackName(track, time, "Track0")
MyMIDI.addTempo(track, time, bpm)

# globally, to write all notes on same channel at one volume
channel = 0
volume = 100

# Each line in d contains data for one note
for line in d:
    if len(line) == 3:
        pitch = float(line[0])
        time = float(line[1])
        duration = float(line[2]) - float(line[1])
        # Now add the note.
        MyMIDI.addNote(track, channel, pitch, time, duration, volume)

# Let user decide if they want to save the file
proceed = ''
while proceed not in ('y', 'n'):
    proceed = raw_input('Do you wish to save this file? (y/n) \n')
    if proceed == 'n':
        sys.exit
    elif proceed != 'y':
        print "y/n"

# Let user input the desired file name
outfile_name = raw_input('Please input a filename:\n')

outfile = outfile_name + '.midi'

# Let user input the desired Author
name = raw_input('Please input an author:\n')

# And write it to disk.
binfile = open(outfile, 'wb')
MyMIDI.writeFile(binfile)
binfile.close()

# send file, outfile_name, and author of file to website
r = requests.post('http://ide50-zhao03.cs50.io/apiupload.php', data={'title': outfile_name, 'name': name},
                    files={'fileToUpload': open(outfile, 'rb')})
