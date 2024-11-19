import json

# Define the function to update fields
def update_jsonl_fields(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Parse the JSON object from the current line
            data = json.loads(line)
            
            # Update the field names
            if 'conversation' in data:
                data['conversations'] = data.pop('conversation')
                
            for conv in data['conversations']:
                if conv['role'] == 'chatbot':
                    conv['role'] = 'assistant'
                
                # Rename 'role' to 'from'
                conv['from'] = conv.pop('role')
            
            # Write the updated JSON object back to a new file
            json.dump(data, outfile)
            outfile.write('\n') 

# Replace 'input.jsonl' and 'output.jsonl' with your actual file paths
update_jsonl_fields('multiturn_tasks_x_subtopics.jsonl', 'multiturn_tasks_cleaned.jsonl')
