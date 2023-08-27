import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv(r"D:\Warwick\MSC_Code\newdataset\Phishing_Legitimate_full.csv")

# 对标签进行分层抽样，以保证训练、测试和验证集中的标签比例与整体数据集相同
train, temp = train_test_split(df, test_size=0.2, stratify=df['CLASS_LABEL'], random_state=42)
valid, test = train_test_split(temp, test_size=0.5, stratify=temp['CLASS_LABEL'], random_state=42)

# 保存训练、测试和验证集为新的CSV文件
train.to_csv(r'D:\Warwick\MSC_Code\newdataset\train.csv', index=False)
valid.to_csv(r'D:\Warwick\MSC_Code\newdataset\valid.csv', index=False)
test.to_csv(r'D:\Warwick\MSC_Code\newdataset\test.csv', index=False)
