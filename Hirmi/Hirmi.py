import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
from scipy.io import wavfile
import threading


def record_audio(path):
    fs = 44100  # Sample rate
    seconds = 2# Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(path, fs, myrecording)  # Save as WAV file


def main():
    for index in range(1,3):
        x = threading.Thread(target=record_audio, args=(str(index)+".wav",))
        x.start()

main()
