from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_version = "2024-02-15-preview"

client = AzureOpenAI(
    api_version=api_version,
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
)

completion = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL"),
    messages=[
        {
            "role": "user",
            "content": "What is the meaning of life?",
        },
    ],
    temperature=0.5
)

print(completion.to_json())
