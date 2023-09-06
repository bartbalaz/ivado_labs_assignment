from typing import Optional, Tuple, List
from pandas import DataFrame, read_html
from bs4 import BeautifulSoup
import requests
import json
import io
import math

class InvalidContentFromWikipedia(Exception):
    pass


class OrigData:
    def __init__(self, museums_df=None, cities_df=None):
        self.museums_df = museums_df
        self.cities_df = cities_df

o = OrigData()

class  MasterData:
    def __init__(self, museums_cities_df=None):
        self.museums_cities_df = museums_cities_df

m = MasterData()

location_overrides = { "Vatican City": ("Rome", "Italy"),
                       "Singapore": ("Singapore", "Singapore"),
                       "Washingon, DC, United States": ("Washington", "Unitesd States")}

city_populations = { "Vatican City": 825,
                     "Krakow": 766683 }


# Helper methods
def _get_table(page: str, section: int ) -> DataFrame:
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

    print('4 Success')
    return response_df




def _extract_location_values(location: str, location_overrides: dict = {}) -> Tuple[str, str]:

    location_city, location_country = location_overrides.get(location, (None, None))

    if location_city is not None:
        return (location_city, location_country)

    location_list = location.split(',')

    while len(location_list) < 2:
        location_list.append(None)

    while len(location_list) > 2:
        del location_list[-1]

    return tuple(location_list)

def _get_city_population(city_name: str, cities_df: DataFrame, city_populations: dict = {}) -> int:
    val = cities_df.query("city == @city_name")
    return val['population'] if val is not None else city_populations.get('city_name', Math.nan)

# Module entry point function

def download_data():
    global o
    o = OrigData(_get_table('List_of_most-visited_museums', 1), _get_table('List_of_largest_cities', 5))

    # Set more friendly headers
    o.museums_df.columns = ['name', 'location', 'visitors']

    o.cities_df = o.cities_df.drop(o.cities_df.iloc[:,3:13], axis=1)
    o.cities_df.columns = ['city', 'country', 'population']

def create_master_data():
    global o
    global m
    global location_overrides
    global city_populations
    if o.museums_df is None or o.cities_df is None:
        print('Download data first')
        return

    m = MasterData(DataFrame(data={'name': [], 'location_city': [], 'location_country': [], 'visitors': [], 'city_population': [] }))

    for i, row in o.museums_df.iterrows():
        (location_city, location_country) = _extract_location_values(row['location'], location_overrides)
        visitors = int(row['visitors'].split('[')[0].replace(',',''))

        city_pouplation = _get_city_population(location_city, o.cities_df, city_populations)
        m.museums_cities_df[len(m.museums_cities_df)] = [row['name'], location_city, location_country, visitors, city_pouplation ]
        print((location_city if location_city is not None else "N/A") + ", " + (location_country if location_country is not None else "N/A") + ", " + str(visitors))


if __name__ == '__main__':
    download_data()
    create_master_data()
    print()