import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from html import unescape


# Uncomment the following lines to download necessary NLTK data in your local environment
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_email_improved(email_body, stop_words):
    # Remove HTML tags
    clean_email_body = re.sub(r'<.*?>', '', email_body)

    # Decode HTML entities (if any)
    clean_email_body = unescape(clean_email_body)

    # Tokenization using NLTK's word_tokenize
    words = nltk.word_tokenize(clean_email_body)

    # Convert to lowercase
    words = [word.lower() for word in words]

    # Filter out stopwords and non-alphabetic words
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

    # Replace URLs with "URL" token
    filtered_words = [
        "URL" if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          word) else word
        for word in filtered_words
    ]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    preprocessed_email_body = ' '.join(lemmatized_words)

    return preprocessed_email_body


def preprocess_csv(input_file_path, output_file_path, stop_words):
    # Open the input CSV file for reading
    with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
        csvreader = csv.reader(infile)

        # Read the header and add a new column for preprocessed text
        header = next(csvreader)
        header.append('Preprocessed_Body')

        # Initialize a list to hold all rows including the header
        rows = [header]

        # Loop through each row in the CSV
        for row in csvreader:
            email_body = row[1]  # Assume email body is in the second column
            preprocessed_body = preprocess_email_improved(email_body, stop_words)  # Call your preprocessing function

            # Append the preprocessed text as a new column to the row
            row.append(preprocessed_body)

            # Add the row (now containing an extra column) to the list
            rows.append(row)

    # Open the output CSV file for writing
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        csvwriter = csv.writer(outfile)

        # Write all rows to the new CSV
        csvwriter.writerows(rows)


# Example usage
stop_words = set(stopwords.words('english'))
input_file_path = r"D:\Warwick\MSC_Code\dataset-ok\non-spam-ok.csv"
output_file_path = r"D:\Warwick\MSC_Code\dataset-ok\preprocess2\non-spam-preprocess-2.csv"
preprocess_csv(input_file_path, output_file_path, stop_words)

input_file_path = r"D:\Warwick\MSC_Code\dataset-ok\spam-ok.csv"
output_file_path = r"D:\Warwick\MSC_Code\dataset-ok\preprocess2\spam-preprocess-2.csv"
preprocess_csv(input_file_path, output_file_path, stop_words)
