import os
import csv
from bs4 import BeautifulSoup


def split_email(email_text):
    """
    Split the email into header and body.

    Args:
    - email_text (str): The raw email text.

    Returns:
    - tuple: (header, body)
    """

    # 使用两个连续的换行符作为分隔符，将邮件分割成头部和正文
    parts = email_text.split("\n\n", 1)

    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return email_text, ""


def process_email_files(folder_path):
    """
    Process all email files in the given folder, including its subfolders.

    Args:
    - folder_path (str): Path to the folder containing email files.

    Returns:
    - dict: A dictionary where keys are file paths and values are a tuple of (header, body).
    """

    email_data = {}
    h = []
    b = []
    paths=[]

    # 遍历文件夹和子文件夹中的每个文件
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file_name in filenames:
            file_path = os.path.join(dirpath, file_name)

            # 确保我们正在处理文件
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    email_content = file.read()
                    header, body = split_email(email_content)

                    # if "<html" in body.lower() or "<body" in body.lower():
                    #     body = extract_text_from_html_string(body)

                    email_data[file_path] = (header, body)
                    h.append(header)
                    b.append(body)
                    paths.append(file_path)

    return h, b, paths


def save_to_csv(headers, bodies, paths, csv_file):
    """
    Save the extracted headers and bodies to a CSV file.

    Args:
    - headers (list): List of email headers.
    - bodies (list): List of email bodies.
    - csv_file (str): Path to the CSV file to save the data.

    Returns:
    None
    """
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # 写入CSV文件的标题
        writer.writerow(['Header', 'Body', 'File Path'])

        # 遍历 headers 和 bodies 并将它们写入CSV文件
        for header, body, path in zip(headers, bodies, paths):
            writer.writerow([header, body, path])


def extract_text_from_html_string(html_content):
    # 使用BeautifulSoup解析HTML字符
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取纯文本
    text = soup.get_text()

    return text




folder = 'D:\/Warwick\/Project\/test\/non-spam'

Header = []
Body = []

Header, Body, Paths = process_email_files(folder)
save_to_csv(Header, Body, Paths, 'non-spam-with-paths.csv')
