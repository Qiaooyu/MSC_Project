import pandas as pd

df = pd.read_csv(r'D:\Warwick\MSC_Code\dataset-ok\preprocess2\spam-preprocess-2-word2vec.csv')

df.iloc[:, 4] = df.iloc[:, 4].str.replace('[\[\]]', '', regex=True)
new_columns = [f"feature{i+1}" for i in range(300)]
split_data = df.iloc[:, 4].str.split(',', expand=True)
split_data.columns = new_columns


df = pd.concat([df.iloc[:, :7], split_data, df.iloc[:, 7:]], axis=1)

df.to_csv(r'D:\Warwick\MSC_Code\dataset-ok\preprocess2\spam-preprocess-2-word2vec-300.csv', index=False)
