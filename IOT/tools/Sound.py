import subprocess
from tools.DLog import DLog
from GlobalVariables import Path

class PlaySound:
    init_path = Path.instance().init_sound

    @classmethod
    def __set_volume(cls, volume):
        # Assurez-vous que le volume est une valeur entre 0 et 100
        volume = max(0, min(100, volume))
        subprocess.run(['amixer', 'sset', 'Master', f'{volume}%'])

    @classmethod
    def __play_sound(cls, file, volume=100):
        DLog.LogSuccess("PLAY SOUND")
        cls.__set_volume(volume)
        subprocess.run(['aplay', file])

    @classmethod
    def play_sound(cls, file_name, volume=100):
        sound_path = cls.init_path + file_name
        cls.__play_sound(sound_path, volume)
    
    @classmethod
    def print(cls):
        volume = 100
        print_path = cls.init_path + Path.instance().found_sound
        cls.__play_sound(print_path, volume)

