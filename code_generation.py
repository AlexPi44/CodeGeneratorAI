import boto3  # AWS SDK for Python to interact with AWS services
import botocore.config  # To set custom retry and timeout configs
import json  # For encoding and decoding JSON
from datetime import datetime  # To timestamp output filenames


def generate_code_using_bedrock(message: str, language: str) -> str:
    # This function sends a prompt to Claude via AWS Bedrock and returns the generated code

    # Format the prompt for Claude
    prompt_text = f"""
Human: Write {language} code for the following instructions: {message}.
    Assistant:
    """

    # Construct the payload with generation settings
    body = {
        "prompt": prompt_text,
        "max_tokens_to_sample": 2048,  # Max number of tokens Claude can return
        "temperature": 0.1,             # Controls randomness (0 = more deterministic)
        "top_k": 250,                   # Top-K sampling
        "top_p": 0.2,                   # Top-P (nucleus) sampling
        "stop_sequences": ["\n\nHuman:"]  # When to stop generating
    }

    try:
        # Initialize the Bedrock runtime client
        bedrock = boto3.client("bedrock-runtime",
                               region_name="us-west-2",
                               config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))
        # Send the request
        response = bedrock.invoke_model(body=json.dumps(body), modelId="anthropic.claude-v2")
        # Decode the response
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        # Extract the generated code
        code = response_data["completion"].strip()
        return code

    except Exception as e:
        # Print any errors that occur
        print(f"Error generating the code: {e}")
        return ""


def save_code_to_s3_bucket(code, s3_bucket, s3_key):
    # This function uploads the generated code to the specified S3 bucket

    s3 = boto3.client('s3')  # Initialize S3 client

    try:
        # Upload the object to S3
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=code)
        print("Code saved to s3")

    except Exception as e:
        # Handle upload failure
        print("Error when saving the code to s3")


def lambda_handler(event, context):
    # AWS Lambda entry point

    event = json.loads(event['body'])  # Parse the input body from JSON
    message = event['message']         # Extract the message (instruction)
    language = event['key']            # Extract the language to use

    print(message, language)  # Print inputs for logging

    # Generate the code
    generated_code = generate_code_using_bedrock(message, language)

    if generated_code:
        # Format a timestamped filename
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f'code-output/{current_time}.py'
        s3_bucket = 'bedrock-course-bucket'  # ⚠️ Replace with your bucket

        # Save the generated code to S3
        save_code_to_s3_bucket(generated_code, s3_bucket, s3_key)
    else:
        print("No code was generated")

    return {
        'statusCode': 200,
        'body': json.dumps('Code generation')
    }
