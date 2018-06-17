import numpy as np

class Stack:
    
    def __init__(self, folds_number, 
                 base_models, models_params,
                 stacking_model, stacking_params):
        self.folds_number = folds_number
        self.stacking_model = stacking_model(**stacking_params)
        self.base_models = [model(**params) for model, params in zip(base_models, models_params)]
    
    
    def fit(self, X, y):
        data = np.column_stack((X, y))
        np.random.shuffle(data)
        X, y = data[:, :-1], data[:, -1]
        folds = np.array_split(X, self.folds_number)
        labels = np.array_split(y, self.folds_number)
        all_predictions = []
        for i in range(self.folds_number):
            X_train = np.concatenate([folds[j] for j in range(self.folds_number) if j != i])
            y_train = np.concatenate([labels[j] for j in range(self.folds_number) if j != i])
            predictions = []
            for model in self.base_models:
                model.fit(X_train, y_train)
                predictions.append(model.predict(folds[i]))
            all_predictions.append(np.column_stack(predictions))
        for model in self.base_models:
            model.fit(X, y)
        stacking_features = np.concatenate(all_predictions)
        self.stacking_model.fit(stacking_features, y)
    

    def predict(self, X):
        stacking_features = np.column_stack([model.predict(X) for model in self.base_models])
        return self.stacking_model.predict(stacking_features)

