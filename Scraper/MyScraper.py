import requests
from bs4 import BeautifulSoup


def show_topic(soup: BeautifulSoup):
    try:
        topic_name = soup.find('span', class_="topic_name")
        print('\nTopic name -> ', topic_name.text)
    except AttributeError:
        pass


def show_origin(soup):
    try:
        origin = soup.find('span', {'unbox': 'wordorigin'})
        print('\nOrigin -> ', origin.text)
    except AttributeError:
        pass


def show_definitions(soup):
    print()
    senseList = []
    senses = soup.find_all('li', class_='sense')
    for s in senses:
        definition = s.find('span', class_='def').text
        print("-", definition)

        # Examples
        examples = s.find_all('ul', class_='examples')
        for e in examples:
            show_topic(e)
            for ex in e.find_all('li'):
                print('\t-', ex.text)


def test(word_to_search: str, scrape_url: str, headers: dict):
    scrape_url = scrape_url + word_to_search

    web_response = requests.get(scrape_url, headers=headers)

    print(web_response)

    if web_response.status_code == 200:

        soup = BeautifulSoup(web_response.text, 'html.parser')
        try:

            show_origin(soup)
            show_definitions(soup)
        except AttributeError:
            print('Word not found!!')
    else:
        print('Failed to get response...')
