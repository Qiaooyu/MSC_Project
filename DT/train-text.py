import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier


train_text_data_path = r'D:\Warwick\MSC_Code\dataset-ok\train text 3\train.csv'
train_text_df = pd.read_csv(train_text_data_path)
X_train_text = train_text_df.drop(columns=['isphishing'])
y_train_text = train_text_df['isphishing']


# 加载验证数据集
valid_text_data_path = r'D:\Warwick\MSC_Code\dataset-ok\train text 3\valid.csv'
valid_text_df = pd.read_csv(valid_text_data_path)

X_valid_text = valid_text_df.drop(columns=['isphishing'])
y_valid_text = valid_text_df['isphishing']

# #
# # # KNN训练
# knn_clf = KNeighborsClassifier(n_neighbors=5)  # 使用k=5
# knn_clf.fit(X_train_text, y_train_text)
#
# y_pred_text = knn_clf.predict(X_valid_text)
#
# accuracy_text = accuracy_score(y_valid_text, y_pred_text)
# print(accuracy_text) # 54.55%



# 创建并训练SVM模型
svm_clf = SVC(kernel='linear', random_state=42)
svm_clf.fit(X_train_text, y_train_text)

# 在验证集上进行预测
y_pred_svm = svm_clf.predict(X_valid_text)

# 计算模型在验证集上的准确度
accuracy_svm = accuracy_score(y_valid_text, y_pred_svm)
print(accuracy_svm)


# 创建并训练梯度提升模型Gradient Boosting
gb_clf = GradientBoostingClassifier(random_state=42)
gb_clf.fit(X_train_text, y_train_text)

# 在验证集上进行预测
y_pred_gb = gb_clf.predict(X_valid_text)

# 计算模型在验证集上的准确度
accuracy_gb = accuracy_score(y_valid_text, y_pred_gb)
print(accuracy_gb)




# 创建并训练朴素贝叶斯模型
nb_clf = GaussianNB()
nb_clf.fit(X_train_text, y_train_text)

# 在验证集上进行预测
y_pred_nb = nb_clf.predict(X_valid_text)

# 计算模型在验证集上的准确度
accuracy_nb = accuracy_score(y_valid_text, y_pred_nb)
print(accuracy_nb)