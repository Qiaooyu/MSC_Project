import os
import csv
from bs4 import BeautifulSoup
import re
from email import message_from_string
from urllib.parse import urlparse


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

                    # email_data[file_path] = (header, body)
                    if len(body) > 32000:
                        print(f"Skipping email due to large body size (>32000 characters). File path: {file_path}")
                    else:
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
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        # 写入CSV文件的标题
        writer.writerow(['Header', 'Body', 'File Path'])

        # 遍历 headers 和 bodies 并将它们写入CSV文件
        for header, body, path in zip(headers, bodies, paths):
            try:
                writer.writerow([header, body, path])
            except:
                print(path)


# def extract_text_from_html_string(html_content):
#     # 使用BeautifulSoup解析HTML字符
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#     # 提取纯文本
#     text = soup.get_text()
#
#     return text

def check_html_in_body(body):
    try:
        # 使用 BeautifulSoup 尝试解析 HTML
        soup = BeautifulSoup(body, 'html.parser')

        # 检查是否存在常见的 HTML 标签
        common_tags = ['html', 'body', 'div', 'span', 'a', 'table']
        if any(soup.find(tag) for tag in common_tags):
            return 1

        # 检查是否存在成对的开放和关闭标签
        if re.search(r'<(\w+)>.*</\1>', body, re.DOTALL):
            return 1

        return 0
    except Exception as e:
        print(f"An error occurred while checking for HTML: {e}")
        return 0


def check_html_form_in_body(body):
    """
    Check if the body of the email contains an HTML form.

    Args:
    - body (str): The body of the email.

    Returns:
    - int: 1 if an HTML form is found, 0 otherwise.
    """
    try:
        # 使用 BeautifulSoup 尝试解析 HTML
        soup = BeautifulSoup(body, 'html.parser')

        # 检查是否存在 form 标签并且有 action 属性
        if soup.find('form', action=True):
            return 1

        # 检查是否存在多个 input、textarea、select 或 button 标签
        form_elements = soup.find_all(['input', 'textarea', 'select', 'button'])
        if len(form_elements) > 1:
            return 1

        # 检查是否存在用于提交表单的元素
        if soup.find(['input', 'button'], {'type': 'submit'}):
            return 1

        return 0
    except Exception as e:
        print(f"An error occurred while checking for HTML form: {e}")
        return 0  # 在发生异常时返回 0，表示没有找到 HTML form


def check_javascript_in_body(body):
    try:
        # Use BeautifulSoup to try to parse HTML
        soup = BeautifulSoup(body, 'html.parser')

        # Check if a script tag exists
        if soup.find('script'):
            return 1

        # Check for the presence of MIME types related to JavaScript
        javascript_mime_types = ['text/javascript', 'application/javascript', 'text/ecmascript', 'application/ecmascript']
        if any(mime in body for mime in javascript_mime_types):
            return 1

        # Check for paired opening and closing script tags
        if re.search(r'<script[\s\S]*?>[\s\S]*?</script>', body, re.IGNORECASE):
            return 1

        return 0
    except Exception as e:
        print(f"An error occurred while checking for JavaScript: {e}")
        return 0


def check_attachment_in_header(header):

    if "Content-Disposition: attachment" in header:
        return 1
    return 0


def check_hidden_hyperlink_on_image(body):

    try:
        # 使用 BeautifulSoup 尝试解析 HTML
        soup = BeautifulSoup(body, 'html.parser')

        # 查找所有的 <a> 标签
        for a_tag in soup.find_all('a', href=True):
            # 在每个 <a> 标签内查找 <img> 标签
            if a_tag.find('img'):
                return 1  # 找到了带有隐藏超链接的图片

        return 0  # 没有找到带有隐藏超链接的图片
    except Exception as e:
        print(f"An error occurred while checking for hidden hyperlink on image: {e}")
        return 0  # 在发生异常时返回 0，表示没有找到带有隐藏超链接的图片


