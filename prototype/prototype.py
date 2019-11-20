import sys
import soundfile as sf
from pydub import AudioSegment
import numpy

# files
cab_mp3 = "wowowCAB.mp3"  # CAB- Cut at beginning
cae_mp3 = "wowowCAE.mp3"  # CAE - Cut at end
cab_wav = "CABwav.wav"
cae_wav = "CAEwav.wav"


def main():
    cab_arr = mp3_to_wav(cab_mp3, cab_wav)
    cae_arr = mp3_to_wav(cae_mp3, cae_wav)
    print(cmp_sound_files(cab_arr, cae_arr))


def mp3_to_wav(src, dst):
    """
    converts mp3 file to wav file and return sound array
    :param src: mp3 file to convert
    :param dst: destination wav file
    :return: a sound file object that represents the wav data
    """
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    data = sf.SoundFile(dst)
    return data


def cmp_sound_files(sf1, sf2):
    """
    compares 2 identical but indented sound files and return the length of the indentation
    :param sf1: sound file 1
    :param sf2: sound file 2
    :return: delay time between sf1 and sf2
    """
    count = 0
    for i in range(1, len(sf1)):
        for j in range(1, len(sf2)):
            if sf1.read(i) == sf2.read(j):
                count += 1
                i += 1
            else:
                count = 0
            if count > 10:
                sf2 = sf2[0:j]
                break
        if count > 10:
            sf1 = sf1[0:i]
            break
    return len(sf1) / sf1.samplerate - len(sf2) / sf2.samplerate


if __name__ == "__main__":
    main()
