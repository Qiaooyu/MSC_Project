import pandas as pd
from sklearn.feature_selection import mutual_info_classif


def mi_body(df):

    y = df.iloc[:, 0]

    X = df.iloc[:, 1:301]

    # 计算互信息（Mutual Information）
    mi = mutual_info_classif(X, y)

    # 创建一个DataFrame以存储特征和其对应的互信息分数
    mi_df = pd.DataFrame({'Feature': X.columns, 'Mutual Information': mi})

    # 按互信息分数降序排序特征
    mi_df = mi_df.sort_values('Mutual Information', ascending=False)

    # 输出结果
    print(mi_df)
    mi_df.to_csv('mi_scores.csv', index=False)


print('for spam body')
df = pd.read_csv(r'D:\Warwick\MSC_Code\dataset-ok\copy.csv')
mi_body(df)
