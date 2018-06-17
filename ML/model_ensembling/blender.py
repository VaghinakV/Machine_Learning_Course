import numpy as np

class Blender:

    def __init__(self, train_percent, 
                 base_models, models_params,
                 blender_model, blender_params):
        self.train_percent = train_percent
        self.blender_model = blender_model(**blender_params)
        self.base_models = [model(**params) for model, params in zip(base_models, models_params)]
    

    def fit(self, X, y):
        data = np.column_stack((X, y))
        np.random.shuffle(data)
        X, y = data[:, :-1], data[:, -1]
        train_bound = int(y.shape[0] * self.train_percent / 100)
        X_train, y_train, X_test, y_test = X[:train_bound], y[:train_bound], X[train_bound:], y[train_bound:]
        predictions = []
        for model in self.base_models:
            model.fit(X_train, y_train)
            predictions.append(model.predict(X_test))
        blender_features = np.column_stack(predictions)
        self.blender_model.fit(blender_features, y_test)
    

    def predict(self, X):
        blender_features = np.column_stack([model.predict(X) for model in self.base_models])
        return self.blender_model.predict(blender_features)
