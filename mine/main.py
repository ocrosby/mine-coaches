# This is a sample Python script.
import bs4
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests

from mine.models.team import Team
from mine.probes import SidearmSportsProbe

import warnings
from urllib3.exceptions import InsecureRequestWarning

# Disable the warning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


def fetch_teams(division: str, gender: str):
    base_url = "http://184.73.139.41/api/v1/tds/college/teams/"
    params = {"division": division, "gender": gender}
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from the API. Status code: {response.status_code}")

    # Step 3: Parse the JSON response into a list of Team objects
    teams_data = response.json()
    teams = [Team(**team_data) for team_data in teams_data]

    return teams


def get_website_url(target_team: Team):
    """
    Given a Team this function loads it's TopDrawer page and retrieves the website URL from
    the button at the top right of the screen, labeled "Website link".
    :param target_team:
    :return:
    """
    response = requests.get(target_team.tds_url)
    response.raise_for_status()

    if response.status_code != 200:
        raise Exception(f"Failed to fetch the TopDrawer page for : {target_team.name}")

    html_content = response.content
    soup = bs4.BeautifulSoup(html_content, "html.parser")

    # Find the anchor element by its class or any other attribute
    anchor_element = soup.find('a', class_='btn tds-button', string='Website link')

    # Extract the 'href' attribute
    if anchor_element is None:
        raise Exception(f"Website link button not found for team: {target_team.name}")

    href = anchor_element.get('href')

    return href


def classify_website_url(website_url: str) -> str:
    """
    Given a website url this function will classify it as one of the following:
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

    :param website_url:
    :return:
    """
    # Load the soup from the website_url
    response = requests.get(website_url)
    response.raise_for_status()

    if response.status_code != 200:
        raise Exception(f"Failed to fetch the website page for : {website_url}")

    html_content = response.content
    soup = bs4.BeautifulSoup(html_content, "html.parser")

    sidearmsports_probe = SidearmSportsProbe(soup)

    if sidearmsports_probe.test():
        return "SidearmSports"

    return "Other"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Step 1: Retrieve the appropriate list of teams.
    division = "di"
    gender = "female"

    print("Fetching teams ...")
    teams = fetch_teams(division, gender)
    print(f"There are {len(teams)} matching teams")

    sorted_teams = sorted(teams, key=lambda team: team.name)

    # Create a dict mapping each team's name to it's website url.
    team_website_urls = {}

    print("Fetching website urls ...")
    teams_without_website_urls = []
    for team in sorted_teams:
        try:
            print(f"Fetching website url for team: {team.name}")
            team_website_urls[team.name] = get_website_url(team)
        except Exception as e:
            teams_without_website_urls.append(team)

    # Display the teams missing website URL's, something special will have to be done for
    # all of them.
    print(f"the following {len(teams_without_website_urls)} teams do not have website urls: ")
    for team in teams_without_website_urls:
        print(team.name)

    # At this point I have a dict containing mappings from team names and website urls.
    # If I were to visit each website url how would I classify each one to determine
    # what to do to extract the coach information?

    # I need a collection of strategies. Each strategy will be responsible for extracting
    # the coach information from a specific website or type of website once it has been
    # classified.

    # sidearmsports_probe = SidearmSportsProbe()

    for team in sorted_teams:
        # determine if the current team contains a website_url
        if team.name in team_website_urls:
            website_url = team_website_urls[team.name]
            print(f"Classifying website url: {website_url}")
            website_url_classification = classify_website_url(website_url)
            print(f"Classification: {website_url_classification}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
