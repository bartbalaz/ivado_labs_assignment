from typing import Optional, Tuple, List, Dict
from pandas import DataFrame, read_html, read_csv
import torch
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler


RANDOM_SEED = 89

dtype = torch.float
device = "cuda" if torch.cuda.is_available() else "cpu"


class LinearRegression(torch.nn.Module):

    def __init__(self, lr):
        super().__init__()
        self.linear_layer = torch.nn.Linear(in_features=1, out_features=1, device=device, dtype=torch.float64)
        self.to(device)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_layer(x)




def train_model(model_nn, X, Y, epochs: int, test_ratio: float):

    loss_fn = torch.nn.L1Loss()
    optimizer = torch.optim.SGD(params=model_nn.parameters(), lr=0.001)

    X = torch.FloatTensor(X).unsqueeze(dim=1)
    Y = torch.FloatTensor(Y).unsqueeze(dim=1)

    scaler = MinMaxScaler()
    X = torch.from_numpy(scaler.fit_transform(X)).to(device)
    Y = torch.from_numpy(scaler.fit_transform(Y)).to(device)
    torch.manual_seed(RANDOM_SEED)

    """
    self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, test_size= (test_ratio / 100),
                                                                            random_state=RANDOM_SEED)
    self.Y_pred = None

    self.X_train = self.X_train.to(device)
    self.X_test = self.X_test.to(device)
    self.Y_train = self.Y_train.to(device)
    self.Y_test = self.Y_test.to(device)

    """
    X_train = X.to(device)
    Y_train = Y.to(device)

    for epoch in range(epochs):
        ### Training
        model_nn.train()

        # 1. Forward pass
        Y_pred = model_nn(X_train)

        # 2. Calculate loss
        loss = loss_fn(Y_pred, Y_train)

        # 3. Zero grad optimizer
        optimizer.zero_grad()

        # 4. Loss backward
        loss.backward()

        # 5. Step the optimizer
        optimizer.step()

        """
        ### Testing
        self.eval()  # put the model in evaluation mode for testing (inference)
        # 1. Forward pass
        with torch.inference_mode():
            test_pred = self(self.X_test)

            # 2. Calculate the loss
            test_loss = self.loss(test_pred, self.Y_test)

        # if epoch % 100 == 0:
        """
        print(f"Epoch: {epoch} | Train loss: {loss} | ") #Test loss: {test_loss}


    """
    def plot(self):
        # Plot training data in blue
        plt.scatter(self.X_train, self.Y_train, c="b", s=4, label="Training")

        # Plot test data in green
        # plt.scatter(self.X_test, self.Y_test, c="g", s=4, label="Testing")

        # if self.Y_pred is not None:
            # Plot the predictions in red (predictions were made on the test data)
            #  plt.scatter(self.X_test, self.Y_pred, c="r", s=4, label="Predictions")

        # Show the legend
        plt.legend();
    """