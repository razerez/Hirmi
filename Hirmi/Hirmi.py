import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
from scipy.io import wavfile
from matplotlib import pyplot as plt
from pydub import AudioSegment
import numpy
import threading
import subprocess
import time


# files:
# CAB- Cut at beginning:
wav1 = "wav1.wav"
# CAE - Cut at end:
wav2 = "wav2.wav"
amount = 10
_rec_time_ = 0.03
_take_ = 0
error_counter = 10
driver = 0
not_driver = 0


def main():
    # transfer record mics and transfer audio to wav:
    global error_counter
    while True:
        error_counter = 10

        while error_counter > 0:
            try:
                t1 = threading.Thread(target=audio_to_wav, args=(wav1, 1, _rec_time_,))
                t2 = threading.Thread(target=audio_to_wav, args=(wav2, 2, _rec_time_,))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            except():
                print("REC error")
                error_counter += 1
            t3 = threading.Thread(target=tread_tst, daemon=True)
            t3.start()

            error_counter -= 1
        t3.join()

        try:
            global driver
            global not_driver

            if driver > not_driver:
                print("Driver is speaking (" + str(driver * 10) + "% accuracy) ")
                set_vol()
            elif driver < not_driver:
                print("Not driver (" + str(driver * 10) + "% accuracy) ")
            else:
                 print("inaccurate")
            driver = 0
            not_driver = 0

        except ZeroDivisionError:
            print("P error")

    # play the wav files audio
    # playsound(wav1)
    # playsound(wav2)

def tread_tst():
    global error_counter
    try:
        arr1, smp1 = wav_to_arr(wav1)
        arr2, smp2 = wav_to_arr(wav2)

        arr1 = abs(arr1)
        arr2 = abs(arr2)

        fix_ratio(arr1, arr2)
        fix_ratio(arr2, arr1)

        get_rounded_arr(arr1)
        # draw_wav(arr1, smp1, "Melikson")
        get_rounded_arr(arr2)
        # draw_wav(arr2, smp2, "Barda")
        trim_arr(arr2, _rec_time_ / 3, smp2)
        sb = subtract_arrays(arr1, arr2, smp1)
        if sb < 0.01:
            print("Driver")
            global driver
            driver += 1
        else:
            global  not_driver
            not_driver += 1
            print("Not Driver")
    except:
        print("Calc Error")
        error_counter += 1


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
    # print("recording: " + str(device))
    # Wait until recording is finished:
    sd.wait()
    # Save as WAV file:
    write(dst, fs, recording)
    new_audio = AudioSegment.from_wav(dst)
    new_audio = new_audio[_delay_*1000:]
    new_audio.export(dst, format="wav")


def fix_ratio(arr1, arr2):
    """
    :param arr1: an audio array
    :param arr2: an audio array
    :return:  the smaller array with multiplied values
    """
    # calc the sum of each array to define which is bigger
    sum1 = sum(arr1)
    sum2 = sum(arr2)

    if sum1 > sum2:
        # the ratio of the arrays
        ratio = sum1 / sum2

        # multiply the smaller array to get they both similar
        for i in range(0, len(arr2)):
            arr2[i] *= ratio
    else:
        # the ratio of the arrays
        ratio = sum2 / sum1

    # multiply the smaller array to get they both similar
    for i in range(0, len(arr1)):
        arr1[i] *= ratio


def wav_to_arr(file):
    samplerate, sound = wavfile.read(file)
    arr = numpy.array(separate_array(sound), dtype=numpy.float64)
    return arr, samplerate


def get_rounded_arr(arr):
    round_arr(arr)


def round_arr(arr):
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


def trim_arr(arr, trim_time, samplerate):
    global _take_
    start = int(time_to_index(trim_time, samplerate))
    end = -start
    _take_ = start
    return arr[start:end]


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


def subtract_arrays(big_arr, small_arr, small_arr_samplerate):
    small_arr = numpy.array(small_arr, dtype=numpy.float64)
    index = match_arrays(big_arr, small_arr)
    return index_to_time(index, small_arr_samplerate)


def time_to_index(time, samplerate):
    return time * samplerate


def index_to_time(index, samplerate):
    return index/samplerate


def match_arrays(big_arr, small_arr):
    """
    move SA(small_array) along BA(big_array) and subtract the values from each other, smallest difference means
    that the arrays are closer
    :param big_arr: array to move along
    :param small_arr: array to move on big array
    :return: index of match in big array
    """
    _pow2_ = 2
    _move_ = 1
    sub_sum = 0
    sub_sum_arr = numpy.array([], dtype=numpy.float64)
    print("match")
    for i in range(0, len(big_arr) - _take_, _move_):
        big_arr_slice = big_arr[i:i + _take_]
        small_arr_slice = small_arr[:]
        fix_arr(big_arr_slice, small_arr_slice)
        for j in range(0, _take_):
            sub_sum += pow(big_arr_slice[j] - small_arr_slice[j], _pow2_)
        sub_sum_arr = numpy.append(sub_sum_arr, [sub_sum, i])
        sub_sum_arr = numpy.reshape(sub_sum_arr, (-1, 2))
        sub_sum = 0
    print("match finished")

    return sub_sum_arr[numpy.argmin(sub_sum_arr[:, 0])][1]


def fix_arr(arr1, arr2):
    sub = int(avg_arr(arr1) - avg_arr(arr2))
    for i in range(0, len(arr2)):
        arr2[i] += sub
    return arr2


def avg_arr(arr):
    return sum(arr) / len(arr)


def set_vol():
    """
    This function is setting the audio level to 30% and then change it back to 100%
    :return: None
    """
    # using Nircmd in order to make the cmd command, ypu need to install it
    subprocess.Popen('cmd /k "nircmd.exe setsysvolume 19661" ')
    time.sleep(3)
    subprocess.Popen('cmd /k "nircmd.exe setsysvolume 65535"')


if __name__ == "__main__":
    # call main:
    main()
