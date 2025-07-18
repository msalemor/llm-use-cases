import os
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv


load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("OPENAI_VERSION")
AZURE_OPENAI_API_KEY = os.getenv("OPENAI_KEY")

aoai_client = None


def get_aoai_client():
    global aoai_client
    if aoai_client is None:
        aoai_client = AsyncAzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_OPENAI_API_VERSION,
            api_key=AZURE_OPENAI_API_KEY,
        )
    return aoai_client


def get_date_time() -> str:
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


get_date_topic = {
    "name": "get_date",
    "phrases": [
        "What is the current date and time?",
        "What day is it?",
        "Can you tell me the current date?",
        "Can you tell me the current time?",
    ],
    "action": get_date_time,
}
topics = [get_date_topic]


async def topic_check_agent(user_phrase: str, phrases: list[str]) -> bool:
    # Note: performance idea
    # If the user phrase is an exact match do not call the agent, just return True
    user_message = user_phrase
    system_prompt = "You are an agent that checks if a user message contains any of the following phrases or very similar phrases not in this list: "
    for frase in phrases:
        system_prompt += f"\n- {frase}"

    system_prompt += "\n\nIf any of the phrases or very similar phrases are found, return: YES, otherwise return: NO. No epilogue or prologue."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    answer = await completion(messages, model="gpt-4o", check_topic_injector=False)
    return bool(answer.strip().lower() == "yes")


async def topic_injector(list_messages: list[dict[str, str]]) -> str | None:
    """
    Determine if there's a topic and use it
    """
    last_message = list_messages[-1]
    if last_message["role"] == "user" and last_message["content"]:
        for topic in topics:
            if await topic_check_agent(last_message["content"], topic["phrases"]):
                response = topic["action"]()
                return response
    else:
        return None


async def completion(
    messages: list[dict[str, str]] = [],
    model: str = "gpt-4o",
    temperature: float = 0.1,
    check_topic_injector: bool = True,
) -> str:
    """
    Sends a list of messages to the OpenAI API and returns the response.
    """

    # Check for a topic and follow the topic's path
    if check_topic_injector:
        topic_answer = await topic_injector(messages)
        if topic_answer:
            return topic_answer

    final_messages = [
        {"role": message["role"], "content": message["content"]} for message in messages
    ]
    completion = await get_aoai_client().chat.completions.create(
        model=model,  # e.g. gpt-35-instant
        messages=final_messages,
        temperature=temperature,
    )

    return completion.choices[0].message.content


async def process(chat_history: list[dict[str, str]], prompt: str) -> None:
    chat_history.append({"role": "user", "content": prompt})
    print("Question: " + chat_history[-1]["content"])
    response = await completion(chat_history)
    chat_history.append({"role": "assistant", "content": response})
    print(f"Answer: {chat_history[-1]['content']}\n")


async def main():
    chat_history = []

    # No match
    await process(chat_history, "What is the capital of France?")

    # Exact match
    await process(chat_history, "What is the current date and time?")

    # Semantic match
    await process(chat_history, "What is my local time?")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
