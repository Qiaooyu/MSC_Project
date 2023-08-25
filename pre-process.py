import nltk
from nltk.stem import WordNetLemmatizer
import csv
import re
import numpy as np
import string
from nltk.corpus import stopwords
from html import unescape



nltk.download('stopwords')
nltk.download('wordnet')


def preprocess_email(email_body, stop_words):
    # 去除HTML标签
    clean_email_body = re.sub(r'<.*?>', '', email_body)

    # 解码HTML实体（如果有）
    clean_email_body = unescape(clean_email_body)

    # 手动分词（基于空格和标点符号）
    def manual_tokenize(text):
        words = text.split()
        tokens = []
        for word in words:
            token = ''.join(char for char in word if char not in string.punctuation)
            tokens.append(token)
        return tokens

    lemmatizer = WordNetLemmatizer()

    words = manual_tokenize(clean_email_body)
    words = [word.lower() for word in words]
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    filtered_words = [
        "URL" if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          word) else word for word in filtered_words]
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    preprocessed_email_body = ' '.join(lemmatized_words)

    return preprocessed_email_body




# input_file_path = r'D:\Warwick\MSC_Code\dataset-ok\spam-ok.csv'
# output_file_path = r'D:\Warwick\MSC_Code\dataset-ok\spam-ok-preprocessed.csv'
input_file_path = r'D:\Warwick\MSC_Code\dataset-ok\non-spam-ok.csv'
output_file_path = r'D:\Warwick\MSC_Code\dataset-ok\non-spam-ok-preprocessed.csv'
stop_words = set(stopwords.words('english'))

with open(input_file_path, mode='r', newline='', encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    header.append('Preprocessed_Body')
    rows = [header]

    for row in csvreader:
        email_body = row[1]  # 假设电子邮件正文在第二列
        preprocessed_body = preprocess_email(email_body, stop_words)
        row.append(preprocessed_body)
        rows.append(row)

# 写入新的CSV文件
with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerows(rows)

