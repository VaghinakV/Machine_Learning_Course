import numpy as np
import pandas as pd
from decision_node import *

class DecisionTree(object):
    
    def __init__(self, 
                 max_depth=4, 
                 criterion='gini', 
                 shuffle=False,
                 bootstrap=False,
                 sample_size=None):
        self.max_depth = max_depth
        self.tree = None
        self.shuffle = shuffle
        self.bootstrap = bootstrap
        self.sample_size = sample_size

        if criterion == 'entropy':
            self.criterion = self.entropy
        else:
            self.criterion = self.gini

                
    def fit(self, X, y):
        data = pd.DataFrame(X).join(pd.DataFrame({'label': y}))
        fraction = 1 if self.sample_size is None else self.sample_size / len(data)
        data = data.sample(frac=fraction, replace=self.bootstrap).reset_index(drop=True)
        self.tree = self.build_tree(data, self.criterion, max_depth=self.max_depth)
        

    def predict(self, X):
        return np.array([self.predict_single_data(data) for data in X])
    
    
    def predict_single_data(self, x):
        current_node = self.tree
        while not current_node.is_leaf:
            if x[current_node.column] <= current_node.value:
                current_node = current_node.true_branch
            else:
                current_node = current_node.false_branch
        return self.classification(current_node.results)
    
    
    def classification(self, results):
        return results.idxmax()
    
    
    def build_tree(self, data, criterion, max_depth=4, current_depth=0):
        """
        criterion is impurity function to use
        """

        if len(data) == 0:
            return DecisionNode(is_leaf=True)

        if current_depth == max_depth:
            return DecisionNode(results=self.frequency_by_label(data), is_leaf=True)

        if len(self.frequency_by_label(data)) == 1:
            return DecisionNode(results=self.frequency_by_label(data), is_leaf=True)

        gain, best_column, best_value = self.best_gain(data, criterion)
        if criterion(data) <= gain:
            return DecisionNode(results=self.frequency_by_label(data), is_leaf=True)
        else:
            split_pos, split_neg = self.divide_data(data, best_column, best_value)
            return DecisionNode(column=best_column,
                                value=best_value,
                                results=self.frequency_by_label(data),
                                false_branch=self.build_tree(split_neg, criterion, max_depth, current_depth+1),
                                true_branch=self.build_tree(split_pos, criterion, max_depth, current_depth+1))
    
    
    def frequency_by_label(self, data):
        return data.groupby('label').size()

    
    def divide_data(self, data, feature_column, feature_value):
        data1 = data.where(data[feature_column] <= feature_value).dropna()
        data2 = data.where(data[feature_column] > feature_value).dropna()
        return data1, data2

    
    def get_probabilities(self, data):
        count_by_labels = data.groupby('label').size()
        data_size = len(data)
        probabilities = count_by_labels / data_size
        return probabilities

    
    def gini(self, data):
        return 1 - (self.get_probabilities(data)**2).sum()

    
    def entropy(self, data):
        probabilities = self.get_probabilities(data)
        return -(probabilities * np.log(probabilities)).sum()

    
    def calc_gain(self, data, feature_column, feature_value, impurity_function):
        left, right = self.divide_data(data, feature_column, feature_value)
        return (len(left) * impurity_function(left) + len(right) * impurity_function(right)) / len(data) 

    
    def best_gain_by_feature(self, data, feature_column, impurity_function):
        gain, feature_value = min([(self.calc_gain(data, feature_column, value, impurity_function), value) 
                        for value in data[feature_column].unique()])
        return gain, feature_value

    
    def best_gain(self, data, impurity_function):
        gain, feature_value, feature_column = min([self.best_gain_by_feature(data, column, impurity_function) + (column,)
                                              for column in data.columns.drop('label')])
        return gain, feature_column, feature_value    