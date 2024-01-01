import io
import pickle

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

    def save_data(self, file_write: io.BytesIO):
        if file_write.closed:
            raise "Passed file is closed"
        data_to_save = {
            "_text": self._text,
            "_link": self._link,
            "_is_complete": self._is_complete,
            "_word_type": self.__word_type,
            "_definitions": self.__definitions
        }
        pickle.dump(data_to_save, file_write)

    def read_data(self, file_read: io.BytesIO):
        data_to_restore = pickle.load(file_read)
        self._text = data_to_restore["_text"]
        self._link = data_to_restore["_link"]
        self._is_complete = data_to_restore["_is_complete"]
        self.__word_type = data_to_restore["_word_type"]
        self.__definitions = data_to_restore["_definitions"]

    def parse_data(self):
        pass
