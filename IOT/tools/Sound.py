import subprocess
from tools.DLog import DLog

class PlaySound:
    join_file = 'ressources/sound/discord_join.wav'
    leave_file = 'ressources/sound/discord_leave.wav'
    print_file = 'ressources/sound/print.wav'
    error_file = 'ressources/sound/error.wav'

    @staticmethod
    def set_volume(volume):
        # Assurez-vous que le volume est une valeur entre 0 et 100
        volume = max(0, min(100, volume))
        subprocess.run(['amixer', 'sset', 'Master', f'{volume}%'])

    @staticmethod
    def play_sound(file, volume=100):
        DLog.LogSuccess("PLAY SOUND")
        PlaySound.set_volume(volume)
        subprocess.run(['aplay', file])

    @staticmethod
    def join():
        volume = 50
        PlaySound.play_sound(PlaySound.join_file, volume)
    
    @staticmethod
    def leave():
        volume = 100
        PlaySound.play_sound(PlaySound.leave_file, volume)
    
    @staticmethod
    def print():
        volume = 100
        PlaySound.play_sound(PlaySound.print_file, volume)
    
    @staticmethod
    def error():
        volume = 70
        PlaySound.play_sound(PlaySound.error_file, volume)

if __name__ == "__main__":
    PlaySound.join()
