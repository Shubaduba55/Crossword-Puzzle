import requests
from WebPage import WebPage


def create_and_save_web_page(file_name: str = "output") -> bool:
    """
    Creates WebPage and saves it. Many parameters are specified inside,
    because this class and its object have narrow purpose to access one
    and only WebPage.
    :param file_name: name of the file to write to (without file extension like .txt, .img).
    File is saved in data folder.
    :return: True, if data is saved, otherwise False
    """
    link = "https://www.oxfordlearnersdictionaries.com/topic/"
    text = "EnteringPoint"

    # Create WebPage, Entering Point
    webpage = WebPage(text, link)

    print(webpage)

    # Setup session
    session = requests.Session()

    # Setup headers (use: https://myhttpheader.com/)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "uk,en;q=0.9,en-GB;q=0.8,en-US;q=0.7"
    }
    session.headers.update(headers)

    # Parse data
    is_success = webpage.parse_data(session)

    if is_success:
        with open(f"./data/{file_name}.dat", "wb") as write_file:
            webpage.save_data(write_file)

    return is_success


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


def main():
    # create_and_save_web_page()
    wp = load_web_page("output")
    print(wp)


if __name__ == '__main__':
    main()
