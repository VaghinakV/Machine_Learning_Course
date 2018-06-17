from random_forest import *
from logistic_regression import *
from SVC import *
from stack import *
from blender import *
from boost import *
from sklearn.metrics import accuracy_score

def main():
    train_data = np.load('train_data.npy')
    train_data, train_labels = train_data[:, 1:], train_data[:, 0]
    train_data = (train_data - train_data.min()) / (train_data.max() - train_data.min())
    train_labels[train_labels == 0] = -1
    test_data = np.load('test_data.npy')
    test_data = (test_data - test_data.min()) / (test_data.max() - test_data.min())
    base_models = [RandomForest, SVC, SVC, LogisticRegression]
    base_models_params = [{'max_depth': 10, 'each_tree_data': 100, 'tree_count': 10}, 
                          {'kernel': 'poly', 'use_bias': True}, 
                          {'gamma': 5 / train_data.shape[0], 'use_bias': True}, 
                          {'learning_rate': 0.0000001}]
    stacking_model = RandomForest
    stacking_params = {'max_depth': 10, 'tree_count': 10}
    clf = Stack(5, base_models, base_models_params, stacking_model, stacking_params)
    clf.fit(train_data, train_labels)
    predictions = clf.predict(test_data)
    predictions[predictions == -1] = 0
    np.save("predictions.npy", predictions)

if __name__ == "__main__":
    main()