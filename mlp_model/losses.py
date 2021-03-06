
import numpy as np
from abc import abstractmethod


class Loss:
    """
    Base class for loss function for prediction error
    """

    @abstractmethod
    def forward(self, actual: np.array, prediction: np.array) -> np.array:
        pass

    @abstractmethod
    def derivate(self, actual: np.array, prediction: np.array) -> np.array:
        pass


class MSE(Loss):
    """
    Class that implements Mean Squared Error
    """

    def __init__(self):
        self.type = "mse"

    def forward(self, actual: np.array, prediction: np.array) -> np.array:
        """
        Compute MSE error between target and prediction
        :param actual: target vector (type: np.array)
        :param prediction: predictions vector (type: np.array)
        :return: vector containing element-wise MSE 
        """
        return 0.5 * ((prediction - actual) ** 2)

    def derivate(self, actual: np.array, prediction: np.array) -> np.array:
        """
        Compute the derivative of MSE error 
        :param actual: target vector (type: np.array)
        :param prediction: predictions vector (type: np.array)
        :return: vector containing element-wise derivative of MSE 
        """
        return prediction - actual


class MAE(Loss):
    """
    Class that implements Mean Absolute Error
    """

    def __init__(self):
        self.type = "mae"

    def forward(self, actual: np.array, prediction: np.array) -> np.array:
        """
        Compute MAE error between target and prediction
        :param actual: target vector (type: np.array)
        :param prediction: predictions vector (type: np.array)
        :return: vector containing element-wise MAE 
        """
        return np.abs(prediction - actual)

    def derivate(self, actual: np.array, prediction: np.array) -> np.array:
        """
        Compute the derivative of MAE 
        :param actual: target vector (type: np.array)
        :param prediction: predictions vector (type: np.array)
        :return: vector containing element-wise derivative of MAE 
        """
        return np.where(prediction - actual > 0, 1, -1)


class Logloss(Loss):
    """
    Class that implements Logloss Error
    """

    def __init__(self):
        """
        Initialize logloss object
        eps is a small number to avoid extreme values in predictions of 0 and 1
        """
        self.type = "logloss"
        self._eps = 1e-15

    def forward(self, actual: np.array, prediction: np.array) -> np.array:
        """
        Compute Logloss error between targt and prediction
        :param actual: target vector (type: np.array)
        :param prediction: predictions vector (type: np.array)
        :return: vector containing element-wise Logloss
        """

        # Clip prediction to avioid 0 and 1
        prediction = np.clip(prediction, self._eps, 1 - self._eps)

        return -(actual * np.log(prediction) + (1 - actual) * np.log(1 - prediction))

    def derivate(self, actual: np.array, prediction: np.array) -> np.array:
        """
        Compute the derivative of Logloss error 
        :param actual: target vector (type: np.array)
        :param prediction: predictions vector (type: np.array)
        :return: vector containing element-wise derivative of Logloss
        """

        # Clip prediction to avioid 0 and 1
        prediction = np.clip(prediction, self._eps, 1 - self._eps)
        return -(actual / prediction) + ((1 - actual) / (1 - prediction))


class Quantile(Loss):
    """
    Class that implements Quantile Loss
    """

    def __init__(self, q: float = 0.5):
        """
        Initialize quantile loss object
        :param q: quantile for which we want to cumpute the loss (type: float)
        """
        self.type = "quantile"
        self.q = q

    def forward(self, actual: np.array, prediction: np.array) -> np.array:
        """
        Compute quantile loss for an especific quantile
        
        :param actual: target vector (type: np.array)
        :param prediction: predictions vector (type: np.array)
        :return: vector containing element-wise derivative of Logloss
        """

        e = actual - prediction

        return np.maximum(self.q * e, (self.q - 1) * e)

    def derivate(self, actual: np.array, prediction: np.array) -> np.array:
        """
        Compute the derivative of quantile loss
        :param actual: target vector (type: np.array)
        :param prediction: predictions vector (type: np.array)
        :return: vector containing element-wise derivative of Logloss
        """

        e = actual - prediction
        q_loss = np.where(e > 0, -self.q, 1 - self.q)
        return q_loss
