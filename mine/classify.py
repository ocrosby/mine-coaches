import bs4
import requests
import utils
from probes import SidearmSportsProbe, TopDrawerSoccerProbe, PrestoSportsProbe

from bs4 import BeautifulSoup


class WebsiteClassifier:
    """
    This class helps to classify a website based on the contents of the soup.

    Given a website url this function will classify.py it as one of the following:
    - TopDrawerSoccer
    - PrestoSports
    - SidearmSports
    - Other

    The process of classifying a website url will be done by attempting to load the page
    and then looking for specific elements on the page that are unique to each of the
    above categories.  In order to modularize the process I will create a set of Probes
    each one will be responsible for probing a page for identifying elements.

    This make take some iteration to determine the set of all classifications that are
    required to effectively return coaching information consistently across the NCAA.

    Game on!
    """
    def __init__(self):
        pass

    def classify(self, website_url: str) -> str:
        try:
            # Load the soup from the website_url
            final_url = utils.follow_redirections(website_url, 5)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            response = requests.get(final_url, headers=headers)  # Some sites require the User-Agent header
            response.raise_for_status()
            if response.status_code != 200:
                raise Exception(f"Failed to fetch the website page for: {final_url}")

            html_content = response.content
            soup = bs4.BeautifulSoup(html_content, "html.parser")

            probes = [
                SidearmSportsProbe(soup),
                TopDrawerSoccerProbe(soup),
                PrestoSportsProbe(soup)
                # Add more probes as needed
            ]

            for probe in probes:
                if probe.test():
                    return probe.__class__.__name__

            return "Other"
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return "Other"
        except Exception as e:
            print(f"Error classifying website url: {website_url}")
            print(e)
            return "Other"


if __name__ == "__main__":
    classifier = WebsiteClassifier()

    website_url = ""
    classification = classifier.classify(website_url)

    print(f"Classification: {classification}")
