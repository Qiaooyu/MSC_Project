import pandas as pd


df = pd.read_csv(r'D:\Warwick\MSC_Code\dataset-ok\preprocess3\non-spam-ok-preprocess-word2vec2.csv')
df['isphishing'] = 0
df.to_csv(r'D:\Warwick\MSC_Code\dataset-ok\preprocess3\non-spam-ok-preprocess-word2vec2-label.csv', index=False)

df = pd.read_csv(r'D:\Warwick\MSC_Code\dataset-ok\preprocess3\spam-ok-preprocess-word2vec2.csv')
df['isphishing'] = 1
df.to_csv(r'D:\Warwick\MSC_Code\dataset-ok\preprocess3\spam-ok-preprocess-word2vec2-label.csv', index=False)