#!pip install openai, azure-identity, python-dotenv
import os
import time
import json
import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

# Initialize Azure OpenAI client with entra-id authentication
ENV=os.getenv('ENV')
if ENV=='prod':
  token_provider = get_bearer_token_provider(
      DefaultAzureCredential(),
      "https://cognitiveservices.azure.com/.default"
  )
  client = AzureOpenAI(
      azure_ad_token_provider=token_provider,
      azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
      api_version="2024-05-01-preview"
  )
else:
  client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview"
  )

# Create an assistant with no tools
assistant = client.beta.assistants.create(
    model="gpt-4o",  # replace with model deployment name
    name="Assistant792",
    instructions="",
    tools=[]
    ,tool_resources={},
    temperature=1,
    top_p=1
)

print(f"Assistant created: {json.dumps(assistant)}")

# Create a thread
thread = client.beta.threads.create()

# Add a user question to the thread
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="hi" # Replace this with your prompt
)

# Run the thread
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)

# Looping until the run completes or fails
while run.status in ['queued', 'in_progress', 'cancelling']:
  time.sleep(1) # wait to see if there's a result
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )

if run.status in ['completed','cancelled]:
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)

  try:
    # Clean up
    # Delete the tread
    client.beta.threads.delete(thread.Id)
    # Delete the Assistant
    client.beta.assistants.delete(assistant.Id)
  except:
    pass
  
elif run.status == 'requires_action':
  # the assistant requires calling some functions
  # and submit the tool outputs back to the run
  pass
else:
  print(run.status)
