from ParsingClasses import ParsingGroup
from Topic import Topic
import requests
from bs4 import BeautifulSoup

"""
div (class="topic-box topic-box-secondary") -> <a> (class="topic-box-secondary-heading") -> text

a.topic-box-secondary-heading
"""


def get_topics(soup: BeautifulSoup) -> dict:
    """
    Gets all categories from the WebPage.
    :param soup: scraped HTML code of the page
    :return: dictionary of such template: {"Topic Name": "Link to the topic"}
    """
    results = {}
    try:
        all_links = soup.find_all('a.topic-box-secondary-heading')

        for link in all_links:
            try:
                topic_label_text = link.get_text(strip=True)
                results[topic_label_text] = link['href']
            except (AttributeError, TypeError) as e:
                print(f"Exception occurred: {e}")

    except Exception as e:
        print(f"Unexpected exception occurred: {e}")

    return results


class Category(ParsingGroup):
    """
    Class that stores info of categories and links to them. Its children are topics.
    """
    def __init__(self, text: str,
                 link: str,
                 is_complete: bool = False,
                 is_parsed: bool = False,
                 children=None):
        super().__init__(text, link, is_complete, is_parsed, children)

    def __str__(self):
        return f"Category called {self._text}, link: {self._link}"

    def _unpack_children(self, data_children):
        return [Topic(**child_data) for child_data in data_children]

    def parse_data(self, session: requests.Session) -> bool:
        """
        Parses data (links and topics' names) from the category's webpage
        creating objects of class Topic.
        Note: you need to specify parameters of session variable before
        giving it to this method. For example, specify headers for the session.
        :param session:
        :return: True if parsing process succeeded, else False.
        """
        return self._parse_data(session, get_topics, Topic)


