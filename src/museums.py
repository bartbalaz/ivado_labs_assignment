from typing import List
import pickle
from pandas import read_csv
import os
from src.components import data, model
import importlib

# To force reload of data and model components upon a reload of this module
importlib.reload(data)
importlib.reload(model)

# Default values and parameters
DATA_DIR = os.environ.get('DATA_DIR', './')

MASTER_DATA_FILE = DATA_DIR + "/master_data.cvs"

MODEL_FILE = DATA_DIR + "/model.pt"

LEARNING_RATE = 0.0001

class FileDoesNotExist(Exception):
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
    print('\nDownloading data from Wikipedia')
    print('-------------------------------')
    global museum_data, city_data
    museum_data, city_data = data.download_data()
    print('\nDone')


def create_master_data(custom_locations: bool = True, custom_population: bool = True):
    print('\nCreating master data')
    print('--------------------')
    global master_data
    master_data = data.create_master_data(museum_data, city_data, location_overrides if custom_locations else {},
                                          missing_city_populations if custom_population else {})
    print('\nDone')


def verify_master_data():
    print('\nVerifying master data')
    print('---------------------')
    global master_data_issues
    master_data_issues = (
        master_data.query("visitors == 0 or population == 0 or country =='' or not country.str.match('^[A-Za-z\ ]*$')"))
    print('\nDone')


def save_master_data(master_data_file: str = MASTER_DATA_FILE):
    print(f'\nSaving master_data to {master_data_file}')
    print('------------------------')
    master_data.to_csv(master_data_file)
    print('\nDone')


def load_master_data(master_data_file: str = MASTER_DATA_FILE):
    print(f'\nLoading master_data from {master_data_file}')
    print('--------------------------------')
    if not os.path.exists(master_data_file):
        raise FileDoesNotExist
    global master_data
    master_data = read_csv(master_data_file)
    print('\nDone')


def print_museum_data():
    print('\nMuseum data')
    print('-----------')
    print(museum_data.to_markdown())
    print('\nDone')


def print_city_data():
    print('\nCity data')
    print('---------')
    print(city_data.to_markdown())
    print('\nDone')


def print_master_data():
    print('\nMaster data')
    print('-----------')
    print(master_data.to_markdown())
    print('\nDone')


def print_master_data_issues():
    print('\nMaster data issues')
    print('------------------')
    print(master_data_issues.to_markdown())
    print('\nDone')


def print_missing_city_populations():
    print('\nMissing city populations')
    print('-------------------------')
    print(missing_city_populations)
    print('\nDone')


def print_location_overrides():
    print('\nLocations overrides')
    print('-------------------')
    print(location_overrides)
    print('\nDone')


# Model API
def create_model(lr = LEARNING_RATE):
    print('\nCreating model')
    print('--------------')
    global nn_model
    nn_model = model.LinearRegression(lr)
    print('Model parameters')
    print(nn_model)
    print(f'Device: {next(nn_model.parameters()).device}')
    print('Model state')
    print(str(nn_model.state_dict()))
    print('\nDone')


def train_model(threshold: int = 2000000, epochs: int = 20000, test_ratio: int = 20):
    print('\nTraining')
    print('--------')

    data_set = master_data.query("visitors > @threshold").sort_values(by=['visitors', 'population'],
                                                                      ascending=False)
    X = data_set['population'].values.tolist()
    Y = data_set['visitors'].values.tolist()

    nn_model.train_model(X,Y, epochs, test_ratio)
    print('\nDone')


def plot_training():
    nn_model.plot_training()


def print_training():
    print('Training summary')
    print('----------------')
    nn_model.print_training()
    print('\nDone')


def evaluate(vector: List[int]):
    print('Evaluating')
    print('----------')
    print(f'Input: {str(vector)}')
    print(f'Output: {str(nn_model.evaluate(vector))}')
    print('\nDone')


def save_model(model_file: str = MODEL_FILE):
    print(f'Saving model to {model_file}')
    print('---------------------')
    with open(model_file, 'wb') as f:
        pickle.dump(nn_model, f)
    f.close()
    print('\nDone')


def load_model(model_file: str = MODEL_FILE):
    print(f'Loading model from {model_file}')
    print('---------------------')
    global nn_model
    if not os.path.exists(model_file):
        raise FileDoesNotExist
    with open(model_file, 'rb') as f:
        nn_model = pickle.load(f)
    f.close()
    print('\nDone')


if __name__ == '__main__':
    download_data()
    create_master_data(True, True)
    verify_master_data()
    create_model()
    train_model(epochs=1000, test_ratio=10)
    evaluate([1000000, 2000000])
