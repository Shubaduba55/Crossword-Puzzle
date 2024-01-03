from ParsingClasses import ParsingGroup
from Word import Word
import requests
from bs4 import BeautifulSoup

"""
ul.top-g li a
"""


def get_words(soup: BeautifulSoup) -> dict:
    """
    Gets all words from the Topic.
    :param soup: scraped HTML code of the page
    :return: dictionary of such template: {"Word's Name": "Link to the word"}
    """
    results = {}
    try:
        all_links = soup.select('ul.top-g li a')

        for link in all_links:
            try:
                word_label_text = link.get_text(strip=True)
                results[word_label_text] = link['href']
            except (AttributeError, TypeError) as e:
                print(f"Exception occurred: {e}")

    except Exception as e:
        print(f"Unexpected exception occurred: {e}")

    return results


class Topic(ParsingGroup):
    """
    Class that stores info of words and links to them. Its children are words.
    """
    def __init__(self, text: str,
                 link: str,
                 is_complete: bool = False,
                 is_parsed: bool = False,
                 children=None):
        children = [Word(**child_data) for child_data in children] if children else []
        super().__init__(text, link, is_complete, is_parsed, children)

    def __str__(self):
        return f"Topic called {self._text}, link: {self._link}"

    def parse_data(self, session: requests.Session) -> bool:
        """
        Parses data (links and words' names) from the topic's webpage
        creating objects of class Word.
        Note: you need to specify parameters of session variable before
        giving it to this method. For example, specify headers for the session.
        :param session:
        :return: True if parsing process succeeded, else False.
        """
        return self._parse_data(session, get_words, Word)

