import sys
import soundfile as sf
from pydub import AudioSegment
from scipy.io import wavfile
import numpy

# files
# CAB- Cut at beginning:
cab_mp3 = "wowowCAB.mp3"
# CAE - Cut at end:
cae_mp3 = "wowowCAE.mp3"
cab_wav = "CABwav.wav"
cae_wav = "CAEwav.wav"


def main():
    # transfer cab from mp3 to wav:
    mp3_to_wav(cab_mp3, cab_wav)
    # transfer cae from mp3 to wav:
    mp3_to_wav(cae_mp3, cae_wav)
    # print delay between sound files:
    print(cmp_sound_files(cab_wav, cae_wav))


def mp3_to_wav(src, dst):
    """
    converts mp3 file to wav file and return sound array
    :param src: mp3 file to convert
    :param dst: destination wav file
    """
    sound = AudioSegment.from_mp3(src)
    # mp3 to wav file:
    sound.export(dst, format="wav")


def cmp_sound_files(wav1, wav2):
    """
    compares 2 identical but indented sound files and return the length of the indentation
    :param wav1: sound file 1
    :param wav2: sound file 2
    :return: delay time between sf1 and sf2
    """

    wav1_samplerate, wav1_arr = wavfile.read(wav1)
    wav2_samplerate, wav2_arr = wavfile.read(wav2)
    count = 0
    for i in range(1, wav1_arr.shape[0]):  # run from start to end of soundfile
        for j in range(1, wav2_arr.shape[0]):  # run from start to end of soundfile
            if wav1_arr[i] == wav2_arr[j]:  # if a match between a frame of the soundfiles has found
                count += 1
                i += 1  # forward i by 1
            else:
                count = 0  # if the streak was broken the match was a coincidence
            if count > 10:  # after 10 matches we can be almost certain that this is not a coincidence
                wav2_arr = wav2_arr[0:j]  # slice soundfile from start to j
                break
        if count > 10:  # after 10 matches we can be almost certain that this is not a coincidence
            wav1_arr = wav1_arr[0:i]  # slice soundfile from start to i
            break
    return wav1_arr.shape[0] / wav1_samplerate - wav2_arr.shape[0] / wav2_samplerate  # len / samplerate is the length
                                                                                # in time units of the soundfile


if __name__ == "__main__":
    main()  # call main
