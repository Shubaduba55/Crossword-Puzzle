from random import uniform

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

    :param session:
    :param webpage:
    :return: True, if process has been successful, otherwise False.
    """
    option = int(input("Choose what you want to do "
                       "\n 1. Parse all categories "
                       "\n 2. Parse topics for specific category "
                       ""
                       "\n Enter: "))

    if option == 1:
        min_delay = float(input("Enter minimal delay (float): "))
        max_delay = float(input("Enter maximal delay (float): "))
        status = webpage.parse_categories(session, min_delay, max_delay)
        print("Parsing categories status:", status)
        return status
    elif option == 2:
        min_delay = float(input("Enter minimal delay (float): "))
        max_delay = float(input("Enter maximal delay (float): "))
        status = webpage.parse_topics_for_specific_category(session, min_delay, max_delay)
        print("Parsing categories status:", status)
        return status

    return False


def choose_option(headers: dict):
    option = int(input("Choose what you want to do "
                       "\n 1. Create WebPage and save it. "
                       "\n 2. Read WebPage and display its children. "
                       "\n 3. Parse data for the WebPage. "
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


if __name__ == '__main__':
    main()
