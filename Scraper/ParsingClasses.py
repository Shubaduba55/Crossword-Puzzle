import io
import pickle
from abc import ABC, abstractmethod


class ParsingObject(ABC):
    def __init__(self, text: str, link: str, is_complete: bool = False):
        self._text = text
        self._link = link
        self._is_complete = is_complete

    def is_complete(self):
        return self._is_complete

    def get_link(self):
        return self._link

    @abstractmethod
    def parse_data(self):
        pass

    @abstractmethod
    def save_data(self, file_write: io.BytesIO):
        pass

    @abstractmethod
    def read_data(self, file_read: io.BytesIO):
        pass


class ParsingGroup(ParsingObject, ABC):
    def __init__(self, text: str,
                 link: str,
                 is_complete: bool = False,
                 is_parsed: bool = False,
                 children=None):
        super().__init__(text, link, is_complete)
        self._children = children  # must be a descendant of ParsingObject
        self._is_parsed = is_parsed  # Indicates whether we got info from children or not

    def is_parsed(self):
        return self._is_parsed

    @abstractmethod
    def unpack_children(self, data_children):
        pass

    def save_data(self, file_write: io.BytesIO):
        if file_write.closed:
            raise "Passed file is closed"
        data_to_save = {
            "_text": self._text,
            "_link": self._link,
            "_is_parsed": self._is_parsed,
            "_children": [child_object.__dict__ for child_object in self._children]
        }
        pickle.dump(data_to_save, file_write)

    def read_data(self, file_read: io.BytesIO):
        if file_read.closed:
            raise "Passed file is closed"
        data_to_restore = pickle.load(file_read)
        self._text = data_to_restore["_text"]
        self._link = data_to_restore["_link"]
        self._is_parsed = data_to_restore["_is_parsed"]
        self._children = self.unpack_children(data_to_restore["_children"])
