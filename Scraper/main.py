from MyScraper import test
from WebPage import WebPage


def create_web_page():
    link = "https://www.oxfordlearnersdictionaries.com/topic/"
    text = "EnteringPoint"
    webpage = WebPage(text, link)

    print(webpage)
    webpage.parse_data()


def main():
    word_to_search = "boxer"
    scrape_url = "https://www.oxfordlearnersdictionaries.com/definition/english/"
    headers = {"User-Agent": ""}

    test(word_to_search, scrape_url, headers)


if __name__ == '__main__':
    create_web_page()



