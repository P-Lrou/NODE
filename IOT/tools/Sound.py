import sounddevice as sd
import soundfile as sf
from tools.DLog import DLog
from GlobalVariables import Path

class PlaySound:
    # command to run for jack : 
    # sudo jackd -d alsa -d hw:0 -r 44100 &

    init_path = Path.instance().init_sound

    @classmethod
    def __play_sound(cls, file, volume=100):
        DLog.LogSuccess("PLAY SOUND")
        
        # Load the audio file
        data, fs = sf.read(file, dtype='float32')
        
        # Adjust volume
        data *= volume / 100.0
        
        # Play the sound
        sd.play(data, samplerate=fs)
        sd.wait()

    @classmethod
    def play_sound(cls, file_name, volume=100):
        sound_path = cls.init_path + file_name
        cls.__play_sound(sound_path, volume)
    
    @classmethod
    def print(cls):
        volume = 100
        print_path = cls.init_path + Path.instance().found_sound
        cls.__play_sound(print_path, volume)

    @classmethod
    def error(cls):
        volume = 100
        print_path = cls.init_path + Path.instance().error_sound
        cls.__play_sound(print_path, volume)
