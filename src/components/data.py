from typing import Tuple, Dict
from pandas import DataFrame, read_html
from bs4 import BeautifulSoup
import requests
import json
import io
import re

class InvalidContentFromWikipedia(Exception):
    pass

# Helper methods

def _download_table(page: str, section: int) -> DataFrame:
    print(f'Getting page {page}, section {section} from Wikipedia')

    # Query Wikipedia
    print('1 Downloading')
    response_html = requests.get(
        f'https://en.wikipedia.org/w/api.php?format=json&page={page}&action=parse&prop=text&section={section}')
    # Raise an exception upon HTTP/IP layer failure
    response_html.raise_for_status()

    # Translate response into a dict
    print('2 Extracting content')
    response_json = json.loads(response_html.text)
    # Find the "parse.text.*" element if it exists
    response_content = response_json.get('parse', {}).get('text', {}).get('*', "")

    print('3 Parsing content')
    # Parse the HTML content
    response_soup = BeautifulSoup(response_content, 'html.parser')
    # Load the HTML DOM content of <div><table> into io.StringIO()
    if response_soup and response_soup.div and response_soup.div.table:
        response_df = read_html(io.StringIO(str(response_soup.div.table)))[0]
    else:
        response_df = None

    if response_df is None:
        raise InvalidContentFromWikipedia

    return response_df


def _get_location_values(location: str, location_overrides: Dict) -> Tuple[str, str]:
    location_city, location_country = location_overrides.get(location, (None, None))

    # If the location value is not overriden (cannot be found in location_overrides)
    if not location_city:

        # Split the availabel value using commas
        location_list = location.split(',')

        # If the list is too small add a None
        while len(location_list) < 2:
            location_list.append(None)

        # If the list is too long trim to 2 elements
        while len(location_list) > 2:
            del location_list[-1]

        # Create a tuple
        location_city, location_country = (tuple(location_list))

    # Return a tuple with strings having removed heading or trailing white spaces or empty strings if values unavailable
    return (location_city.lstrip().rstrip() if location_city else '',
            location_country.lstrip().rstrip() if location_country else '')


def _get_population(city_name: str, city_data: DataFrame, missing_city_populations: Dict) -> int:
    val_df = city_data.query("city == @city_name")
    return val_df['population'].item() if not val_df.empty else missing_city_populations.get(city_name, 0)


# API methods

def download_data() -> Tuple[DataFrame, DataFrame]:
    # Museum data
    museum_data = _download_table('List_of_most-visited_museums', 1)
    # Add our header
    museum_data.columns = ['name', 'location', 'visitors']

    # City data
    city_data = _download_table('List_of_largest_cities', 5)
    # Remove unnecessary columns
    city_data = city_data.drop(city_data.iloc[:, 3:13], axis=1)
    # Remove parsed header
    city_data = city_data.drop(city_data.index[0])
    # Add our header
    city_data.columns = ['city', 'country', 'population']
    # Force our types
    city_data = city_data.astype({'city': str, 'country': str, 'population': int})
    # Ensure the missing values are blank strings
    city_data = city_data.fillna(' ')

    return museum_data, city_data


def create_master_data(museum_data: DataFrame, city_data: DataFrame,
                       location_overrides: Dict, missing_city_populations: Dict) -> DataFrame:
    master_data = DataFrame(data={'name': [], 'city': [], 'country': [], 'visitors': [], 'population': []})
    for i, row in museum_data.iterrows():
        # Get the locations
        location_city, location_country = _get_location_values(row['location'], location_overrides)
        # Get the visitors value (get rid of the commas and the trailing characters)
        pattern = '^[0-9,]+'
        match = re.match(pattern, row['visitors'])
        visitors = int(match.group(0).replace(',', '')) if match else 0
        # Get the city population
        population = _get_population(location_city, city_data, missing_city_populations)
        master_data.loc[len(master_data)] = [row['name'], location_city, location_country, visitors, population]
        # print(f'{row["name"]}: {location_city}, {location_country}, {visitors}, {population}')

    return master_data