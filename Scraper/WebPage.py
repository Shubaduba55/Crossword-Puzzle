from Category import Category
from ParsingClasses import ParsingGroup
import requests
from bs4 import BeautifulSoup

"""
Note for HTML file structure:
body -> div (id="main_container") -> div (class="responsive_container") -> div (class = "topic_list") ->
-> div (class = "topic-box") -> a (link) -> div (class = "topic-content") -> div (class = "topic-label") ->
-> text
"""


class WebPage(ParsingGroup):
    def __init__(self,
                 text: str = "None",
                 link: str = "None",
                 is_complete: bool = False,
                 is_parsed: bool = False,
                 children=None):
        super().__init__(text, link, is_complete, is_parsed, children)

    def __str__(self):
        return f"WebPage called {self._text}, link: {self._link}"

    def unpack_children(self, data_children):
        # Deserialize and restore child objects
        return [Category(**child_data) for child_data in data_children]

    def parse_data(self):
        web_response = requests.get(self.get_link())
        pass



