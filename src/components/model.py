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


def plot():
    # Plot training data in blue
    plt.scatter(X_train, Y_train, c="b", s=4, label="Training")

    # Plot test data in green
    plt.scatter(X_test, Y_test, c="g", s=4, label="Testing")

    if Y_pred is not None:
        # Plot the predictions in red (predictions were made on the test data)
        plt.scatter(X_test, Y_pred, c="r", s=4, label="Predictions")

    # Show the legend
    plt.legend();

class LinearRegression(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_layer=torch.nn.Linear(in_features=1, out_features=1)
        self.loss=torch.nn.L1Loss()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_layer(x)


def learn(threshold: int = 2000000, epochs: int = 1000, test_ratio: float = 20.0):
    global X_train
    global X_test
    global Y_train
    global Y_test
    global Y_pred
    data_set = master_data.query("visitors > @threshold").sort_values(by=['visitors', 'population'], ascending=False)
    X = data_set['population'].values.tolist()
    Y = data_set['visitors'].values.tolist()

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_ratio/100, random_state=RANDOM_STATE)
    Y_pred = None


    torch.manual_seed(RANDOM_STATE)
