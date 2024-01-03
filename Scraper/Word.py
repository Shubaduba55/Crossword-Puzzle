import pickle
from typing import BinaryIO

import requests

from ParsingClasses import ParsingObject


class Word(ParsingObject):
    def __init__(self,
                 text: str,
                 link: str,
                 is_complete: bool = False,
                 word_type: str = "undefined",
                 definitions: list = None):
        super().__init__(text, link, is_complete)
        self.__word_type = word_type
        self.__definitions = definitions or []

    def __str__(self):
        return self._text

    def to_dict(self):
        return {
            "text": self._text,
            "link": self._link,
            "is_complete": self._is_complete,
            "word_type": self.__word_type,
            "definitions": self.__definitions
        }

    def print_all(self, depth: int):
        for definition in self.__definitions:
            print(depth * "\t" + f"{definition}")

    def save_data(self, file_write: BinaryIO):
        if file_write.closed:
            raise "Passed file is closed"
        data_to_save = {
            "text": self._text,
            "link": self._link,
            "is_complete": self._is_complete,
            "word_type": self.__word_type,
            "definitions": self.__definitions
        }
        pickle.dump(data_to_save, file_write)

    def read_data(self, file_read: BinaryIO):
        data_to_restore = pickle.load(file_read)
        self._text = data_to_restore["text"]
        self._link = data_to_restore["link"]
        self._is_complete = data_to_restore["is_complete"]
        self.__word_type = data_to_restore["word_type"]
        self.__definitions = data_to_restore["definitions"]

    def parse_data(self, session: requests.Session) -> bool:
        pass
