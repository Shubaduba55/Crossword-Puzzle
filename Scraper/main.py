import pickle
from random import uniform
import pandas as pd

import requests
from WebPage import WebPage


def load_web_page(file_name: str) -> WebPage:
    """
    Loads data from the file of given name.
    :param file_name: name of the file to read from (without file extension like .txt, .img).
    Note that file must be in data folder!!!
    :return: instance of WebPage class that has been read from the file.
    """

    webpage = WebPage()
    with open(f"./data/{file_name}.dat", "rb") as read_file:
        webpage.read_data(read_file)
        return webpage
    # TODO: add proper way to return webpage and handle errors


def save_web_page(webpage: WebPage, file_name: str):
    """
    Saves WebPage to the file of the given name. Note: file is saved to the data folder!!!
    :param webpage:
    :param file_name: name of the file to read from (without file extension like .txt, .img).
    :return:
    """

    with open(f"./data/{file_name}.dat", "wb") as write_file:
        webpage.save_data(write_file)


def create_and_save_web_page(session: requests.Session, file_name: str = "output") -> bool:
    """
    Creates WebPage and saves it. Many parameters are specified inside,
    because this class and its object have narrow purpose to access one
    and only WebPage.
    :param session:
    :param file_name: name of the file to write to (without file extension like .txt, .img).
    File is saved in data folder.
    :return: True, if data is saved, otherwise False
    """
    link = "https://www.oxfordlearnersdictionaries.com/topic/"
    text = "EnteringPoint"

    # Create WebPage, Entering Point
    webpage = WebPage(text, link)

    print(webpage)

    # Parse data
    is_success = webpage.parse_data(session)

    if is_success:
        save_web_page(webpage, file_name)

    return is_success


def parse_chosen_data(session: requests.Session, webpage: WebPage) -> bool:
    """
    Parses specific data: 1. All categories from the WebPage; 2. All the topics for specific category;
    3. All the definitions and types of words for specific category.
    :param session:
    :param webpage:
    :return: True, if process has been successful, otherwise False.
    """
    option = int(input("Choose what you want to do "
                       "\n 1. Parse all categories "
                       "\n 2. Parse topics for specific category "
                       "\n 3. Parse types of words and their definitions for specific category."
                       "\n 4. Parse types of words and their definitions for each category."
                       "\n Enter: "))

    min_delay = float(input("Enter minimal delay (float): "))
    max_delay = float(input("Enter maximal delay (float): "))
    if option == 1:
        status = webpage.parse_categories(session, min_delay, max_delay)
        print("Parsing categories status:", status)
        return status
    elif option == 2:
        status = webpage.parse_topics_for_specific_category(session, min_delay, max_delay)
        print("Parsing topics status:", status)
        return status
    elif option == 3:
        status = webpage.parse_words_for_specific_category(session, min_delay, max_delay)
        print("Parsing words' data status:", status)
        return status
    elif option == 4:
        try:
            status = webpage.parse_words_for_category(session, min_delay, max_delay)
        except ConnectionError:
            print("Connection error occured. Saving file.")
            return True
        print("Parsing words' data status:", status)
        return status
    return False


def unpack_webpage(file_name: str) -> pd.DataFrame:
    """
    Unpacks dictionary of WebPage that is stored in the given file. Note: file's name should not contain extension;
    file must be stored in the data folder.
    :param file_name: file to read from.
    :return: returns Dataframe object of pandas library.
    """

    with open(f"./data/{file_name}.dat", "rb") as file:
        webpage_dict = pickle.load(file)

    final_data = []
    categories_array = webpage_dict['children']
    for category in categories_array:
        topics_array = category['children']
        for topic in topics_array:
            words_array = topic["children"]
            for word in words_array:
                final_data.append({
                    "Category": category["text"],
                    "Topic": topic["text"],
                    "Word": word["text"],
                })

    df = pd.DataFrame(final_data)
    return df


def choose_option(headers: dict):
    """
    Function for User interaction with the program.
    :param headers: info for data parsing from browser
    :return:
    """
    option = int(input("Choose what you want to do "
                       "\n 1. Create WebPage and save it. "
                       "\n 2. Read WebPage and display its children. "
                       "\n 3. Parse data for the WebPage. "
                       "\n 4. Export WebPage data from .dat file into .csv table. "
                       "\n 5. Update words values (adds link to the oxforddictionary to the beginning)."
                       "\n 6. Run through incomplete data and finish it."
                       "\n Enter: "))
    if option == 1:
        session = requests.Session()
        session.headers.update(headers)

        file_name = str(input("Enter file name (without extension, must be in data folder): "))

        status = create_and_save_web_page(session, file_name)

        print(f"Success! Data has been saved to {file_name}.dat file." if status
              else "Failure. Data has not been parsed and saved.")

    elif option == 2:
        file_name = str(input("Enter file's name to read (without extension, must be in data folder): "))
        webpage = load_web_page(file_name)
        webpage.print_all()

    elif option == 3:
        session = requests.Session()
        session.headers.update(headers)

        file_name_read = str(input("Enter file's name which you want to use (without extension, must be in data "
                                   "folder): "))
        file_name_save = str(input("Enter file's name where you want to save data (without extension, must be in data "
                                   "folder): "))

        webpage = load_web_page(file_name_read)
        status = parse_chosen_data(session, webpage)

        if status:
            save_web_page(webpage, file_name_save)
            print(f"Success! Data has been saved to {file_name_save}.dat file.")
        else:
            print("Failure. Data has not been parsed and saved.")

    elif option == 4:
        file_name_read = str(input("Enter .dat file's name which you want to use (without extension, must be in data "
                                   "folder): "))
        file_name_save = str(input("Enter .csv file's name where you want to save data (without extension, must be in "
                                   "data folder): "))

        dataframe = unpack_webpage(file_name_read)

        dataframe.to_csv(f"./csv/{file_name_save}.csv", index=False)

    elif option == 5:
        file_name_read = str(input("Enter file's name which you want to use (without extension, must be in data "
                                   "folder): "))
        file_name_save = str(input("Enter file's name where you want to save data (without extension, must be in data "
                                   "folder): "))
        webpage = load_web_page(file_name_read)

        webpage.update_word_links()

        save_web_page(webpage, file_name_save)

    elif option == 6:
        file_name_read = str(input("Enter file's name which you want to use (without extension, must be in data "
                                   "folder): "))
        file_name_save = str(input("Enter file's name where you want to save data (without extension, must be in data "
                                   "folder): "))
        webpage = load_web_page(file_name_read)

        webpage.complete_words()

        save_web_page(webpage, file_name_save)


def main():
    # Setup headers (use: https://myhttpheader.com/)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "uk,en;q=0.9,en-GB;q=0.8,en-US;q=0.7"
    }

    choose_option(headers)


def test_word_parsing(file_path: str):
    from Word import get_word_info
    from bs4 import BeautifulSoup

    with open(file_path, "rt", encoding="utf-8") as html:
        html_lines = html.readlines()

    html_text = ""
    for line in html_lines:
        html_text += line

    soup = BeautifulSoup(html_text, "html.parser")

    print(get_word_info(soup))


if __name__ == '__main__':
    main()

    # wp = load_web_page("OUCtest")
    #
    # wp.check_if_complete()
