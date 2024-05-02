import subprocess

class PlaySound:
    join_file = 'import/sound/discord_join.mp3'
    leave_file = 'import/sound/discord_leave.mp3'

    @staticmethod
    def play_sound(file):
        subprocess.run(['mpg321', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def join():
        PlaySound.play_sound(PlaySound.join_file)
    
    @staticmethod
    def leave():
        PlaySound.play_sound(PlaySound.leave_file)
