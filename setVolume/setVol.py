import subprocess, keyboard
import time


def vol():
    """
    This function is setting the audio level to 30% and then change it back to 100%
    :return: None
    """
    # using Nircmd in order to make the cmd command, ypu need to install it
    subprocess.Popen('cmd /k "nircmd.exe setsysvolume 19661" ')
    time.sleep(3)
    subprocess.Popen('cmd /k "nircmd.exe setsysvolume 65535"')


def main():
    # A loop in order to check if event happened consistency
    while True:
        # check if the spacebar is pressed
        if keyboard.is_pressed("space"):
            vol()






main()
