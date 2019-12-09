import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
from scipy.io import wavfile

fs = 441000  # Sample rate
seconds = 2 # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file