def count_bad_words_in_body(body):

    # 定义一个包含不良词汇的列表
    bad_words = ["link", "click", "confirm", "user", "customer", "client", "suspend", "restrict", "verify", "payment",
                 "protect"]

    # 使用正则表达式查找不良词汇，并计算它们的出现次数
    total_count = 0
    for word in bad_words:
        total_count += len(re.findall(r'\b{}\b'.format(re.escape(word)), body, re.IGNORECASE))

    return total_count


def count_bad_words_in_subject(header):

    # Find the subject line in the header
    subject_line = ""
    for line in header.split("\n"):
        if line.lower().startswith("subject:"):
            subject_line = line[8:].strip()  # Remove "Subject:" and strip whitespace
            break

    # Define a list of bad words
    bad_words = ["verify", "bank", "debit", "payment", "suspend"]

    # Count the occurrences of each bad word in the subject line
    total_count = 0
    for word in bad_words:
        total_count += subject_line.lower().count(word.lower())

    return total_count


def calculate_text_richness(body):

    num_words = len(body.split())
    num_chars = len(body)

    if num_chars == 0:
        return 0.0

    richness = num_words / num_chars
    return round(richness, 2)


def count_distinct_words(body):

    words = body.split()  # Split the text into words
    distinct_words = set(words)  # Create a set of distinct words
    return len(distinct_words)


def count_email_parts(header, body):

    email_text = header + "\n\n" + body  # Combine header and body with a double newline
    msg = message_from_string(email_text)
    if msg.is_multipart():
        return len(msg.get_payload())
    else:
        return 1


def extract_email_encoding(header):

    match = re.search(r"Content-Type:.*charset=([^\s;]+)", header, re.IGNORECASE)
    if match:
        return match.group(1).strip('"')
    else:
        return ""


def count_recipients(header):

    match = re.search(r"To: (.+)", header, re.IGNORECASE)
    if match:
        recipients = match.group(1)
        # Split by commas to get individual email addresses
        return len([email.strip() for email in recipients.split(",")])
    else:
        return 0


def count_ip_urls(body):

    # Regular expression to match IP-based URLs
    ip_url_pattern = r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    return len(re.findall(ip_url_pattern, body))


def count_hyperlinks(body):

    soup = BeautifulSoup(body, 'html.parser')
    return len(soup.find_all('a'))


def count_text_hyperlinks(body):

    soup = BeautifulSoup(body, 'html.parser')
    return len([tag for tag in soup.find_all('a') if tag.string])


def count_mismatched_href(body):

    soup = BeautifulSoup(body, 'html.parser')
    count = 0
    for tag in soup.find_all('a'):
        href = tag.get('href', '')
        text = tag.string if tag.string else ''
        if href != text and href and text:
            count += 1
    return count


def max_dots_in_urls(body):

    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)
    max_dots = 0
    for url in urls:
        num_dots = url.count(".")
        if num_dots > max_dots:
            max_dots = num_dots
    return max_dots


def count_port_urls(body):

    urls = re.findall(r'https?://[^\s<>":]+:\d+', body)
    return len(urls)


def check_sender_vs_link_domain(header, body):
    sender_match = re.search(r"From:.*@([a-zA-Z0-9.-]+)", header)
    sender_domain = sender_match.group(1) if sender_match else ""

    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)
    link_domains = set()

    for url in urls:
        try:
            link_domain = urlparse(url).netloc.split(":")[0]
            link_domains.add(link_domain)
        except ValueError:
            # Invalid URL, you might want to log it for further inspection
            continue

    for link_domain in link_domains:
        if link_domain != sender_domain:
            return 0
    return 1

################


def html_code_selection(input_csv, output_csv):
    
    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 处理表头
        headers = next(reader)
        headers.append('htmlCode')
        writer.writerow(headers)

        # 处理每一行（每一封邮件）
        for row in reader:
            body = row[1]  # body 在 CSV 的第二列
            html_code = check_html_in_body(body)
            row.append(html_code)
            writer.writerow(row)


def html_form_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        headers.append('htmlForm')
        writer.writerow(headers)

        for row in reader:
            body = row[1]
            html_form = check_html_form_in_body(body)
            row.append(html_form)
            writer.writerow(row)


