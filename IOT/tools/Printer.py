import subprocess

class Printer:
    @staticmethod
    def print(image_path: str) -> None:
        command = [
            'phomemo_printer',
            '-a', 'D0:67:6C:D1:DB:6D',
            '-c', '1',
            '-i', image_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)