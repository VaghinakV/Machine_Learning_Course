class DecisionNode(object):
    def __init__(self,
                 column=None,
                 value=None,
                 false_branch=None,
                 true_branch=None,
                 results=None,
                 is_leaf=False):
        """
        node of each split
        column is the index of feature by wich data is splitted
        value is column's value by which we filter data into splits
        if true_branch, then it is true branch of it's parent, same for false_branch
        is_leaf is true when node has no child
        results is dict_of_values(data) for data which reached this node
        """
        
        self.column = column
        self.value = value
        self.false_branch = false_branch
        self.true_branch = true_branch
        self.results = results
        self.is_leaf = is_leaf
