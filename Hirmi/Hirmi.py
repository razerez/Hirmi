import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
from scipy.io import wavfile
import threading

# files:
# CAB- Cut at beginning:
cab_wav = "CABwav.wav"
# CAE - Cut at end:
cae_wav = "CAEwav.wav"


def main():
    # transfer record mics and transfer audio to wav:
    t1 = threading.Thread(target=audio_to_wav, args=(cab_wav, 2,))
    t2 = threading.Thread(target=audio_to_wav, args=(cae_wav, 1,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # play the wav files audio
    playsound(cab_wav)
    playsound(cae_wav)
    # print delay between sound files:


def audio_to_wav(dst, device):
    """
    converts live audio file to wav file and return sound array
    :param device: which device to use
    :param dst: destination wav file
    """
    # Sample rate:
    fs = 4410
    # Duration of recording:
    seconds = 5
    # record:
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, device=device)
    print("recording: " + str(device))
    # Wait until recording is finished:
    sd.wait()
    # Save as WAV file:
    write(dst, fs, myrecording)

if __name__ == "__main__":
    # call main:
    main()
