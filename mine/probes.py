from bs4 import BeautifulSoup

from urllib.parse import urlparse


class SidearmSportsProbe:
    soup: BeautifulSoup

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def test(self) -> bool:
        """
        This function loops over all anchor elements in the soup, parsing the href from
        each one and checking if the hostname is 'www.sidearmsports.com'.  If it finds
        one it returns True otherwise it returns False.

        :return: True if the soup contents are from a SidearmSports website, False otherwise.
        """
        # Find all anchor elements
        anchor_elements = self.soup.find_all('a')

        for anchor in anchor_elements:
            href = anchor.get('href')

            if href:
                # Parse the href URL
                parsed_url = urlparse(href)

                # Check if the hostname is 'www.sidearmsports.com'
                if parsed_url.hostname == 'www.sidearmsports.com':
                    return True

        return False
