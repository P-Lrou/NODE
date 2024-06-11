import sounddevice as sd
import soundfile as sf
from tools.DLog import DLog
from GlobalVariables import Path

class PlaySound:
    # command to run for jack : 
    # sudo jackd -d alsa -d hw:0 -r 44100 &

    init_path = Path.instance().init_sound

    @classmethod
    def __play_sound(cls, file_path: str, volume: int = 100) -> None:
        if file_path is not None:
            DLog.LogSuccess("PLAY SOUND")
            # Load the audio file
            data, fs = sf.read(file_path, dtype='float32')
            # Adjust volume
            data *= volume / 100.0
            # Play the sound
            sd.play(data, samplerate=fs)
            sd.wait()
        else:
            DLog.LogError("There is no file to play")

    @classmethod
    def play(cls, file_name: str, volume: int = 100) -> None:
        if file_name is not None:
            sound_path = cls.init_path + file_name
            cls.__play_sound(sound_path, volume)
    
    @classmethod
    def print(cls) -> None:
        volume = 40
        print_path = cls.init_path + Path.instance().found_sound
        cls.__play_sound(print_path, volume)

    @classmethod
    def test(cls) -> None:
        volume = 10
        print_path = cls.init_path + "discord_join.wav"
        cls.__play_sound(print_path, volume)
        
    @classmethod
    def error(cls) -> None:
        volume = 10
        print_path = cls.init_path + Path.instance().error_sound
        cls.__play_sound(print_path, volume)
