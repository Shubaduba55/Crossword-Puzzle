from ParsingClasses import ParsingGroup
from Word import Word
import requests
from bs4 import BeautifulSoup


class Topic(ParsingGroup):
    def __init__(self, text: str,
                 link: str,
                 is_complete: bool = False,
                 is_parsed: bool = False,
                 children=None):
        super().__init__(text, link, is_complete, is_parsed, children)

    def __str__(self):
        return f"Topic called {self._text}, link: {self._link}"

    def _unpack_children(self, data_children):
        return [Word(**child_data) for child_data in data_children]

    def parse_data(self):
        pass
