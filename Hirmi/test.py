import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
from scipy.io import wavfile
from matplotlib import pyplot as plt
from pydub import AudioSegment
import numpy
import threading
import random
import math


def main():
    a1 = [36, 14, 9, 21, 99, 74, 1, 55, 15, 25, 26, 79, 30, 16, 90, 65, 5, 80, 24, 11, 83, 75, 61, 76, 81, 95, 11, 86,
          20, 37, 50, 55, 38, 58, 2, 5, 14, 22, 71, 78, 11, 8, 6, 6, 54, 53, 92, 47, 23, 33, 37, 40, 87, 21, 44, 22,
          62, 86, 88, 83, 89, 93, 19, 34, 96, 19, 7, 44, 20, 32, 42, 22, 49, 64, 87, 14, 96, 19, 31, 59, 86, 41, 23,
          26, 39, 97, 14, 79, 22, 79, 70, 2, 78, 48, 29, 9, 76, 36, 41, 48]
    a2 = [80, 50, 0, 30, 5]

    #print(subtract_arrays(a1, a2, 100))
    print(a2[1:-1])


def subtract_arrays(big_arr, small_arr, samplerate):
    match_arrays(big_arr, small_arr)
    small_arr = numpy.array(small_arr, dtype=numpy.float64)
    index = match_arrays(big_arr, small_arr)
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
    _take_ = 5
    _move_ = 1
    sub_sum = 0
    sub_sum_arr = numpy.array([], dtype=numpy.float64)
    for i in range(0, len(big_arr) - _take_, _move_):
        big_arr_slice = big_arr[i:i + _take_]
        small_arr_slice = small_arr[:]
        fix_arr(big_arr_slice, small_arr_slice)
        for j in range(0, _take_):
            sub_sum += pow(big_arr_slice[j] - small_arr_slice[j], _pow2_)
        sub_sum_arr = numpy.append(sub_sum_arr, [sub_sum, i])
        sub_sum_arr = numpy.reshape(sub_sum_arr, (-1, 2))
        sub_sum = 0
    return sub_sum_arr[numpy.argmin(sub_sum_arr[:, 0])][1]


def fix_arr(arr1, arr2):
    sub = int(avg_arr(arr1) - avg_arr(arr2))
    print(sub)
    for i in range(0, len(arr2)):
        arr2[i] += sub
    return arr2


def avg_arr(arr):
    return sum(arr) / len(arr)


if __name__ == "__main__":
    # call main:
    main()
