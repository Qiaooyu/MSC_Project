import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import time

# 加载并预处理训练数据集
train_data_path = r'D:\Warwick\MSC_Code\newdataset\train.csv'
train_df = pd.read_csv(train_data_path)
X_train = train_df.drop(columns=['CLASS_LABEL'])
y_train = train_df['CLASS_LABEL']
label_encoder = LabelEncoder()
# X_train['emailencoding'] = label_encoder.fit_transform(X_train['emailencoding'])

# 初始化模型
models = {
    'DecisionTree': DecisionTreeClassifier(random_state=42),
    'RandomForest': RandomForestClassifier(random_state=42),
    'SVM': SVC()
}

# 分别训练决策树，随机森林，和SVM模型，并进行性能评估
for name, clf in models.items():
    start_time = time.time()

    # 训练模型
    clf.fit(X_train, y_train)

    # 计算训练时间
    training_time = time.time() - start_time

    # 加载并预处理验证数据集
    valid_data_path = r'D:\Warwick\MSC_Code\newdataset\valid.csv'
    valid_df = pd.read_csv(valid_data_path)
    X_valid = valid_df.drop(columns=['CLASS_LABEL'])
    y_valid = valid_df['CLASS_LABEL']
    # X_valid['emailencoding'] = label_encoder.transform(X_valid['emailencoding'])

    # 在验证集上进行预测并计算准确度、召回率和F1分数
    y_pred_valid = clf.predict(X_valid)
    valid_report = classification_report(y_valid, y_pred_valid)

    # 加载并预处理测试数据集
    test_data_path = r'D:\Warwick\MSC_Code\newdataset\test.csv'
    test_df = pd.read_csv(test_data_path)
    X_test = test_df.drop(columns=['CLASS_LABEL'])
    y_test = test_df['CLASS_LABEL']
    # X_test['emailencoding'] = label_encoder.transform(X_test['emailencoding'])

    # 在测试集上进行预测并计算准确度、召回率和F1分数
    y_pred_test = clf.predict(X_test)
    test_report = classification_report(y_test, y_pred_test)

    print(f"Model: {name}")
    print(f"Training time: {training_time} seconds")
    print(f"Validation Classification Report:\n{valid_report}")
    print(f"Test Classification Report:\n{test_report}")
    print("=" * 60)



train_data_path = r'D:\Warwick\MSC_Code\newdataset\filtered_train.csv'
train_df = pd.read_csv(train_data_path)
X_train = train_df.drop(columns=['CLASS_LABEL'])
y_train = train_df['CLASS_LABEL']
label_encoder = LabelEncoder()
# X_train['emailencoding'] = label_encoder.fit_transform(X_train['emailencoding'])

# 初始化模型
models = {
    'DecisionTree': DecisionTreeClassifier(random_state=42),
    'RandomForest': RandomForestClassifier(random_state=42),
    'SVM': SVC()
}

# 分别训练决策树，随机森林，和SVM模型，并进行性能评估
for name, clf in models.items():
    start_time = time.time()

    # 训练模型
    clf.fit(X_train, y_train)

    # 计算训练时间
    training_time = time.time() - start_time

    # 加载并预处理验证数据集
    valid_data_path = r'D:\Warwick\MSC_Code\newdataset\filtered_valid.csv'
    valid_df = pd.read_csv(valid_data_path)
    X_valid = valid_df.drop(columns=['CLASS_LABEL'])
    y_valid = valid_df['CLASS_LABEL']
    # X_valid['emailencoding'] = label_encoder.transform(X_valid['emailencoding'])

    # 在验证集上进行预测并计算准确度、召回率和F1分数
    y_pred_valid = clf.predict(X_valid)
    valid_report = classification_report(y_valid, y_pred_valid)

    # 加载并预处理测试数据集
    test_data_path = r'D:\Warwick\MSC_Code\newdataset\filtered_test.csv'
    test_df = pd.read_csv(test_data_path)
    X_test = test_df.drop(columns=['CLASS_LABEL'])
    y_test = test_df['CLASS_LABEL']
    # X_test['emailencoding'] = label_encoder.transform(X_test['emailencoding'])

    # 在测试集上进行预测并计算准确度、召回率和F1分数
    y_pred_test = clf.predict(X_test)
    test_report = classification_report(y_test, y_pred_test)

    print(f"Model: {name}")
    print(f"Training time: {training_time} seconds")
    print(f"Validation Classification Report:\n{valid_report}")
    print(f"Test Classification Report:\n{test_report}")
    print("=" * 60)
