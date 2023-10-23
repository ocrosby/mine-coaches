# This is a sample Python script.
import bs4
import pickle

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests

from typing import Dict, List, Tuple

from mine.models.team import Team
from mine.probes import SidearmSportsProbe, TopDrawerSoccerProbe, PrestoSportsProbe

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


def follow_redirections(url):
    max_redirects = 5  # You can adjust the maximum number of redirects
    for _ in range(max_redirects):
        response = requests.get(url, allow_redirects=False)
        if 300 <= response.status_code < 400:
            location = response.headers.get('Location')
            if location:
                url = location
            else:
                break
        else:
            break
    return url


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
    try:
        # Load the soup from the website_url
        final_url = follow_redirections(website_url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(final_url, headers=headers) # Some sites require the User-Agent header
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


def save_state(state, checkpoint_file):
    with open(checkpoint_file, 'wb') as file:
        pickle.dump(state, file)


def load_state(checkpoint_file):
    with open(checkpoint_file, 'rb') as file:
        return pickle.load(file)


# Press the green button in the gutter to run the script.
def original():
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


def extract_website_urls(teams: List[Team]) -> Tuple[Dict[str, str], List[Team]]:
    team_website_urls = {}

    problem_teams = []
    for team in teams:
        print(f"Fetching website url for team: {team.name}")

        try:
            team_website_urls[team.name] = get_website_url(team)
        except Exception as e:
            problem_teams.append(team)
            print(f"Error fetching website url for team: {team.name}")
            print(e)

    return (team_website_urls, problem_teams)


def main(division: str, gender: str):
    checkpoint1_file = 'checkpoint1.pkl'
    checkpoint2_file = 'checkpoint2.pkl'
    checkpoint3_file = 'checkpoint3.pkl'

    # Try to load checkpoint1 (teams data) first
    try:
        teams = load_state(checkpoint1_file)
        print("Resuming from checkpoint 1 (teams data). Current state:")
        for team in teams:
            print(team)

        print(f"Loaded {len(teams)} teams.")
    except FileNotFoundError:
        # If checkpoint 1 doesn't exist, fetch the teams and create the initial state
        teams = fetch_teams(division='di', gender='female')
        print("Fetched initial teams data.")
        for team in teams:
            print(team)

        print(f"Fetched {len(teams)} teams.")

        save_state(teams, checkpoint1_file)
        print("Checkpoint 1 (teams data) created.")

    # Process checkpoint2 (website URLs) based on the data from checkpoint1
    try:
        website_urls = load_state(checkpoint2_file)
        print("Resuming from checkpoint 2 (website URLs). Current state:")
        for school_name in website_urls:
            print(f"Website URL: {school_name} -> '{website_urls[school_name]}'")
    except FileNotFoundError:
        # If checkpoint 2 doesn't exist, extract website URLs based on checkpoint1 data
        website_urls, problem_teams = extract_website_urls(teams)
        print("Extracted website URLs for teams.")
        for school_name in website_urls:
            print(f"Website URL: {school_name} -> '{website_urls[school_name]}'")
        save_state(website_urls, checkpoint2_file)
        print("Checkpoint 2 (website URLs) created.")

    # Process checkpoint3 (website classifications) based on the data from checkpoint2
    try:
        website_classifications = load_state(checkpoint3_file)
        print("Resuming from checkpoint 3 (website classifications). Current state:")
        for school_name in website_classifications:
            print(f"Website classification: {school_name} -> '{website_classifications[school_name]}'")
    except FileNotFoundError:
        # If checkpoint 3 doesn't exist, classify website URLs based on checkpoint2 data
        website_classifications = {}
        for school_name in website_urls:
            try:
                website_url = website_urls[school_name]
                print(f"Classifying website url: {website_url}")

                # During the process of classification it is possible that an exception will be thrown
                # I am noticing that several of the URL's from TopDrawerSoccer are not valid.

                # What should I do for those cases?
                # First I want to log the error so I can see what the problem is.
                # I would also like a file that contains the name of the school and the URL that caused
                # the error.
                classification = classify_website_url(website_url)

                website_classifications[school_name] = classification
                print(f"Classification: {website_classifications[school_name]}")
            except Exception as e:
                print(f"Error classifying website url: {website_url}")
        save_state(website_classifications, checkpoint3_file)
        print("Checkpoint 3 (website classifications) created.")


if __name__ == "__main__":
    division = "di"
    gender = "female"

    main(division, gender)
