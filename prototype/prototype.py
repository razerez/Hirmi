from os import path
from scipy.io.wavfile import read
from pydub import AudioSegment
import numpy

# files
src = "nitayMekalelMp3.mp3"
dst = "test.wav"

# convert wav to mp3
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")
print()
a, b = read(dst)
numpy.array(a[1], dtype=float)
text_file = open("Output.txt", "w")
for i in a:
    print(i, file=text_file)
text_file.close()
