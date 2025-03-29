import os
from dotenv import load_dotenv
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from openai import AsyncAzureOpenAI

load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")


global creative_instance
creative_instance = None


def get_creative_model_client():
    global creative_instance
    if creative_instance is None:
        creative_instance = AzureOpenAIChatCompletionClient(
            model="gpt-4o",
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_OPENAI_API_VERSION,
            api_key=AZURE_OPENAI_API_KEY,
            temperature=1,
        )
    return creative_instance


global instance
instance = None


def get_model_client():
    global instance
    if instance is None:
        instance = AzureOpenAIChatCompletionClient(
            model="gpt-4o",
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_OPENAI_API_VERSION,
            api_key=AZURE_OPENAI_API_KEY,
            temperature=0.1,
        )
    return instance


global aoai_client
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


async def completion(messages: list[dict[str, str]] = [], model: str = "gpt-4o", temperature: float = 0.1) -> str:
    """
    Sends a list of messages to the OpenAI API and returns the response.

    Args:
        messages (list): A list of dictionaries containing 'role' and 'content'.
        model (str): The model to use for the API request.
        temperature (float): The temperature for the API response.

    Returns:
        dict: The response from the OpenAI API.
    """

    # Send the request to the OpenAI API
    final_messages = [{"role": message["role"],
                       "content": message["content"]} for message in messages]
    completion = await get_aoai_client().chat.completions.create(
        model=model,  # e.g. gpt-35-instant
        messages=final_messages,
    )

    return completion.choices[0].message.content
