import csv
import re


# 定义预处理函数
def preprocess_email_body(email_body):
    # 替换 URL 为 "url"
    clean_text = re.sub(r'http\S+|www\S+|https\S+', 'url', email_body, flags=re.MULTILINE)

    # 去除 HTML 标签
    clean_text = re.sub(r'<.*?>', '', clean_text)

    # 去除特殊字符和符号，保留字母、数字、空格、句号和换行符
    clean_text = re.sub(r'[^a-zA-Z0-9\s\.\n]', '', clean_text)

    clean_text = clean_text.lower()

    return clean_text


# 指定CSV文件路径
input_csv_path = r'D:\Warwick\MSC_Code\dataset-ok\preprocess3\spam-ok.csv'
output_csv_path = r'D:\Warwick\MSC_Code\dataset-ok\preprocess3\spam-ok-preprocess.csv'


with open(input_csv_path, mode='r', newline='', encoding='utf-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    header.append('Preprocessed_Body')
    rows = [header]

    for row in csvreader:
        email_body = row[1]  # 假设电子邮件正文在第二列
        preprocessed_body = preprocess_email_body(email_body)
        row.append(preprocessed_body)
        rows.append(row)

# 写入新的CSV文件
with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerows(rows)