import os
import simpleaudio as sa
from time import sleep

DIRECTORY = os.getcwd()


def countdown(time: int) -> None:
    """Counts down for {time} seconds, playing sound at each second

    Args:
        time: (int) Number of seconds to count down for

    Returns: None
    """
    wave_obj = sa.WaveObject.from_wave_file(f"{DIRECTORY}/sounds/beep.wav")
    count = 0
    while count < time:
        play_obj = wave_obj.play()
        sleep(1)
        play_obj.wait_done()
        count += 1


def play_quick_sound(num_times: int) -> None:
    """Plays sound at every 0.25 seconds for {num_times} times

    Args:
        num_times: (int) Number of times to play sound

    Returns: None
    """
    wave_obj = sa.WaveObject.from_wave_file(f"{DIRECTORY}/sounds/beep.wav")
    count = 0
    while count < num_times:
        play_obj = wave_obj.play()
        sleep(0.25)
        play_obj.wait_done()
        count += 1
