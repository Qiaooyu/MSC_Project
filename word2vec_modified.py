
from gensim.models import Word2Vec
import numpy as np
import csv

def email_to_feature_vector(email, model):
    words = email.split()
    feature_vector = np.zeros(model.vector_size)
    count = 0
    for word in words:
        if word in model.wv.index_to_key:
            feature_vector += model.wv[word]
            count += 1
    if count > 0:
        feature_vector /= count
    return feature_vector.tolist()

# 读取CSV文件
input_file_path = r"D:\Warwick\MSC_Code\dataset-ok\preprocess3\non-spam-ok-preprocess.csv"
output_file_path = r"D:\Warwick\MSC_Code\dataset-ok\preprocess3\non-spam-ok-preprocess-word2vec2.csv"

with open(input_file_path, mode='r', newline='', encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    
    # Update header to include individual feature columns
    for i in range(1, 301):  # Assuming a feature vector of size 300
        header.append(f'Feature_{i}')
    
    rows = [header]

    sentences = [row[2].split() for row in csvreader]
    file.seek(0)
    next(csvreader)

    # 训练Word2Vec模型
    model = Word2Vec(sentences, vector_size=300, window=5, min_count=1, sg=0)

    # 生成特征向量并添加到新列中
    for row in csvreader:
        email_body = row[2]
        feature_vector = email_to_feature_vector(email_body, model)
        
        # Extend the row with the feature_vector elements
        row.extend(feature_vector)
        
        rows.append(row)

# 写入新的CSV文件
with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerows(rows)
