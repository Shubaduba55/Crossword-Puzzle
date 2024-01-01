from ParsingClasses import ParsingGroup
from Topic import Topic
import requests
from bs4 import BeautifulSoup


class Category(ParsingGroup):
    def __init__(self, text: str,
                 link: str,
                 is_complete: bool = False,
                 is_parsed: bool = False,
                 children=None):
        super().__init__(text, link, is_complete, is_parsed, children)

    def __str__(self):
        return f"Category called {self._text}, link: {self._link}"

    def unpack_children(self, data_children):
        # Deserialize and restore child objects
        return [Topic(**child_data) for child_data in data_children]

    def parse_data(self):
        pass

