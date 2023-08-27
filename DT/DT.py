# 导入所有必要的库
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# 加载并预处理训练数据集
train_data_path = r'D:\Warwick\MSC_Code\dataset-ok\for train\train.csv'
train_df = pd.read_csv(train_data_path)
X_train = train_df.drop(columns=['isphishing'])
y_train = train_df['isphishing']
label_encoder = LabelEncoder()
X_train['emailencoding'] = label_encoder.fit_transform(X_train['emailencoding'])

# 训练决策树模型
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# 加载并预处理验证数据集
valid_data_path = r'D:\Warwick\MSC_Code\dataset-ok\for train\valid.csv'
valid_df = pd.read_csv(valid_data_path)
X_valid = valid_df.drop(columns=['isphishing'])
y_valid = valid_df['isphishing']
unknown_labels_index = X_valid[~X_valid['emailencoding'].isin(label_encoder.classes_)].index
X_valid.drop(index=unknown_labels_index, inplace=True)
y_valid.drop(index=unknown_labels_index, inplace=True)
X_valid['emailencoding'] = label_encoder.transform(X_valid['emailencoding'])

# 在验证集上进行预测并计算准确度
y_pred = clf.predict(X_valid)
accuracy_valid = accuracy_score(y_valid, y_pred)

# 加载并预处理测试数据集
test_data_path = r'D:\Warwick\MSC_Code\dataset-ok\for train\test.csv'
test_df = pd.read_csv(test_data_path)
X_test = test_df.drop(columns=['isphishing'])
y_test = test_df['isphishing']
unknown_labels_index_test = X_test[~X_test['emailencoding'].isin(label_encoder.classes_)].index
X_test.drop(index=unknown_labels_index_test, inplace=True)
y_test.drop(index=unknown_labels_index_test, inplace=True)
X_test['emailencoding'] = label_encoder.transform(X_test['emailencoding'])

# 在测试集上进行预测并计算准确度
y_pred_test = clf.predict(X_test)
accuracy_test = accuracy_score(y_test, y_pred_test)

print(accuracy_valid, accuracy_test)
