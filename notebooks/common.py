import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextEmbedding
from dotenv import load_dotenv
import tiktoken
from openai import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from jinja2 import Template

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


def get_openai_client():
    return AzureOpenAI(
        api_key=api_KEY,
        api_version="2023-12-01-preview",
        azure_endpoint=api_URI)


# os.environ["AZURE_OPENAI_API_KEY"] = api_KEY
# os.environ["AZURE_OPENAI_ENDPOINT"] = api_URI


def get_model():
    return AzureChatOpenAI(
        openai_api_version="2023-12-01-preview",
        azure_deployment=gpt_api_deployment,
        openai_api_key=api_KEY,
        openai_api_base=api_URI,
    )


def render_template(template_string, **kwargs) -> str:
    return Template(template_string).render(**kwargs)


def Call_OpenAI(client: AzureOpenAI, deployment_name: str, content: str, max_tokens: int = 100, temperature: float = 0.3) -> str:
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "assistant", "content": content},
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return str(response.choices[0].message.content)
