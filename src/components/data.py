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
    print('1 Downloading')
    response_html = requests.get(
        f'https://en.wikipedia.org/w/api.php?format=json&page={page}&action=parse&prop=text&section={section}')
    response_html.raise_for_status()

    print('2 Extracting content')
    response_json = json.loads(response_html.text)
    response_content = response_json.get('parse', {}).get('text', {}).get('*', "")

    print('3 Parsing content')
    response_soup = BeautifulSoup(response_content, 'html.parser')
    response_df = read_html(io.StringIO(str(response_soup.div.table)))[0] if response_soup is not None else None

    if response_df is None:
        raise InvalidContentFromWikipedia

    return response_df


def _get_location_values(location: str, location_overrides: Dict) -> Tuple[str, str]:
    location_city, location_country = location_overrides.get(location, (None, None))

    if not location_city:
        location_list = location.split(',')

        while len(location_list) < 2:
            location_list.append(None)

        while len(location_list) > 2:
            del location_list[-1]

        location_city, location_country = (tuple(location_list))

    return (location_city if location_city else '', location_country if location_country else '')


def _get_population(city_name: str, city_data: DataFrame, missing_city_populations: bool) -> int:
    val_df = city_data.query("city == @city_name")
    return val_df['population'].item() if not val_df.empty else missing_city_populations.get(city_name, 0)


# API methods

def download_data() -> Tuple[DataFrame, DataFrame]:
    museum_data = _download_table('List_of_most-visited_museums', 1)
    museum_data.columns = ['name', 'location', 'visitors']

    city_data = _download_table('List_of_largest_cities', 5)
    city_data = city_data.drop(city_data.iloc[:, 3:13], axis=1)
    city_data = city_data.drop(city_data.index[0])
    city_data.columns = ['city', 'country', 'population']
    city_data = city_data.astype({'city': str, 'country': str, 'population': int})
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