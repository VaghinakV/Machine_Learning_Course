import numpy as np

class LogisticRegression:

    def __init__(self, learning_rate=0.01):
        self._weights = []
        self._learning_rate = learning_rate


    def fit(self, X, y):
        self._weights = []
        data = self._add_ones_column(X)
        for i in np.unique(y):
            binary_labels = y.copy()
            binary_labels[y == i] = 1
            binary_labels[y != i] = -1
            self._weights.append(self._fit_binary(data, binary_labels))


    def _fit_binary(self, X, y):
        b = np.zeros(X.shape[1])
        indices = np.arange(y.shape[0])
        np.random.shuffle(indices)
        for i in indices:
            b -= self._learning_rate * self._gradient(y[i], X[i], b)
        return b


    def predict(self, X):
        data = self._add_ones_column(X)
        return np.array([self._predict_single_data(feature) for feature in data])


    def _predict_single_data(self, features):
        predictions = [self._sigmoid(features, weight) for weight in self._weights]
        return predictions.index(max(predictions))


    def _gradient(self, y, x, b):
        return -y*x * (1 - self._sigmoid(y*x, b))


    def _sigmoid(self, x, b):
        return 1 / (1 + np.exp(-np.dot(b, x)))


    def _add_ones_column(self, X):
        return np.concatenate((np.array(np.ones(X.shape[0]))[:, np.newaxis], X), axis=1)