from abc import ABC, abstractmethod
from typing import Callable

import requests
from bs4 import BeautifulSoup


class ParsingObject(ABC):
    def __init__(self, text: str, link: str, is_complete: bool = False):
        self._text = text
        self._link = link
        self._is_complete = is_complete

    def is_complete(self):
        return self._is_complete

    def get_text(self):
        return self._text

    def get_link(self):
        return self._link

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def print_all(self, depth: int):
        pass

    @abstractmethod
    def parse_data(self, session: requests.Session) -> bool:
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

    def get_number_of_children(self):
        return len(self._children)

    def get_children(self) -> list:
        """
        :return: Copy of the children of the Class.
        """
        return self._children.copy()

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

    def display_and_choose_child(self) -> ParsingObject:
        n = len(self._children)

        for i in range(n):
            child = self._children[i]
            print(f"{i + 1}. {child.get_text()} "
                  f"{child.is_complete()} "
                  f"{child.get_number_of_children()}")

        option = 0
        while option <= 0 or option > n:
            option = int(input("Choose child: "))

        return self._children[option]

    def print_all(self, depth: int = 0):
        for child in self._children:
            print(depth * "\t" + f"{child}")
            child.print_all(depth + 1)

    def _parse_data(self,
                    session: requests.Session,
                    get_webpage_dict: Callable[[BeautifulSoup], dict],
                    children_class: type) -> bool:
        if self._is_parsed:
            return self._is_parsed

        web_response = session.get(self.get_link())

        if web_response.status_code == 200:

            soup = BeautifulSoup(web_response.text, 'html.parser')

            try:
                res_dict = get_webpage_dict(soup)
                for child_name, link in res_dict.items():
                    self._children.append(children_class(child_name, link))

                if len(self._children) != 0:
                    self._is_parsed = True

            except AttributeError:
                print(f'{children_class.__name__} not found')
        else:
            print('Failed to get response...')

        return self._is_parsed
