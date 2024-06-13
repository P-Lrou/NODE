from Checker.Testable import Testable
class Checker:
    def __init__(self) -> None:
        pass

    @staticmethod
    def test_object(testable_object: Testable) -> Testable:
        if testable_object.test():
            return None
        else:
            return testable_object

    @classmethod
    def test_objects(cls, testable_objects: list[Testable]) -> Testable:
        for testable_object in testable_objects:
            if cls.test_object(testable_object):
                return testable_object
        return None