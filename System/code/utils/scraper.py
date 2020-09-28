import re
import sys
from contextlib import closing

import math
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def main():
    for language in ['Gujarati', 'Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi', 'Punjabi', 'Malayalam', 'Kannada', 'Oriya', 'Urdu']:
        for gender in ['Boy', 'Girl']:
            with open(language + ".txt", 'w', encoding='utf-8') as file:
                for char in range(ord('A'), ord('Z') + 1):
                    count = 0
                    num = 1
                    site = "https://www.bachpan.com/" + language + "-" + gender + "-Names-" + chr(
                        char) + ".aspx?page=" + str(num)
                    soup = BeautifulSoup(simple_get(site), 'html.parser')

                    nPages = soup.find('span',
                                       attrs={'style': 'float: left; vertical-align: top; padding: 5px 5px 5px 5px;'})

                    if nPages:
                        num = math.ceil(int(re.search("\\sof\\s(\\d+)", str(nPages)).group(1))/100.0)
                        for i in range(1, num + 1):

                            site = "https://www.bachpan.com/" + language + "-" + gender + "-Names-" + chr(
                                char) + ".aspx?page=" + str(i)
                            soup = BeautifulSoup(simple_get(site), 'html.parser')
                            table = soup.find_all('td', attrs={'class': 'c1'})
                            for row in table:
                                name = re.search("<[^>]+>(\\w+)[^>]+>([^<\\|^&]+)", str(row))
                                if name:
                                    file.write(name.group(1) + '\t' + name.group(2) + '\n')
                                    count += 1

                    file.flush()
                    print("Downloading {}:{}:{}:{}".format(language, gender, chr(char), count))


if __name__ == "__main__":
    sys.exit(main())
