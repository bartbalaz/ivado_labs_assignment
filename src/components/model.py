from typing import List
from pandas import DataFrame
import torch
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

class InvaidEpochs(Exception):
    pass

# Set a seed for consistent
RANDOM_SEED = 89

# Detect device type
dtype = torch.float
device = "cuda" if torch.cuda.is_available() else "cpu"


class LinearRegression(torch.nn.Module):

    def __init__(self, lr):
        super().__init__()
        torch.manual_seed(RANDOM_SEED)

        self.linear_layer = torch.nn.Linear(in_features=1, out_features=1, device=device, dtype=torch.float64)
        self.to(device)
        self.loss_fn = torch.nn.L1Loss()
        self.lr = lr
        self.optimizer = torch.optim.SGD(params=self.parameters(), lr=self.lr)
        self.scaler_x, self.scaler_y = MinMaxScaler(), MinMaxScaler()


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_layer(x)


    def train_model(self, x_in: List[int], y_in: List[int], threshold: int, epochs: int, test_ratio: int):
        self.to(device)
        self.training_params = f't: {threshold}, s: {len(x_in)}, e: {epochs}, r: {test_ratio}%, lr: {self.lr}'
        print(f'Parameters: {self.training_params}')

        if epochs <= 0:
            raise InvaidEpochs

        x = torch.FloatTensor(x_in).unsqueeze(dim=1)
        y = torch.FloatTensor(y_in).unsqueeze(dim=1)

        x = torch.from_numpy(self.scaler_x.fit_transform(x))
        y = torch.from_numpy(self.scaler_y.fit_transform(y))

        if test_ratio > 0:
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size= float(test_ratio / 100),
                                                                                    random_state=RANDOM_SEED)
            self.x_train = self.x_train.to(device)
            self.y_train = self.y_train.to(device)
            self.x_test = self.x_test.to(device)
            self.y_test = self.y_test.to(device)
        else:
            self.x_train = x.to(device)
            self.y_train = y.to(device)
            self.x_test = None
            self.y_test = None

        self.y_pred = None

        self.training_run = DataFrame(data={'epoch': [], 'training_loss': [], 'test_loss': [] })

        for epoch in range(epochs):
            ### Training
            self.train()

            # Forward pass
            y_pred = self(self.x_train)

            # Loss
            loss = self.loss_fn(y_pred, self.y_train)

            # Zero grad optimizer
            self.optimizer.zero_grad()

            # Loss backward
            loss.backward()

            # Step the optimizer
            self.optimizer.step()

            if test_ratio > 0:
                ### Testing
                self.eval()  # put the model in evaluation mode for testing (inference)
                # Forward pass
                with torch.inference_mode():
                    self.y_pred = self(self.x_test)

                    # Calculate the loss
                    test_loss = self.loss_fn(self.y_pred, self.y_test)

            if epoch % (epochs / 10) == 0:
                if test_ratio > 0:
                    test_loss = test_loss.cpu()
                else:
                    test_loss = 0

                print(f"Epoch: {epoch} | Train loss: {loss} | Test loss: {test_loss} ")
                self.training_run.loc[len(self.training_run)] = [ epoch, loss.cpu().detach().numpy(), test_loss ]

        # Sweep test
        self.x_sweep = torch.from_numpy(self.scaler_x.transform(torch.FloatTensor(range(min(x_in), max(x_in), 1000)).unsqueeze(dim=1))).to(device)
        self.eval()
        with torch.inference_mode():
            self.y_sweep = self(self.x_sweep)

        # De-scale after training
        self.x_sweep = self.scaler_x.inverse_transform(self.x_sweep.cpu())
        self.y_sweep = self.scaler_y.inverse_transform(self.y_sweep.cpu())

        if test_ratio > 0:
            self.x_train = self.scaler_x.inverse_transform(self.x_train.cpu())
            self.y_train = self.scaler_y.inverse_transform(self.y_train.cpu())
            self.x_test = self.scaler_x.inverse_transform(self.x_test.cpu())
            self.y_test = self.scaler_y.inverse_transform(self.y_test.cpu())
        else:
            self.x_train = self.scaler_x.inverse_transform(self.x_train.cpu())
            self.y_train = self.scaler_y.inverse_transform(self.y_train.cpu())

        if self.y_pred is not None:
            self.y_pred = self.scaler_y.inverse_transform(self.y_pred.cpu())

    def plot_training(self):
        fig, axs = plt.subplots(2, 1, figsize=(12, 12))
        fig.suptitle(f'Training params: {self.training_params}')
        axs[0].scatter(self.x_train, self.y_train, c="b", s=4, label="Training")
        axs[0].scatter(self.x_sweep, self.y_sweep, c="y", s=4, label="Sweep")
        if self.x_test is not None:
            axs[0].scatter(self.x_test, self.y_test, c="g", s=4, label="Testing")
        if self.y_pred is not None:
            axs[0].scatter(self.x_test, self.y_pred, c="r", s=4, label="Testing predictions")
        axs[0].legend()
        axs[1].plot(self.training_run['training_loss'].values, c='b', label='Training loss')
        axs[1].plot(self.training_run['test_loss'].values, c='g', label='Testing loss')
        axs[1].legend()

    def print_training(self):
        print('Parameters:')
        print(self.training_params)
        print(self.training_run.to_markdown())

    def evaluate(self, vector: List[int]) -> List[int]:
        self.to(device)
        vector = torch.from_numpy(self.scaler_x.transform(torch.FloatTensor(vector).unsqueeze(dim=1))).to(device)
        self.eval()
        with torch.inference_mode():
            result = self(vector).cpu()

        r = self.scaler_y.inverse_transform(result).squeeze().tolist()

        return r
