class ActualPixels:
    _instance = None

    def __init__(self) -> None:
        self.pixels = {
            "18": [],
            "21": []
        }

    @classmethod
    def instance(cls) -> "ActualPixels":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance