import os
import time
from functools import wraps

import click
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
load_dotenv()


azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("API_KEY")
api_version = os.getenv("VERSION")
model = os.getenv("MODEL", "gpt-4.1")


client = AsyncAzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_version=api_version,
    api_key=api_key,
)

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        click.echo(click.style(f"Execution time for {func.__name__}: {end - start:.4f} seconds", fg="green"))
        return result
    return wrapper


@measure_time
async def completion(messages:list, temperature=0.1, model=model, response_format: str = "text")-> tuple[str, dict]:
    #print(f"Model: {model}")
    result = await client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={ "type": response_format }, # or "text" or "json_object"
        temperature=temperature,
    )
    return result.choices[0].message.content, result.usage

@measure_time
async def non_optimized_run():

    print("*"*20)
    print("Non-optimized run")
    print("*"*20)

    prompts = [
        "Write a Python FastAPI application to manage contacts. Use SQLite to store the contacts.",
        "Convert the Python application to Golang.",
        "Convert the Golang application to TypeScript with Bun.js."
    ]

    
    conversation_history = [] # conversation thread
    usage = None

    for prompt in prompts:
        conversation_history.append({"role": "user", "content": prompt})
        print("User:", prompt)
        response, usage = await completion(conversation_history)
        print("Assistant:", response)
        conversation_history.append({"role": "assistant", "content": response})            
        print(f"Token Usage: Sent: {usage.prompt_tokens}, Received: {usage.completion_tokens}, Total: {usage.total_tokens}")

    print(f"Final Token Usage: Sent: {usage.prompt_tokens}, Received: {usage.completion_tokens}, Total: {usage.total_tokens}\n")

@measure_time
async def optimized_run():

    print("*"*20)
    print("Optimized run")
    print("*"*20)


    prompts = [
        "Write a Python FastAPI application to manage contacts. Use SQLite to store the contacts. Output the code only in the following JSON format: {\"code\": \"<your_code_here>\"}. No epilogue or prologue.",
        "Convert the Python application to Golang. Output the code only in the following JSON format: {\"code\": \"<your_code_here>\"}. No epilogue or prologue.",
        "Convert the Golang application to TypeScript with Bun.js. Output the code only in the following JSON format: {\"code\": \"<your_code_here>\"}. No epilogue or prologue."
    ]

    conversation_history = []
    usage = None

    for prompt in prompts:
        conversation_history.append({"role": "user", "content": prompt})
        print("User:", prompt)
        response, usage = await completion(conversation_history, response_format="json_object")
        #print("Assistant:", response)
        conversation_history.append({"role": "assistant", "content": response})            
        print(f"Token Usage: Sent: {usage.prompt_tokens}, Received: {usage.completion_tokens}, Total: {usage.total_tokens}")
    
    print(f"Final Token Usage: Sent: {usage.prompt_tokens}, Received: {usage.completion_tokens}, Total: {usage.total_tokens}\n")

@measure_time
async def super_optimized_run():

    print("*"*20)
    print("Super optimized run")
    print("*"*20)


    prompts = [
        "Write a Python FastAPI application to manage contacts. Use SQLite to store the contacts. Output the code only. No epilogue or prologue.",
        "Convert the Python application to Golang. Output the code only. No epilogue or prologue.",
        "Convert the Golang application to TypeScript with Bun.js. Output the code only. No epilogue or prologue."
    ]

    conversation_history = []
    usage = None
    last_response = ""

    for prompt in prompts:
        conversation_history = []
        conversation_history.append({"role": "user", "content": prompt + last_response})
        print("User:", prompt)
        response, usage = await completion(conversation_history)
        last_response = "\n\n" + response
        print(f"Token Usage: Sent: {usage.prompt_tokens}, Received: {usage.completion_tokens}, Total: {usage.total_tokens}")

    print(f"Final Token Usage: Sent: {usage.prompt_tokens}, Received: {usage.completion_tokens}, Total: {usage.total_tokens}\n")


if __name__ == "__main__":
    import asyncio

    async def main():

        await non_optimized_run()
        await optimized_run()
        await super_optimized_run()


    asyncio.run(main())
