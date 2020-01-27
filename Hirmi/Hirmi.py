import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
from scipy.io import wavfile
from matplotlib import pyplot as plt
from pydub import AudioSegment
import numpy
import threading


# files:
# CAB- Cut at beginning:
wav1 = "wav1.wav"
# CAE - Cut at end:
wav2 = "wav2.wav"


def main():
    # transfer record mics and transfer audio to wav:
    t1 = threading.Thread(target=audio_to_wav, args=(wav1, 2,))
    t2 = threading.Thread(target=audio_to_wav, args=(wav2, 1,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # play the wav files audio
    #playsound(wav1)
    #playsound(wav2)
    draw_wav(wav1, False)
    draw_wav(wav1, True)
    #draw_wav(wav2, False)
    #draw_wav(wav2, True)

    # print delay between sound files:


def audio_to_wav(dst, device):
    """
    converts live audio file to wav file and return sound array
    :param device: which device to use
    :param dst: destination wav file
    """
    DELAY = 1
    # Sample rate:
    fs = 44100
    # Duration of recording:
    seconds = DELAY + 1/1500
    # record:
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, device=device)
    print("recording: " + str(device))
    # Wait until recording is finished:
    sd.wait()
    # Save as WAV file:
    write(dst, fs, recording)
    newAudio = AudioSegment.from_wav(dst)
    newAudio = newAudio[DELAY*1000:]
    newAudio.export(dst, format="wav")


def draw_wav(file, do):
    time_arr = []
    samplerate, sound = wavfile.read(file)
    arr = separate_array(sound)
    size = len(arr)
    time = size / samplerate
    frame_time = time / size
    i = 0
    while i != size:
        time_arr.append(i * frame_time)
        i += 1
    if do:
        avg_arr(arr)
    plt.plot(time_arr, arr)
    plt.title(file + " " + str(do))
    plt.ylabel("Sound")
    plt.xlabel("Time")

    plt.show()


def separate_array(arr):
    ret = []
    for i in range(0, arr.shape[0]):
        ret.append(arr[i][1])
    return ret


def avg_arr(arr):
    #  temp arr:
    t_arr = arr[:]
    amount = 20
    i = amount - 1
    while i != len(t_arr):
        temp = 0
        for j in range(0, amount):
            temp += (t_arr[i - j])
        arr[i] = temp / amount
        i += 1


if __name__ == "__main__":
    # call main:
    main()
