import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextEmbedding
from dotenv import load_dotenv
import tiktoken

load_dotenv()

api_URI = os.getenv("OPENAI_URI")
api_KEY = os.getenv("OPENAI_KEY")
gpt_api_deployment = os.getenv("OPENAI_GPT_DEPLOYMENT")
ada_api_deployment = os.getenv("OPENAI_ADA_DEPLOYMENT")


def get_kernel():
    kernel = sk.Kernel()

    kernel.add_chat_service(
        "gpt", AzureChatCompletion(gpt_api_deployment, api_URI, api_KEY))

    kernel.add_text_embedding_generation_service(
        "ada", AzureTextEmbedding(ada_api_deployment, api_URI, api_KEY))

    kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
    kernel.import_skill(sk.core_skills.TextMemorySkill())
    return kernel


encoding = tiktoken.get_encoding("cl100k_base")


def get_tokens(text: str) -> str:
    return encoding.encode(text)


def get_max_tokens(text: str, expected='short') -> int:
    length = len(get_tokens(text))
    if expected == 'short':
        return length + 100
    elif expected == 'medium':
        return length + 250
    elif expected == 'long':
        return length + 500
