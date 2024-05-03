import subprocess

class PlaySound:
    join_file = 'import/sound/discord_join.wav'
    leave_file = 'import/sound/discord_leave.wav'
    print_file = 'import/sound/print.wav'
    error_file = 'import/sound/error.wav'

    @staticmethod
    def play_sound(file):
        subprocess.run(['aplay', file])

    @staticmethod
    def join():
        PlaySound.play_sound(PlaySound.join_file)
    
    @staticmethod
    def leave():
        PlaySound.play_sound(PlaySound.leave_file)
    
    @staticmethod
    def print():
        PlaySound.play_sound(PlaySound.print_file)
    
    @staticmethod
    def error():
        PlaySound.play_sound(PlaySound.error_file)
