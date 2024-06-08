import subprocess
from tools.DLog import DLog

class PlaySound:
    
    init_path = Path.instance().init_sound
    HDMI_JACK_CONTROL = 'numid=1'

    @staticmethod
    def set_volume(volume):
        # Assurez-vous que le volume est une valeur entre 0 et 100
        volume = max(0, min(100, volume))
        # subprocess.run(['amixer', 'cset', cls.HDMI_JACK_CONTROL, f'{volume}%'])

    @staticmethod
    def play_sound(file, volume=100):
        DLog.LogSuccess("PLAY SOUND")
        PlaySound.__set_volume(volume)
        # subprocess.run(['aplay', '-D', 'hw:0,0', file])

    @classmethod
    def play_sound(cls, file_name, volume=100):
        sound_path = cls.init_path + file_name
        cls.__play_sound(sound_path, volume)

    @classmethod
    def join(cls):
        volume = 80
        print_path = cls.init_path + "discord_join.wav"
        cls.__play_sound(print_path, volume)
    
    @classmethod
    def print(cls):
        volume = 100
        print_path = cls.init_path + Path.instance().found_sound
        cls.__play_sound(print_path, volume)

if __name__ == "__main__":
    PlaySound.join()
