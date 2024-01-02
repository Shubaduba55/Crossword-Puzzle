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
        super().__init__(text, link, is_complete, is_parsed, children)

    def __str__(self):
        return f"WebPage called {self._text}, link: {self._link}"

    def _unpack_children(self, data_children) -> list:
        # print("Data for unpacking children:", data_children)
        return [Category(**child_data) for child_data in data_children]

    def parse_data(self, session: requests.Session) -> bool:
        """
        Parses data (links and categories' names) from the oxford webpage
        creating objects of class Category.
        Note: you need to specify parameters of session variable before
        giving it to this method. For example, specify headers for the session.
        :param session:
        :return: True if parsing process succeeded, else False.
        """
        if self._is_parsed:
            return self._is_parsed

        web_response = session.get(self.get_link())

        if web_response.status_code == 200:

            soup = BeautifulSoup(web_response.text, 'html.parser')

            try:

                res_dict = get_categories(soup)
                for category_name, link in res_dict.items():
                    self._children.append(Category(category_name, link))

                if len(self._children) != 0:
                    self._is_parsed = True

            except AttributeError:
                print('Categories not found')
        else:
            print('Failed to get response...')

        return self._is_parsed
