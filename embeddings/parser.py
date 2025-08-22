import csv
import json
import tiktoken

def clean_value(value):
    # Remove special characters (e.g., Euro symbol)
    cleaned_value = value.replace('\u20ac', '').strip()
    return cleaned_value

def count_tokens(description, encoding_type):
    # Use tiktoken to count LLM tokens
    encoding = tiktoken.get_encoding(encoding_type)
    tokens = encoding.encode(description)
    return len(tokens)

def csv_to_jsonl(csv_file_path, jsonl_file_path, encoding_type):
    incremental_id = 1
    customer_sales = {}  # Dictionary to store total sales for each customer
    article_sales = {}  # Dictionary to store total sales for each article name

    with open(csv_file_path, encoding='utf-8') as csv_file_handler:
        csv_reader = csv.reader(csv_file_handler, delimiter=';')
        header = next(csv_reader)  # Skip the header row
        with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file_handler:
            for row in csv_reader:
                if len(row) >= 4:
                    articulo, fecha, importe, cliente = map(clean_value, row)
                    description = f"AN_{articulo};TS_{fecha};CN_{cliente};P_{importe}"
                    num_tokens = count_tokens(description, encoding_type)

                    # Update total sales for customer
                    customer_sales[cliente] = customer_sales.get(cliente, 0) + float(importe.replace(',', ''))

                    # Update total sales for article name
                    article_sales[articulo] = article_sales.get(articulo, 0) + float(importe.replace(',', ''))

                    # Add TSCN and TSAN to description
                    description += f";TSCN_{customer_sales[cliente]:.2f};TSAN_{article_sales[articulo]:.2f}"

                    data_item = {
                        'embedding_id': incremental_id,
                        'tokens': num_tokens,
                        'description': description,
                    }
                    json.dump(data_item, jsonl_file_handler, ensure_ascii=False)
                    jsonl_file_handler.write('\n')  # Add newline separator
                    incremental_id += 1

    return incremental_id - 1  # Subtract 1 to get the total number of embeddings

csv_file_path = 'embeddings/espiga_data.csv'
jsonl_file_path = 'embeddings/mydata.jsonl'
encoding_type = 'cl100k_base'  # Choose the appropriate encoding
total_embeddings = csv_to_jsonl(csv_file_path, jsonl_file_path, encoding_type)

print(f"Total embeddings written to JSONL: {total_embeddings}")
