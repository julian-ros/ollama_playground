import json

# Define the input and output file paths
input_file_path = '/Users/juliorosua/CERVESA-ESPIGA/embeddings_api/embeddings/source.json'
output_file_path = '/Users/juliorosua/CERVESA-ESPIGA/embeddings_api/embeddings/mydata.jsonl'

# Read the data from the input file
with open(input_file_path, 'r') as infile:
    data = json.load(infile)

# Write each JSON object to the output file, one per line
with open(output_file_path, 'w') as outfile:
    for item in data:
        json_line = json.dumps(item)
        outfile.write(json_line + '\n')

print("Data successfully converted and written to", output_file_path)