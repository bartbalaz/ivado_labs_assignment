from typing import Optional, Tuple, List, Dict
from pandas import DataFrame, read_html
from bs4 import BeautifulSoup
import requests
import json
import io
import re
import os

REPO_DIR = os.environ("REPO_DIR")
WORK_DIR = os.environ("WORK_DIR")


class InvalidContentFromWikipedia(Exception):
    pass

class DataNotDownloaded(Exception):
    pass

# Module data
location_overrides = { "Vatican City": ("Rome", "Italy"),
                       "Singapore": ("Singapore", "Singapore"),
                       "Washington, D.C., United States": ("Washington", "Unitesd States")}

missing_city_populations = {    "Vatican City": 825,
                                "Krakow": 766683,
                                "Rome": 2860009,
                                "Konya": 1390051,
                                "New York City": 8804190,
                                "Keelung": 362177,
                                "Taichung": 2831323,
                                "Florence": 367150,
                                "Berlin": 3850809,
                                "Edinburgh": 530990,
                                "Taipei": 2494813,
                                "Kaohsiung": 2733964,
                                "Amsterdam": 921402,
                                "Melbourne": 5031195,
                                "Changzhou": 5278121,
                                "Athens": 3059764,
                                "Vienna": 1951354,
                                "Bilbao": 345821,
                                "Marseille": 870321,
                             }



# Helper methods

def _download_table(page: str, section: int) -> DataFrame:
    print(f'Getting page {page}, section {section} from Wikipedia')
    print('1 Downloading')
    response_html = requests.get(f'https://en.wikipedia.org/w/api.php?format=json&page={page}&action=parse&prop=text&section={section}')
    response_html.raise_for_status()

    print('2 Extracting content')
    response_json = json.loads(response_html.text)
    response_content = response_json.get('parse', {}).get('text', {}).get('*', "")

    print('3 Parsing content')
    response_soup = BeautifulSoup(response_content, 'html.parser')
    response_df = read_html(io.StringIO(str(response_soup.div.table)))[0] if response_soup is not None else None

    if response_df is None:
        raise InvalidContentFromWikipedia

    print('Done')
    return response_df


def _get_location_values(location: str, custom_locations: bool) -> Tuple[str, str]:

    location_city, location_country = location_overrides.get(location, (None, None)) if custom_locations else (None,None)

    if not location_city:
        location_list = location.split(',')

        while len(location_list) < 2:
            location_list.append(None)

        while len(location_list) > 2:
            del location_list[-1]

        location_city, location_country = (tuple(location_list))

    return (location_city if location_city else '', location_country if location_country else '')


def _get_population(city_name: str, custom_population: bool) -> int:
    val_df = city_data.query("city == @city_name")
    return val_df['population'].item() if not val_df.empty else missing_city_populations.get(city_name, 0) if custom_population else 0




# Module entry point function

def download_data():
    global museum_data
    global city_data

    museum_data = _download_table('List_of_most-visited_museums', 1)
    museum_data.columns = ['name', 'location', 'visitors']

    city_data = _download_table('List_of_largest_cities', 5)
    city_data = city_data.drop(city_data.iloc[:, 3:13], axis=1)
    city_data = city_data.drop(city_data.index[0])
    city_data.columns = ['city', 'country', 'population']
    city_data = city_data.astype({'city': str, 'country': str, 'population': int })
    city_data = city_data.fillna(' ')



def create_master_data(custom_locations: bool=True, custom_population: bool=True):
    global master_data

    print('Creating master data')
    master_data=DataFrame(data = { 'name': [], 'city': [], 'country': [], 'visitors': [], 'population': [] })
    for i, row in museum_data.iterrows():
        # Get the locations
        location_city, location_country = _get_location_values(row['location'], custom_locations)
        # Get the visitors value (get rid of the commans and the trailing garbage)
        pattern = '^[0-9,]+'
        match = re.match(pattern, row['visitors'])
        visitors = int(match.group(0).replace(',','')) if match else 0
        # Get the city population
        population = _get_population(location_city, custom_population)
        master_data.loc[len(master_data)] = [row['name'], location_city, location_country, visitors, population ]
        #print(f'{row["name"]}: {location_city}, {location_country}, {visitors}, {population}')




def verify_master_data():
    print('Verifying master data')
    global master_data_issues
    master_data_issues = master_data.query("visitors == 0 or population == 0 or country =='' or not country.str.match('^[A-Za-z\ ]*$')")          # or not country.str.match('^[A-Za-z]$')")

if __name__ == '__main__':
    download_data()
    create_master_data(False, True)
    verify_master_data()
    print(master_data_issues.to_markdown())