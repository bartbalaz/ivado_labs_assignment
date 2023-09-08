from typing import Optional, Tuple, List, Dict
from pandas import DataFrame, read_html, read_csv
from bs4 import BeautifulSoup
import requests
import json
import io
import re
import os
import torch
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from components import data

WORK_DIR = os.environ.get('WORK_DIR', './')

MASTER_DATA_FILE = WORK_DIR + "/master_date.cvs"

MODEL_FILE = WORK_DIR + "/model.pth"

RANDOM_STATE = 89


class DataNotDownloaded(Exception):
    pass


# Module data
location_overrides = {"Vatican City": ("Rome", "Italy"),
                      "Singapore": ("Singapore", "Singapore"),
                      "Washington, D.C., United States": ("Washington", "Unitesd States")}

missing_city_populations = {"Vatican City": 825,
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


# Data API

def download_data():
    print('Downloading data from Wikipedia')
    global museum_data, city_data
    museum_data, city_data = data.download_data()
    print('Done')


def create_master_data(custom_locations: bool = True, custom_population: bool = True):
    print('Creating master data')
    global master_data
    master_data = data.create_master_data(museum_data, city_data, location_overrides if custom_locations else {},
                                          missing_city_populations if custom_population else {})
    print('Done')


def verify_master_data():
    print('Verifying master data')
    global master_data_issues
    master_data_issues = (
        master_data.query("visitors == 0 or population == 0 or country =='' or not country.str.match('^[A-Za-z\ ]*$')"))
    print('Done')


def save_master_data():
    print(f'Saving master_data to {MASTER_DATA_FILE}')
    master_data.to_csv(MASTER_DATA_FILE)
    print('Done')


def load_master_data():
    print(f'Loading master_data from {MASTER_DATA_FILE}')
    global master_data
    master_data = read_csv(MASTER_DATA_FILE)
    print('Done')


def print_museum_data():
    print('Museum data')
    print('-----------')
    print(museum_data.to_markdown())


def print_city_data():
    print('City data')
    print('---------')
    print(city_data.to_markdown())


def print_master_data():
    print('Master data')
    print('-----------')
    print(master_data.to_markdown())


def print_master_data_issues():
    print('Master data issues')
    print('------------------')
    print(master_data_issues.to_markdown())


def print_missing_city_populations():
    print('Missing city populations')
    print('-------------------------')
    print(missing_city_populations)


def print_location_overrides():
    print('Locations overrides')
    print('-------------------')
    print(location_overrides)


# Model API

if __name__ == '__main__':
    download_data()
    create_master_data(True, True)
    verify_master_data()
    print(master_data_issues.to_markdown())
