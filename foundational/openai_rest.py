import requests
import json
import os

from dotenv import load_dotenv
# Set your Azure OpenAI Service endpoint and API key
# https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME

load_dotenv
endpoint = os.getenv("OPENAI_FULL_ENDPOINT")
api_key = os.getenv("OPENAI_API_KEY")

# Set the prompt and other parameters
prompt = "What is the meaning of life?"
model = os.getenv("OPENAI_MODEL")

# Construct the request payload
payload = {
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "temperature": 0.5
}

# Set the headers and authentication
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Make the REST call
response = requests.post(endpoint, headers=headers, json=payload)

# Get the response JSON
response_json = response.json()

# Print the response
print(json.dumps(response_json, indent=4))
