import subprocess
from tools.DLog import DLog
from GlobalVariables import Path

class PlaySound:
    
    init_path = Path.instance().init_sound
    HDMI_JACK_CONTROL = 'numid=1'

    @classmethod
    def __set_volume(cls, volume):
        # Assurez-vous que le volume est une valeur entre 0 et 100
        volume = max(0, min(100, volume))
        # Mettre à jour le volume pour HDMI Jack avec sudo
        try:
            subprocess.run(['sudo', 'amixer', 'cset', cls.HDMI_JACK_CONTROL, f'{volume}%'], check=True)
        except subprocess.CalledProcessError as e:
            DLog.LogError(f"Failed to set volume: {e}")
            print(f"Failed to set volume: {e}")

    @classmethod
    def __play_sound(cls, file, volume=100):
        DLog.LogSuccess("PLAY SOUND")
        PlaySound.__set_volume(volume)
        # Jouer le son en utilisant mpg123 avec sudo
        try:
            subprocess.run(['sudo', 'mpg123', '-a', 'hw:0,0', file], check=True)
        except subprocess.CalledProcessError as e:
            DLog.LogError(f"Failed to play sound: {e}")
            print(f"Failed to play sound: {e}")

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
