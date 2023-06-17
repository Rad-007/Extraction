import csv
import re
import PyPDF2

def extract_data_from_invoice(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    header_data = {}
    table_data = []

    for page in pdf_reader.pages:
        text = page.extract_text()

        # Extract header data
        if not header_data:
            header_data = extract_header_data(text)

        # Extract table data
        extracted_table_data = extract_table_data(text)
        if extracted_table_data:
            table_data.extend(extracted_table_data)

    pdf_file.close()
    return header_data, table_data

def extract_header_data(text):
    header_data = {}
    # Extracting header data using regular expressions
    invoice_number_match = re.search(r'Invoice Number:\s*(\w+)', text)
    if invoice_number_match:
        header_data['Invoice Number'] = invoice_number_match.group(1)

    date_match = re.search(r'Date:\s*(\d{2}-\d{2}-\d{4})', text)
    if date_match:
        header_data['Date'] = date_match.group(1)

    # Add more header data extraction logic here

    return header_data

def extract_table_data(text):
    table_data = []
    # Extracting table data using regular expressions
    table_regex = r'(\d+)\s+(.+?)\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)'
    matches = re.findall(table_regex, text, re.DOTALL)
    for match in matches:
        item = {
            'Reference': match[0],
            'Designation': match[1],
            'Qty': match[2],
            'Unit_Price': match[3],
            'Total': match[4],
            'Sales': match[5],
        }
        table_data.append(item)

    return table_data

def save_to_csv(header_data, table_data, csv_path):
    fieldnames = list(header_data.keys())
    if table_data:
        fieldnames += list(table_data[0].keys())

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(header_data)
        writer.writerows(table_data)


# Usage example
pdf_path = 'sample/sample1.pdf'
csv_path = 'csv_files/sample1.csv'

header_data, table_data = extract_data_from_invoice(pdf_path)
save_to_csv(header_data, table_data, csv_path)
