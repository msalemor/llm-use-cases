import common
import time
import asyncio
from openai import AsyncAzureOpenAI

# Get a configured model
client = AsyncAzureOpenAI(
    api_key=common.api_KEY,
    api_version="2023-12-01-preview",
    azure_endpoint=common.api_URI)

client1 = AsyncAzureOpenAI(
    api_key=common.api_KEY,
    api_version="2023-12-01-preview",
    azure_endpoint=common.api_URI)

client.max_retries = 3

endpoints = [
    (common.api_URI, common.api_KEY, 1),
    (common.api_URI, common.api_KEY, 2)
]


async def work():
    while True:
        task1 = client.chat.completions.create(
            model=common.gpt_api_deployment,
            messages=[
                {"role": "assistant", "content": "What is the speed of light?"},
            ],
            max_tokens=50,
            temperature=0.3
        )
        tasks2 = client1.chat.completions.create(
            model=common.gpt_api_deployment,
            messages=[
                {"role": "assistant", "content": "What is the speed of light?"},
            ],
            max_tokens=50,
            temperature=0.3
        )
        asyncio.wait([task1, tasks2])

        print(f'{task1.result()}:{tasks2.result()}')
        time.sleep(1)

asyncio.run(work())
