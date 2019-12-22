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
    # transfer mic1 audio to wav:
    t1 = threading.Thread(target= audio_to_wav, args=(cab_wav, 2,))
    t1.start()
    t1.join()
    # transfer mic2 audio to wav:
    t2 = threading.Thread(target= audio_to_wav, args=(cae_wav, 1,))
    t2.start()
    t2.join()
    # play the wav files audio
    playsound(cab_wav)
    playsound(cae_wav)
    # print delay between sound files:
   # print(cmp_sound_files(cab_wav, cae_wav, True))


def audio_to_wav(dst, device):
    """
    converts live audio file to wav file and return sound array
    :param dst: destination wav file
    """
    # Sample rate:
    fs = 4410
    # Duration of recording:
    seconds = 5

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, device=device)
    # Wait until recording is finished:
    sd.wait()
    # Save as WAV file:
    write(dst, fs, myrecording)


def cmp_sound_files(wav1, wav2, first):
    """
    compares 2 identical but indented sound files and return the length of the indentation
    :param first: boolean variable that indicates if this is the first iteration
    :param wav1: sound file 1
    :param wav2: sound file 2
    :return: delay time between soundfile 1 and soundfile 2
    """

    wav1_samplerate, wav1_arr = wavfile.read(wav1)
    wav2_samplerate, wav2_arr = wavfile.read(wav2)
    count = 0
    i = 0
    # run from start to end of soundfile:
    for j in range(1, wav2_arr.shape[0]):
        # if a match between a frame of the soundfiles has found:
        if wav1_arr[i] == wav2_arr[j]:
            count += 1
            # forward i by 1:
            i += 1
        else:
            # if the streak was broken the match was a coincidence:
            count = 0
            # after 10 matches we can be almost certain that this is not a coincidence:
        if count > 10:
            # slice soundfile from j to end of array:
            wav2_arr = wav2_arr[j:]
            break
        # after 10 matches we can be almost certain that this is not a coincidence:
        if count > 10:
            # slice soundfile from i to end of array:
            wav1_arr = wav1_arr[i:]
            break
    if first and count == 0:
        first = False
        return cmp_sound_files(wav2, wav1, first)
    # len / sampleRate is the length # in time units of the soundfile:
    return wav1_arr.shape[0] / wav1_samplerate - wav2_arr.shape[0] / wav2_samplerate


if __name__ == "__main__":
    # call main:
    main()
