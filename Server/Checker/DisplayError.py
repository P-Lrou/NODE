from tools.DLog import DLog
class DisplayError:
    def __init__(self) -> None:
        pass

    @staticmethod
    def display_error(object):
        DLog.LogError(f"There is an error in {object.__class__.__name__} class")