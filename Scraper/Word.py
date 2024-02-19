import pickle
from typing import BinaryIO

import requests
from bs4 import BeautifulSoup

from ParsingClasses import ParsingObject

"""
div.webtop span.pos -- word type
span.def -> text
"""


def get_word_info(soup: BeautifulSoup) -> dict:
    """
    Gets all definitions and additional info about Word.
    :param soup: scraped HTML code of the page
    :return: dictionary of such template: {"Word's Type": "Word's definitions"}
    """
    results = {}
    try:
        word_type = soup.select('div.webtop span.pos', limit=1)
        word_type = word_type.pop().get_text()

        # ol.senses_multiple span.def, div:not(idioms) > ol.sense_single span.def

        # maybe delete div, should be :not(class)
        words_info = soup.select('div:not(idioms) > ol.senses_multiple li.sense, :not(idioms) > '
                                 'ol.sense_single li.sense')

        results[word_type] = []
        for word_info in words_info:
            try:
                definition = word_info.select("span.def", limit=1)
                definition_text = definition.pop().get_text()
                definition_topic = word_info.select("span.topic_name", limit=1)

                if len(definition_topic) != 0:
                    topic_text = definition_topic.pop().get_text()
                    definition_text = topic_text + " //: " + definition_text
                else:
                    definition_text = "NoTopic //: " + definition_text
                results[word_type].append(definition_text)
            except (AttributeError, TypeError, IndexError) as e:
                print(f"Exception occurred: {e}")

    except Exception as e:
        print(f"Unexpected exception occurred: {e}")

    return results


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
        return (f"{self._text} {self.__word_type} \n" +
                f"{self._link} \n" +
                f"{self.__definitions}")

    def to_dict(self):
        return {
            "text": self._text,
            "link": self._link,
            "is_complete": self._is_complete,
            "word_type": self.__word_type,
            "definitions": self.__definitions
        }

    def check_if_complete(self) -> bool:
        self._is_complete = True if self.__word_type != "undefined" and len(self.__definitions) != 0 else False
        return self._is_complete

    def set_link(self, link: str):
        self._link = link

    def print_all(self, depth: int):
        for definition in self.__definitions:
            print(depth * "\t" + f"{definition}")

    def save_data(self, file_write: BinaryIO):
        if file_write.closed:
            raise "Passed file is closed"
        data_to_save = {
            "text": self._text,
            "link": self._link,
            "is_complete": self._is_complete,
            "word_type": self.__word_type,
            "definitions": self.__definitions
        }
        pickle.dump(data_to_save, file_write)

    def read_data(self, file_read: BinaryIO):
        data_to_restore = pickle.load(file_read)
        self._text = data_to_restore["text"]
        self._link = data_to_restore["link"]
        self._is_complete = data_to_restore["is_complete"]
        self.__word_type = data_to_restore["word_type"]
        self.__definitions = data_to_restore["definitions"]

    def finish_word(self):
        type = str(input("Enter type of the word (Enter to skip):"))

        if type != "":
            self.__word_type = type

            definition = "_"
            while definition != "":
                definition = str(input("Enter definition (Enter to stop): "))
                if definition == "":
                    break
                topic = str(input("Enter topic of the definition (Enter to set NoTopic): "))
                if topic == "":
                    topic = "NoTopic"
                self.__definitions.append(topic + " //: " + definition)

        option = str(input("Should be word complete? Y/N: "))
        if option == "Y":
            self._is_complete = True

    def parse_data(self, session: requests.Session) -> bool:
        """
        Parses data (words' types and definitions) from the word's webpage
        completing objects of class Word.
        Note: you need to specify parameters of session variable before
        giving it to this method. For example, specify headers for the session.
        :param session:
        :return: True if parsing process succeeded, else False.
        """
        if self._is_complete:
            return self._is_complete

        web_response = session.get(self.get_link())

        if web_response.status_code == 200:

            soup = BeautifulSoup(web_response.text, 'html.parser')

            try:
                res_dict = get_word_info(soup)
                for word_type, definitions in res_dict.items():
                    self.__word_type = word_type
                    self.__definitions = definitions

                if len(self.__definitions) != 0 and self.__word_type != 'undefined':
                    self._is_complete = True

            except AttributeError:
                print(f'{Word.__name__} not found')
        else:
            print('Failed to get response...')

        return self._is_complete
