import pickle
import time
from random import random, uniform
from typing import BinaryIO

from Category import Category
from ParsingClasses import ParsingGroup
import requests
from bs4 import BeautifulSoup

from Topic import Topic

"""
Note for HTML file structure:
body -> div (id="main_container") -> div (class="responsive_container") -> div (class = "topic_list") ->
-> div (class = "topic-box") -> a (link) -> div (class = "topic-content") -> div (class = "topic-label") ->
-> text
"""


def get_categories(soup: BeautifulSoup) -> dict:
    """
    Gets all categories from the WebPage.
    :param soup: scraped HTML code of the page
    :return: dictionary of such template: {"Category Name": "Link to the category"}
    """
    results = {}
    try:
        all_links = soup.select('div.topic-box a')

        for link in all_links:
            try:
                category_label = link.find('div', {'class': 'topic-label'}, recursive=True)

                if category_label:
                    category_label_text = category_label.get_text(strip=True)
                    results[category_label_text] = link['href']
            except (AttributeError, TypeError) as e:
                print(f"Exception occurred: {e}")

    except Exception as e:
        print(f"Unexpected exception occurred: {e}")

    return results


class WebPage(ParsingGroup):
    """
    Class with the sole purpose to access one and only webpage (https://www.oxfordlearnersdictionaries.com/topic/).
    Its main purpose is to parse names and links to the categories on this webpage. It acts as an entering point
    for the interactions with categories, topics and words.
    """

    def __init__(self,
                 text: str = "None",
                 link: str = "None",
                 is_complete: bool = False,
                 is_parsed: bool = False,
                 children=None):
        children = [Category(**child_data) for child_data in children] if children else []
        super().__init__(text, link, is_complete, is_parsed, children)

    def __str__(self):
        return f"WebPage called {self._text}, link: {self._link}"

    def save_data(self, file_write: BinaryIO):
        """
        Saves data to the file in the form of the dictionary.
        :param file_write:
        :return:
        """
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
        """
        Reads data from the file. The data that is loaded from the file is dictionary.
        :param file_read:
        :return:
        """
        if file_read.closed:
            raise "Passed file is closed"
        data_to_restore = pickle.load(file_read)
        # print("Data to restore:", data_to_restore)
        # print("Keys in data to restore:", data_to_restore.keys())

        # Unpack dict
        self.__init__(**data_to_restore)

    def parse_data(self, session: requests.Session) -> bool:
        """
        Parses data (links and categories' names) from the oxford webpage
        creating objects of class Category.
        Note: you need to specify parameters of session variable before
        giving it to this method. For example, specify headers for the session.
        :param session:
        :return: True if parsing process succeeded, else False.
        """
        return self._parse_data(session, get_categories, Category)

    def parse_categories(self,
                         session: requests.Session,
                         min_delay: float = 0,
                         max_delay: float = 0) -> bool:
        """
        Parses topics (only topics) for each category stored in WebPage.
        :param max_delay: maximal sleep time between parsings.
        :param min_delay: minimal sleep time between parsings.
        :param session:
        :return: True if parsing process succeeded, else False.
        """

        parsing_status_successful = False
        for category in self._children:
            parsing_status_successful = category.parse_data(session)
            sleeping_time = uniform(min_delay, max_delay)
            time.sleep(sleeping_time)
            print(f"Time of our sleep: {sleeping_time}")
            if not parsing_status_successful:
                return False
        return parsing_status_successful

    def parse_topics_for_specific_category(self,
                                           session: requests.Session,
                                           min_delay: float = 0,
                                           max_delay: float = 0) -> bool:
        """
        Parses words (only words) for each topic of specified Category.
        :param max_delay: maximal sleep time between parsings.
        :param min_delay: minimal sleep time between parsings.
        :param session:
        :return: True if parsing process succeeded, else False.
        """

        parsing_status_successful = False

        category = self.display_and_choose_child()

        if isinstance(category, Category):  # Always True
            for topic in category.get_children():

                parsing_status_successful = topic.parse_data(session)
                sleeping_time = uniform(min_delay, max_delay)
                time.sleep(sleeping_time)
                print(f"Time of our sleep: {sleeping_time}")
                if not parsing_status_successful:
                    return False
            return parsing_status_successful

        return False

    def parse_words_for_specific_category(self,
                                          session: requests.Session,
                                          min_delay: float = 0,
                                          max_delay: float = 0) -> bool:
        """
        Parses words' definitions for each topic of specified Category.
        :param max_delay: maximal sleep time between parsings.
        :param min_delay: minimal sleep time between parsings.
        :param session:
        :return: True if parsing process succeeded, else False.
        """

        parsing_status_successful = False

        category = self.display_and_choose_child()

        if isinstance(category, Category):  # Always True
            topic = category.display_and_choose_child()
            if isinstance(topic, Topic):  # Always True
                for word in topic.get_children():
                    parsing_status_successful = word.parse_data(session)
                    sleeping_time = uniform(min_delay, max_delay)
                    time.sleep(sleeping_time)
                    print(f"Time of our sleep: {sleeping_time}")
                if not parsing_status_successful:
                    return False
                else:
                    topic.check_if_complete()
                    category.check_if_complete()

        self.check_if_complete()
        return parsing_status_successful

    def parse_words_for_category(self,
                                 session: requests.Session,
                                 min_delay: float = 0,
                                 max_delay: float = 0) -> bool:
        """
        Parses words' definitions for each Topic of each Category.
        :param max_delay: maximal sleep time between parsings.
        :param min_delay: minimal sleep time between parsings.
        :param session:
        :return: True if parsing process succeeded, else False.
        """

        parsing_status_successful = False
        sleeping_time = uniform(min_delay, max_delay)
        category = self.display_and_choose_child()

        if isinstance(category, Category):  # Always True
            for topic in category.get_children():
                for word in topic.get_children():
                    print(word)
                    parsing_status_successful = word.parse_data(session)
                    sleeping_time = uniform(min_delay, max_delay)
                time.sleep(sleeping_time)
                print(f"Time of our sleep: {sleeping_time}")
                if not parsing_status_successful:
                    return False
                else:
                    topic.check_if_complete()
        category.check_if_complete()

        self.check_if_complete()
        return parsing_status_successful

    def update_word_links(self):
        """
        Fixes the problem with links to Words (when they store only a part of the path
        to the source like '/definition/english/aardvark').
        :return: True if succeeded, else False.
        """
        oxford_website = 'https://www.oxfordlearnersdictionaries.com'
        for category in self._children:
            for topic in category.get_children():
                for word in topic.get_children():
                    word_link = word.get_link()
                    if word_link[:5] != "https":
                        word.set_link(oxford_website + word_link)

    def complete_words(self):
        for category in self.get_children():
            for topic in category.get_children():
                for word in topic.get_children():
                    if not word.is_complete():
                        print(word)
                        word.finish_word()
                topic.check_if_complete()
            category.check_if_complete()
        self.check_if_complete()