def javascript_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        headers.append('javascript')
        writer.writerow(headers)

        for row in reader:
            body = row[1]
            javascript = check_javascript_in_body(body)
            row.append(javascript)
            writer.writerow(row)


def attachment_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        headers.append('attachment')
        writer.writerow(headers)

        for row in reader:
            header = row[0]
            attachment = check_attachment_in_header(header)
            row.append(attachment)
            writer.writerow(row)


def image_hidden_url_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('imagehiddenurl')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            image_hidden_url = check_hidden_hyperlink_on_image(body)
            row.append(image_hidden_url)
            writer.writerow(row)


def bad_word_count_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('badWordCount')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            bad_word_count = count_bad_words_in_body(body)
            row.append(bad_word_count)
            writer.writerow(row)


def bad_word_count_in_subject_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('badWordCountInSubject')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            header = row[0]  # header is in the first column of the CSV
            bad_word_count = count_bad_words_in_subject(header)
            row.append(bad_word_count)
            writer.writerow(row)


def text_richness_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('richness')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            richness = calculate_text_richness(body)
            row.append(richness)
            writer.writerow(row)


def distinct_words_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('DistinctWords')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            distinct_words_count = count_distinct_words(body)
            row.append(distinct_words_count)
            writer.writerow(row)


def email_parts_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('emailparts')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            header = row[0]  # header is in the first column of the CSV
            body = row[1]  # body is in the second column of the CSV
            email_parts_count = count_email_parts(header, body)
            row.append(email_parts_count)
            writer.writerow(row)


def email_encoding_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('emailencoding')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            header = row[0]  # header is in the first column of the CSV
            email_encoding = extract_email_encoding(header)
            row.append(email_encoding)
            writer.writerow(row)


def recipients_number_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('recipients_number')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            header = row[0]  # header is in the first column of the CSV
            recipients_count = count_recipients(header)
            row.append(recipients_count)
            writer.writerow(row)


def ip_url_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('IPURL')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            ip_url_count = count_ip_urls(body)
            row.append(ip_url_count)
            writer.writerow(row)


def hyperlinks_number_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('hyperlinksnumbers')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            hyperlinks_count = count_hyperlinks(body)
            row.append(hyperlinks_count)
            writer.writerow(row)


def text_hyperlinks_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('texthyperlink')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            text_hyperlinks_count = count_text_hyperlinks(body)
            row.append(text_hyperlinks_count)
            writer.writerow(row)


def mismatched_href_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('HREF')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            mismatch_count = count_mismatched_href(body)
            row.append(mismatch_count)
            writer.writerow(row)


def max_dots_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('dots')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            max_dots = max_dots_in_urls(body)
            row.append(max_dots)
            writer.writerow(row)


def port_urls_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('portURLs')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            body = row[1]  # body is in the second column of the CSV
            port_urls_count = count_port_urls(body)
            row.append(port_urls_count)
            writer.writerow(row)


def same_domain_selection(input_csv, output_csv):

    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Handle the header
        headers = next(reader)
        headers.append('samedomain')
        writer.writerow(headers)

        # Handle each row (each email)
        for row in reader:
            header = row[0]  # header is in the first column of the CSV
            body = row[1]    # body is in the second column of the CSV
            same_domain = check_sender_vs_link_domain(header, body)
            row.append(same_domain)
            writer.writerow(row)



# folder = 'D:\/Warwick\/Project\/test\/spam'
#
# Header = []
# Body = []
#
# Header, Body, Paths = process_email_files(folder)
# save_to_csv(Header, Body, Paths, 'spam-ok.csv')


csv_path = r'D:\Warwick\MSC_Code\dataset-ok'

# input_csv_path = os.path.join(csv_path, 'non-spam-ok.csv')
# output_csv_path = os.path.join(csv_path, 'non-spam-ok-with-html-feature.csv')

input_csv_path = os.path.join(csv_path, 'spam-ok-ports_url.csv')
output_csv_path = os.path.join(csv_path, 'spam-ok-domain.csv')

same_domain_selection(input_csv_path, output_csv_path)

