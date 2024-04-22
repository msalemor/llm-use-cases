# OpenAI & OSS  - REST, SDKs, and Orchestrators

## REST

- All OpenAI endpoints, like completion and embedings, are POST API endpoints 
- You don't need SDKs to call them
- Many of my apps do not use any SDKs. In some of more advanced apps I use Golang and Rust again without SDKs.
- For the frontends I use React or SolidJs (writing more in solid lately)
- The list ordered in the SDKs I use most to less

## Python OpenAI SDK (includes Assistants API):

- https://github.com/openai/openai-python
- https://github.com/openai/openai-python/tree/main/examples

## C# - Semantic Kernel SDK:

- https://github.com/microsoft/semantic-kernel/tree/main/dotnet
- https://github.com/microsoft/semantic-kernel/tree/main/dotnet/samples/KernelSyntaxExamples

## Python - Semantic Kernel SDK:

- https://github.com/microsoft/semantic-kernel/tree/main/python
- https://github.com/microsoft/semantic-kernel/tree/main/python/samples/kernel-syntax-examples

## C# - Azure OpenAI SDK:

- https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/README.md

## C# - Azure Assistants API SDK:

- https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/openai/Azure.AI.OpenAI.Assistants

## Python - Promptflow SDK:

- https://github.com/microsoft/promptflow
- https://github.com/microsoft/promptflow/tree/main/examples

## Python - Langchain SDK:

- https://github.com/langchain-ai/langchain

## Hugging Face

- https://huggingface.co
- Most OSS models have samples

```python
import transformers
import torch

model_id = "meta-llama/Meta-Llama-3-8B"

pipeline = transformers.pipeline(
    "text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto"
)
pipeline("Hey how are you doing today?")
```

## Rust (Advanced) - Candle SDK:

- https://github.com/huggingface/candle
