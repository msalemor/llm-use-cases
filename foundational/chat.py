import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("OPENAI_ENDPOINT")
model = os.getenv("OPENAI_MODEL")

client = AzureOpenAI(api_key=api_key,
                     azure_endpoint=endpoint,
                     api_version="2024-02-15-preview")


if __name__ == "__main__":
    messages = []
    while True:
        user_input = input("You (type 'exit' to break): ")
        if user_input == "exit":
            break
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),  # model = "deployment_name".
            messages=messages,
            temperature=0.1,
        )
        resp = response.choices[0].message.content
        print(f"Assistant: {resp}\n\n")
        messages.append({"role": "assistant", "content": resp})
