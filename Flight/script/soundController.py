import os
import simpleaudio as sa
from time import sleep


DIRECTORY = os.getcwd()


class SoundController:

    def __init__(self):
        sound_file_path = f"{DIRECTORY}/../../Flight/sounds/beep.wav"
        self.sound = sa.WaveObject.from_wave_file(sound_file_path)

    def countdown(self, time: int) -> None:
        """Counts down for {time} seconds, playing sound at each second
        Args:
            time: (int) Number of seconds to count down for
        Returns: None
        """
        count = 0
        while count < time:
            play_obj = self.sound.play()
            sleep(1)
            play_obj.wait_done()
            count += 1

    def play_quick_sound(self, num_times: int) -> None:
        """Plays sound at every 0.25 seconds for {num_times} times
        Args:
            num_times: (int) Number of times to play sound
        Returns: None
        """
        count = 0
        while count < num_times:
            play_obj = self.sound.play()
            sleep(0.25)
            play_obj.wait_done()
            count += 1
