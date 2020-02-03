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
amount = 1


def main():
    # transfer record mics and transfer audio to wav:
    t1 = threading.Thread(target=audio_to_wav, args=(wav1, 3, 10,))
    t2 = threading.Thread(target=audio_to_wav, args=(wav2, 2, 10,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # play the wav files audio
    # playsound(wav1)
    # playsound(wav2)
    arr1, smp1 = fix_arr(wav1, True)
    draw_wav(arr1, smp1, "mic x6")
    arr2, smp2 = fix_arr(wav2, True)
    draw_wav(arr2, smp2, "mic x7")
    compare_extreme_points(arr1, smp1, arr2, smp2)
    # print delay between sound files:


def compare_extreme_points(arr1, smp1, arr2, smp2):
    exp1 = get_extreme_time(arr1, smp1)
    exp2 = get_extreme_time(arr2, smp2)
    time_gap = abs(exp1 - exp2)
    print(time_gap)


def get_extreme_time(arr, smp):
    time_arr = get_time_arr(arr, smp)
    min_index = numpy.where(arr == min(arr))[0][0]
    return time_arr[min_index]


def audio_to_wav(dst, device, duration):
    """
    converts live audio file to wav file and return sound array
    :param duration: duration of recording
    :param device: which device to use
    :param dst: destination wav file
    """
    _delay_ = 0
    # Sample rate:
    fs = 44100
    # Duration of recording:
    seconds = _delay_ + duration
    # record:
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, device=device)
    print("recording: " + str(device))
    # Wait until recording is finished:
    sd.wait()
    # Save as WAV file:
    write(dst, fs, recording)
    new_audio = AudioSegment.from_wav(dst)
    new_audio = new_audio[_delay_*1000:]
    new_audio.export(dst, format="wav")


def fix_arr(file, avg):
    samplerate, sound = wavfile.read(file)
    arr = numpy.array(separate_array(sound), dtype=numpy.float64)
    if avg:
        avg_arr(arr)
    return arr, samplerate


def draw_wav(arr, samplerate, name="enter name"):
    """
    draw a graph of the audio in comparison to the time
    :param name: name to write on the graph
    :param samplerate: sample rate of the sound file
    :param arr: array to draw
    """
    time_arr = get_time_arr(arr, samplerate)
    plt.plot(time_arr, arr)
    plt.title(name)
    plt.ylabel("Sound")
    plt.xlabel("Time")

    plt.show()
    return arr


def get_time_arr(arr, samplerate):
    time_arr = []
    size = len(arr)
    time = size / samplerate
    frame_time = time / size
    i = 0
    while i != size:
        time_arr.append(i * frame_time)
        i += 1
    return time_arr


def subtract_arrays(big_arr, small_arr):
    """
    move SA(small_array) along BA(big_array) and subtract the values from each other, smallest difference means
    that the arrays are closer
    :param big_arr: array to move along
    :param small_arr: array to move on big array
    :return:
    """
    _pow2_ = 2
    _take_ = 10
    sub_sum = 0
    sub_sum_arr = numpy.array([], dtype=numpy.float64)
    small_arr_slice = small_arr[:_take_]
    for i in range(0, len(big_arr) - 10, _take_):
        for j in range(0, _take_):
            sub_sum += pow(big_arr[i + j] - small_arr_slice[j], _pow2_)
        sub_sum_arr = numpy.append(sub_sum_arr, sub_sum)
        sub_sum = 0

    return numpy.where(sub_sum_arr == min(sub_sum_arr))[0][0]


def separate_array(arr):
    """
    separate pairs of array to arr[0] only
    :param arr: array
    :return: new array
    """
    ret = []
    for i in range(0, arr.shape[0]):
        ret.append(arr[i][1])
    return ret


def avg_arr(arr):
    """
    moving average- make an average of each five elements of the array moving forward by one element each time
    :param arr: input array
    """
    #  temp arr:
    t_arr = arr[:]
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
