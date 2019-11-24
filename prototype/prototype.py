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
    cab_arr = mp3_to_wav(cab_mp3, cab_wav)  # transfer cab from mp3 to wav
    cae_arr = mp3_to_wav(cae_mp3, cae_wav)  # transfer cae from mp3 to wav
    print(cmp_sound_files(cab_arr, cae_arr))  # print delay between sound files


def mp3_to_wav(src, dst):
    """
    converts mp3 file to wav file and return sound array
    :param src: mp3 file to convert
    :param dst: destination wav file
    :return: a sound file object that represents the wav data
    """
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")  # mp3 to wav file
    data = sf.SoundFile(dst)  # data is a soundfile object
    return data


def cmp_sound_files(sf1, sf2):
    """
    compares 2 identical but indented sound files and return the length of the indentation
    :param sf1: sound file 1
    :param sf2: sound file 2
    :return: delay time between sf1 and sf2
    """

    sf1_arr = sf.read(sf1.name)
    sf2_arr = sf.read(sf2.name)
    count = 0
    for i in range(1, len(sf1_arr[0])):  # run from start to end of soundfile
        for j in range(1, len(sf2_arr[0])):  # run from start to end of soundfile
            if sf1_arr[0][i] == sf2_arr[0][j]:  # if a match between a frame of the soundfiles has found
                count += 1
                i += 1  # forward i by 1
            else:
                count = 0  # if the streak was broken the match was a coincidence
            if count > 10:  # after 10 matches we can be almost certain that this is not a coincidence
                sf2_arr = sf2_arr[0:j]  # slice soundfile from start to j
                break
        if count > 10:  # after 10 matches we can be almost certain that this is not a coincidence
            sf1_arr = sf1_arr[0:i]  # slice soundfile from start to i
            break
    return len(sf1_arr[0]) / sf1.samplerate - len(sf2_arr[0]) / sf2.samplerate  # len / samplerate is the length
                                                                                # in time units of the soundfile


if __name__ == "__main__":
    main()  # call main
