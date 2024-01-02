import io
import pickle
from abc import ABC, abstractmethod
from typing import BinaryIO

import requests


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
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def parse_data(self, session: requests.Session) -> bool:
        pass

    @abstractmethod
    def save_data(self, file_write: io.BytesIO):
        """
        Saves data to the given file.
        :param file_write: instance of the file, where you want to write the data.
        :return:
        """
        pass

    @abstractmethod
    def read_data(self, file_read: io.BytesIO):
        """
        Reads data from the given file.
        :param file_read: instance of the file, from where you want to read the data.
        :return:
        """
        pass


class ParsingGroup(ParsingObject, ABC):
    def __init__(self,
                 text: str,
                 link: str,
                 is_complete: bool = False,
                 is_parsed: bool = False,
                 children=None):
        super().__init__(text, link, is_complete)
        self._children = children or []  # must be a descendant of ParsingObject
        self._is_parsed = is_parsed  # Indicates whether we got info from children or not

    def is_parsed(self):
        return self._is_parsed

    @abstractmethod
    def _unpack_children(self, data_children):
        """
        Performs process of deserialization and restoration of the child objects
        :param data_children: dictionary of data for the children of the class
        :return: List of objects of child class
        """
        pass

    def to_dict(self) -> dict:
        """
        Puts data of the class into dictionary, including its children!
        :return:
        """
        return {
            "text": self._text,
            "link": self._link,
            "is_complete": self._is_complete,
            "is_parsed": self._is_parsed,
            "children": [child_object.to_dict() for child_object in self._children]
        }

    def save_data(self, file_write: BinaryIO):
        if file_write.closed:
            raise "Passed file is closed"
        data_to_save = {
            "text": self._text,
            "link": self._link,
            "is_complete": self._is_complete,
            "is_parsed": self._is_parsed,
            "children": [child_object.to_dict() for child_object in self._children]
        }
        pickle.dump(data_to_save, file_write)

    def read_data(self, file_read: BinaryIO):
        if file_read.closed:
            raise "Passed file is closed"
        data_to_restore = pickle.load(file_read)
        print("Data to restore:", data_to_restore)
        print("Keys in data to restore:", data_to_restore.keys())
        self._text = data_to_restore["text"]
        self._link = data_to_restore["link"]
        self._is_complete = data_to_restore["is_complete"]
        self._is_parsed = data_to_restore["is_parsed"]
        self._children = self._unpack_children(data_to_restore["children"])
