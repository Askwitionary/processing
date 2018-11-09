import pickle

def unique_vals(rows, col):
    """寻找每一列中的唯一值"""
    return set([row[col] for row in rows])


def class_counts(rows):
    """数每个标签的样本数"""
    counts = {}
    for row in rows:
        """最后一列为样本标签"""
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def is_numeric(value):
    """测试一个值是不是数字"""
    return isinstance(value, int) or isinstance(value, float)


class Question:
    """这个class用来对比。取列序号和值
    match方法比较数值或者字符串
    """

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        """对一个例子和本体做比较
        """
        
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        """打印树的时候用"""
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        else:
            condition = "是"
        return "{} {} {}?".format(
            header[self.column], condition, str(self.value))


def partition(rows, question):
    """将数据分割，如果满足上面Question条件则被分入true_row，否则被分入false_row
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def gini(rows):
    """计算一串数据的Gini值，即离散度的一种表达方式
    """
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity


def info_gain(left, right, current_uncertainty):
    """计算信息增益
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def find_best_split(rows):
    """核心，寻找信息增益最大的分割方法"""
    """遍历一次便可得到最高信息增益，以下是placeholder"""
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1  # 列数（除去标签）

    for col in range(n_features):   # 遍历每一列

        values = set([row[col] for row in rows])  # 每一列中的唯一值

        for val in values:  # 遍历每个值

            question = Question(col, val)

            # 以当前维度分割该列
            true_rows, false_rows = partition(rows, question)

            # 如果该维度对分割没有任何作用，跳过
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # 如果进行了分割，计算信息增益
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # 如果该信息增益大于当前最大信息增益，取代placeholder
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


class Leaf:
    """这个object保存训练数据中到这个节点的计数
    """

    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    """这个object保存一个问题和其结果的两支
    """

    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __eq__(self, other):
        return self.question == other.question and self.true_branch == other.branch and self.false_branch == other.false_branch


def build_tree(rows):
    """开始创建我们的决策树，使用递归法
    """
    gain, question = find_best_split(rows)

    # 到不需要再分时，即增益为0时，返回一个Leaf
    if gain == 0:
        return Leaf(rows)

    true_rows, false_rows = partition(rows, question)
    """使用DFS创建决策树，先创建返回正确的"""
    true_branch = build_tree(true_rows)

    false_branch = build_tree(false_rows)

    """返回一个包含最有价值的问题和其两支的object供递归。当所有分支都无需再分时返回整个树"""
    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):
    """打印我们创建出来的树"""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    # Print the question at this node
    print (spacing + str(node.question))

    # Call this function recursively on the true branch
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Call this function recursively on the false branch
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def classify(row, node):
    """See the 'rules of recursion' above."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions

    # Decide whether to follow the true-branch or the false-branch.
    # Compare the feature / value stored in the node,
    # to the example we're considering.
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


if __name__ == '__main__':
    counter = 0
    with open("../../../../data/output/file_tree.pickle", "rb") as f:
        file_tree = pickle.load(f)

    with open("../../../../data/nlp/essay_onehot_.pickle", "rb") as f:
        kws = pickle.load(f)
    # 
    # input data: the last col is label
    training = []
    for lvl1 in file_tree:
        for lvl2 in file_tree[lvl1]:
            for item in file_tree[lvl1][lvl2][:-3]:
                tag = item[0]
                content = item[1]

                onehot = [0] * len(kws)
                for i in range(len(kws)):
                    onehot[i] += content.count(kws[i])

                if onehot == [0]*len(kws):
                    # counter += 1
                    onehot.append(1)
                else:
                    onehot.append(0)
                onehot.append("{}-{}".format(lvl1, lvl2))
                training.append(onehot)

    # testing data
    testing = []
    testing_essay = []
    for lvl1 in file_tree:
        for lvl2 in file_tree[lvl1]:
            for item in file_tree[lvl1][lvl2][-3:]:
                tag = item[0]
                content = item[1]

                onehot = [0] * len(kws)
                for i in range(len(kws)):
                    onehot[i] += content.count(kws[i])
                if onehot == [0] * len(kws):
                    counter += 1
                    onehot.append(1)
                else:
                    onehot.append(0)
                onehot.append("{}-{}".format(lvl1, lvl2))
                testing.append(onehot)
                testing_essay.append((lvl1, lvl2, tag, content))

    # Column labels.
    # These are used only to print the tree.
    header = []
    for _ in range(len(testing[0])):
        header.append('{}'.format(_))
    my_tree = build_tree(training)

    # """测试"""
    # 正确计数

    # 将训练结果保存以防重复训练便于使用
    with open('../../../../data/output/category_dt_.pickle', 'wb') as f:
        pickle.dump(my_tree, f, protocol=pickle.HIGHEST_PROTOCOL)
    corr = 0
    with open('../../../../data/output/category_dt_.pickle', 'rb') as f:
        my_tree = pickle.load(f)
    # print_tree(my_tree)
    for i in range(len(testing)):
        row = testing[i]
        act = row[-1]
        possibilities = print_leaf(classify(row, my_tree))
        temp = 0
        for case in possibilities.keys():
            # print(float(possibilities[case][:-1]))
            if float(possibilities[case][:-1]) > temp:
                prediction = case
                temp = float(possibilities[case][:-1])
        # prediction = list(classify(row, my_tree).keys())[0]
        # print(type(act))
        if prediction == act:
            corr += 1
        else:
            print("Actual: {} === Predicted: {} === Prob: {}".format(act, prediction, print_leaf(classify(row, my_tree))))
            print(str(testing_essay[i]) + "\n")
        # print("Actual: {}. Predicted: {}".format(act, prediction))
    print('Accuracy: {}%'.format(100*corr/len(testing)))
