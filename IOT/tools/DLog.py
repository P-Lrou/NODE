import datetime

class Colors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    DARK_GRAY = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'


class DLog:
    @staticmethod
    def Log(message):
        print(f"{Colors.HEADER}[INFO] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}{Colors.ENDC}")

    @staticmethod
    def LogWhisper(message):
        print(f"{Colors.DARK_GRAY}{Colors.DIM}{Colors.ITALIC}[WHISPER] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}{Colors.ENDC}")

    @staticmethod
    def LogSuccess(message):
        print(f"{Colors.OK_GREEN}[SUCCESS] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}{Colors.ENDC}")

    @staticmethod
    def LogWarning(message):
        print(f"{Colors.WARNING}[WARNING] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}{Colors.ENDC}")

    @staticmethod
    def LogError(message):
        print(f"{Colors.FAIL}{Colors.BOLD}[ERROR] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}{Colors.ENDC}")