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


global image_client
image_client = None


def get_image_client():
    global image_client
    if image_client is None:
        image_client = AsyncAzureOpenAI(
            azure_deployment="dall-e-3",
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version="2024-02-01",
            api_key=AZURE_OPENAI_API_KEY,
        )
    return image_client
