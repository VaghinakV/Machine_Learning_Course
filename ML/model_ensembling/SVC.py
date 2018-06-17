import numpy as np
from cvxopt import matrix, solvers

class SVC:
    def __init__(self, C=1.0, kernel='rbf', degree=3, gamma=1.0, coef=0.0, use_bias=False):
        self._C = C
        self._degree = degree
        self._gamma = gamma
        self._coef = coef
        self._use_bias = use_bias
        self._alphas = None
        self._bias = None
        self._data = None
        self._labels = None
        self._N = None
        self._choose_kernel(kernel)
        
        
    def fit(self, X, y):
        self._N = X.shape[0]
        self._data = X
        self._labels = y
        q = matrix(np.ones(self._N))
        kernel_matrix = self._make_kernel_matrix()
        P = matrix(kernel_matrix)
        A = matrix(y, (1, self._N))
        b = matrix(0.0)
        G = matrix(np.concatenate((-np.eye(self._N), np.eye(self._N))))
        h = matrix(np.pad(np.zeros(self._N), (0, self._N), mode='constant', constant_values=self._C))
        self._alphas = np.array(solvers.qp(P, q, G, h, A, b)['x']).flatten()
        self._bias = self._calc_bias(kernel_matrix) if self._use_bias else 0.0
    
    
    def predict(self, X):
        return np.array([self._single_prediction(element) for element in X])
    
    
    def _single_prediction(self, data_to_predict):
        kernels = self._vectorized_kernel(data_to_predict, self._data)
        w_fi_product = (self._alphas * self._labels * kernels).sum()
        return 1 if w_fi_product + self._bias >= 0 else -1 
    
    
    def _make_kernel_matrix(self):
        P = np.zeros((self._N, self._N))
        for i in np.arange(self._N):
            for j in np.arange(i, self._N):
                P[i, j] = self._labels[i] * self._labels[j] * self._kernel(self._data[i], self._data[j])
        lower_triangle = np.tril_indices(self._N, -1)
        P[lower_triangle] = P.T[lower_triangle]
        return P
    
    
    def _calc_bias(self, P):
        return np.mean(np.array([self._labels[i] - (self._alphas * self._labels * P[i]).sum() for i in np.arange(self._N)]))


    def _choose_kernel(self, kernel):
        if kernel == 'linear':
            self._kernel = self._linear_kernel
        elif kernel == 'rbf':
            self._kernel = self._rbf_kernel
        elif kernel == 'poly':
            self._kernel = self._poly_kernel
        elif kernel == 'sigmoid':
            self._kernel = self._sigmoid_kernel
        else:
            raise NameError('Wrong kernel')
        self._vectorized_kernel = np.vectorize(self._kernel, signature='(i),(i)->()')
    
    
    def _linear_kernel(self, x, y):
        return np.dot(x, y)
    
    
    def _rbf_kernel(self, x, y):
        return np.exp(-self._gamma * np.linalg.norm(x - y)**2)


    def _poly_kernel(self, x, y):
        return (self._gamma * np.dot(x, y) + self._coef)**self._degree
    
    
    def _sigmoid_kernel(self, x, y):
        return np.tanh((self._gamma * np.dot(x, y) + self._coef))