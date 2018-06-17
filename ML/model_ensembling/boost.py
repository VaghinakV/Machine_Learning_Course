import numpy as np

class Boost:
    
    def __init__(self, models, models_params, train_percent=80):
        self.train_percent = train_percent
        self.models = [model(**params) for model, params in zip(models, models_params)]
        self.coeffs = None
    
    
    def fit(self, X, y):
        self.coeffs = np.ones(len(self.models))
        data = np.column_stack((X, y))
        np.random.shuffle(data)
        X, y = data[:, :-1], data[:, -1]
        train_bound = int(y.shape[0] * self.train_percent / 100)
        X_train, y_train, X_test, y_test = X[:train_bound], y[:train_bound], X[train_bound:], y[train_bound:]
        for model in self.models:
            model.fit(X_train, y_train)
        S = np.absolute(np.sign(np.column_stack((model.predict(X_test) - y_test for model in self.models))))
        for i in range(len(self.models) - 1):
            y_C_exp = self._y_C_exp(S, y_test, self.coeffs[:i], self.models[:i], X_test)
            W = self._W(y_C_exp)
            W_e, min_index = min([(self._W_e(S, j, y_C_exp), j) for j in range(i + 1, len(self.models))])
            self.models[i], self.models[min_index] = self.models[min_index], self.models[i]
            S[:, i], S[:, min_index] = S[:, min_index], S[:, i]
            self.coeffs[i] = np.log((W - W_e) / W_e) / 2 
        
    
    def _W_e(self, S, index_of_model, y_C_exp):
        return (S[:, index_of_model] * y_C_exp).sum()
    
    
    def _W(self, y_C_exp):
        return y_C_exp.sum()
    
    
    def _y_C_exp(self, S, labels, coefficients, models, X):
        C = np.array([self._linear_combination(coefficients, models, x) for x in X])
        return np.exp(-labels * C)    
    
    
    def predict(self, X):
        C = np.sign(np.array([self._linear_combination(self.coeffs, self.models, x) for x in X]))
        C[C == 0] = 1
        return C
    
    
    def _linear_combination(self, coefficients, models, x):
        if not models:
            return 0
        x = np.array([x])
        predictions = np.column_stack((model.predict(x) for model in models))
        return (coefficients * predictions).sum()
