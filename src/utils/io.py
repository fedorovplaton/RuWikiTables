import pickle
from typing import Any


def dump(obj: Any, filename: str) -> None:
    """
        Dump object to file
        :param obj: Any
        :param filename: str
    """

    file = open(filename, "wb")
    pickle.dump(obj, file)


def hook_up(filename: str) -> Any:
    """
        Hook up object from file
        :param filename: str
        :return: object as Any
    """

    file = open(filename, "rb")

    return pickle.load(file)
