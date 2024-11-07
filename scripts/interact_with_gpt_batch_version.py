import json
from tqdm import tqdm
from openai import OpenAI

def process_batch_by_gpt(
    path_to_api_key: str = "###Remove, WILL COST MONEY###../API_KEY.txt",
    path_to_batched_prompts: str = "../results/batched_prompts.jsonl",
    output_path_batch_id: str = "../results/batch_id.txt",
    output_path_batch_object: str = "../results/batch.txt"
):
    """
    Process a batch of task by OpenAI
    Paramteres:
        path_to_api_key = store GPT API key in a .txt file
        path_to_batched_prompts = path to .jsonl of batch tasks for OpenAI
        output_path_batch_id = store id of batch job in .txt
        output_path_batch_object = store batch object in .txt
    """
    # Connect to OpenAI client
    print("Connecting to openai")
    my_api_key = open(path_to_api_key, 'r').read()
    client = OpenAI(api_key=my_api_key)

    # Create a batch file
    print("Creating batch file")
    batch_input_file = client.files.create(
        file=open(path_to_batched_prompts, "rb"),
        purpose="batch"
    )
    print("Batch file successfully created")
    print(batch_input_file)
    batch_input_file_id = batch_input_file.id

    # Process batch
    print("Launch batch")
    batch = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
        "description": "generate prompts of health care workers"
        }
    )
    print("Batch successfully launched")

    # Save batch id file
    with open(output_path_batch_id, "w") as f:
        f.write(batch.id)
    # Save the batch object in a file
    with open(output_path_batch_object, "w") as f:
        f.write(str(batch))
    print(f"Batch id saved to {output_path_batch_id} and batch object saved to {output_path_batch_object}")

def get_batch_status(
    path_to_api_key: str = "../API_KEY.txt",
    path_to_batch_id: str = "../results/batch_id.txt"
):
    """
    Check status of a batch job being processed by OpenAI
    Paramteres:
        path_to_api_key = store GPT API key in a .txt file
        path_to_batch_id = id of the batch job to check status of
    """

    # Connect to OpenAI client
    my_api_key = open(path_to_api_key, 'r').read()
    client = OpenAI(api_key=my_api_key)

    # Read from batch_id.txt file
    batch_id = open(path_to_batch_id, "r").read()
    batch_status = client.batches.retrieve(batch_id)
    print(batch_status)
    print(f"status = {batch_status.status}")

def get_batch_output_file_id(
    path_to_api_key: str = "../API_KEY.txt",
    path_to_batch_id: str = "../results/batch_id.txt"
):
    """
    Retrieve output file id of a job processed by OpenAI
    Paramteres:
        path_to_api_key = store GPT API key in a .txt file
        path_to_batch_id = id of the batch job to check status of

        returns the output file id
    """
    # Connect to OpenAI client
    my_api_key = open(path_to_api_key, 'r').read()
    client = OpenAI(api_key=my_api_key)

    # Read from batch_id.txt file and
    # Return output file id
    batch_id = open(path_to_batch_id, "r").read()
    batch_status = client.batches.retrieve(batch_id)
    return batch_status.output_file_id

def retrieve_results(
    path_to_api_key: str = "../API_KEY.txt",
    output_path = "../results/gpt_results.jsonl",
    path_to_batch_id: str = "../results/batch_id.txt"
):
    """
    Retrieve results from a job processed by OpenAI
    Paramteres:
        path_to_api_key = store GPT API key in a .txt file
        output_path = stores retrieved results here
        path_to_batch_id = id of the batch job to retrieve results from
    """
    

    # Connect to OpenAI client
    my_api_key = open(path_to_api_key, 'r').read()
    client = OpenAI(api_key=my_api_key)

    # Get Output file ID
    output_file_id = get_batch_output_file_id(path_to_batch_id = path_to_batch_id)

    # Write results to 
    file_response = client.files.content(output_file_id)
    with open(output_path, "w") as file:
        file.write(file_response.text)

def chose_mode():
    """
    Chose which funtion to execute from CLI
    """
    mode = "0"
    while not mode.isdigit() or mode not in ("1", "2", "3"):
        mode = input("""
            Chose in which mode you want to use this script:
            1: Process batch by GPT -> THIS WILL COST MONEY
            2: Check status of submitted batch job
            3: Retrieve results
            """)
    
    if int(mode) == 1:
        process_batch_by_gpt()
    elif int(mode) == 2:
        get_batch_status()
    elif int(mode) == 3:
        retrieve_results()


if __name__ == "__main__":
    from jsonargparse import CLI
    CLI(chose_mode)