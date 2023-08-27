import pandas as pd
from sklearn.feature_selection import mutual_info_classif


def mi_header(df):
    y = df['isphishing']

    feature_columns = list(range(3, 22))  # 创建一个从3到21的整数列表
    feature_columns.remove(13)  # 从列表中移除10，即排除第11列

    X = df.iloc[:, feature_columns]

    # 计算互信息（Mutual Information）
    mi = mutual_info_classif(X, y)

    # 创建一个DataFrame以存储特征和其对应的互信息分数
    mi_df = pd.DataFrame({'Feature': X.columns, 'Mutual Information': mi})

    # 按互信息分数降序排序特征
    mi_df = mi_df.sort_values('Mutual Information', ascending=False)

    # 输出结果
    print(mi_df)


def mi_body(df):
    y = df['isphishing']

    X = df.iloc[:, 4:304]

    # 计算互信息（Mutual Information）
    mi = mutual_info_classif(X, y)

    # 创建一个DataFrame以存储特征和其对应的互信息分数
    mi_df = pd.DataFrame({'Feature': X.columns, 'Mutual Information': mi})

    # 按互信息分数降序排序特征
    mi_df = mi_df.sort_values('Mutual Information', ascending=False)

    # 输出结果
    print(mi_df)

#
# print('for spam')
# df = pd.read_csv(r'D:\Warwick\MSC_Code\dataset-ok\spam-ok-feature-addlable.csv')
# mi_header(df)
#
# print('for non-spam')
# df = pd.read_csv(r'D:\Warwick\MSC_Code\dataset-ok\non-spam-ok-feature-addlable.csv')
# mi_header(df)

print('for spam body')
df = pd.read_csv(r"D:\Warwick\MSC_Code\dataset-ok\preprocess2\spam-preprocess-2-word2vec2-label.csv")
mi_body(df)