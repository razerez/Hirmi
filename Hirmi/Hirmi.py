import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
from scipy.io import wavfile
from matplotlib import pyplot as plt
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

    draw_wav(wav1)
    draw_wav(wav2)

    # print delay between sound files:


def audio_to_wav(dst, device):
    """
    converts live audio file to wav file and return sound array
    :param device: which device to use
    :param dst: destination wav file
    """
    # Sample rate:
    fs = 44100
    # Duration of recording:
    seconds = 3
    # record:
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, device=device)
    print("recording: " + str(device))
    # Wait until recording is finished:
    sd.wait()
    # Save as WAV file:
    write(dst, fs, recording)


def draw_wav(file):
    time_arr = []
    samplerate, arr = wavfile.read(file)
    size = arr.shape[0]
    time = size / samplerate
    frame_time = time / size
    i = 0
    while i != size:
        time_arr.append(i * frame_time)
        print(time_arr[i])
        i += 1
    #avg_arr(arr)
    plt.plot(time_arr, arr)
    plt.xlabel("Time")
    plt.ylabel("Sound")
    plt.show()


def avg_arr(arr):
    amount = 5
    temp = 0
    i = amount
    while i != arr.shape[0]:
        for j in range(0, amount):
            temp += (arr[i - j])
        temp = temp[0]
        print(arr[i][0])
        arr[i][0] = temp / amount
        i += 1


if __name__ == "__main__":
    # call main:
    main()
