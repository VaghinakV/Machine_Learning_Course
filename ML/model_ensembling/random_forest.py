from decision_tree import *

class RandomForest:

    def __init__(self, 
                 max_depth=4,
                 each_tree_data=70,
                 tree_count=5,
                 criterion="gini",
                 bootstrap=False):
        self.trees = [DecisionTree(max_depth, 
                                   criterion, 
                                   shuffle=True, 
                                   bootstrap=bootstrap, 
                                   sample_size=each_tree_data) for _ in range(tree_count)]
    

    def fit(self, X, y):
        for tree in self.trees:
            tree.fit(X, y)
    

    def predict(self, X):
        predictions = pd.DataFrame(np.array([tree.predict(X) for tree in self.trees]).T)
        y = np.array(predictions.mode(axis=1)[0])
        return y
