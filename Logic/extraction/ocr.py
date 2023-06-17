from mindee import Client, documents
import json
import csv

def extract_data(filename):
# Init a new client
    mindee_client = Client(api_key="830cb7170c9ff80b58bb8cd696448cb1")

    # Load a file from disk
    input_doc = mindee_client.doc_from_path(f"sample/{filename}")

    # Parse the Receipt by passing the appropriate type
    result = input_doc.parse(documents.TypeReceiptV5)

    # Print a brief summary of the parsed data

    data=str(result.document)

    #print(text)
    csv_data = []
    json_data = {}

    # Parse the data
    lines = data.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith(":"):
            # Extract key-value pairs
            key_value = line[1:].split(": ", maxsplit=1)
            if len(key_value) == 2:
                key, value = key_value
                json_data[key] = value
        elif line.startswith("|"):
            # Extract table data
            if not csv_data:
                # Parse the table header for CSV
                headers = [header.strip() for header in line.strip("|").split("|")]
                csv_data.append(headers)
            elif line.startswith("+"):
                # Skip the table separators
                continue
            else:
                # Parse table rows for CSV
                row = [cell.strip() for cell in line.strip("|").split("|")]
                csv_data.append(row)

    # Convert to CSV
    file=filename[:-4]
    csv_file_path = f"csv_files/{file}.csv"
    with open(csv_file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    print(f"CSV file created: {csv_file_path}")



