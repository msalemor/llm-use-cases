# Azure OpenAI GPT Models<br/>Token Cost Optimization

![An image of a Robot pointing to a text caption reading: Token Cost Optionization Techniques](images/token-cost-savings.png)

## Overview


## 1.0 Pricing models

There are two pricing models: Pay-As-You-Go (PAYG) and Provisioned Throughput Units (PTUs). Let’s explore the differences from a cost perspective:

Pay-As-You-Go (PAYG):

- Flexibility: PAYG allows you to pay only for the resources you actually use. It’s ideal for variable workloads where demand fluctuates.
- Resource Consumption: You are billed based on the actual consumption of model processing resources during inference.
- Cost Optimization: PAYG optimizes costs by dynamically adjusting based on usage, making it suitable for scenarios with varying workloads.

Provisioned Throughput Units (PTUs):

- Predictability: PTUs provide guaranteed throughput with minimal latency variance. They offer a predictable pricing model.
- Reserved Capacity: With PTUs, you reserve and deploy a specific amount of model processing capacity in advance.
- Cost Savings: Depending on your workload volume, Managed PTUs can be more cost-effective than PAYG, especially for consistent performance.
- Ideal for Scaling: PTUs are well-suited for scaling AI solutions where you need reliable and consistent throughput.

Pricing Structure:

- Each model (such as GPT-3.5-Turbo, GPT-4, etc.) is priced per unit, ensuring a predictable cost structure for your AI deployments.

## 2.0 Current Azure OpenAI Prices (02/2024)

| Models | Context | Input (Per 1,000 tokens) | Output (Per 1,000 tokens) |
|------------------------|---------|-------------------------|--------------------------|
| GPT-3.5-Turbo-0125 | 16K | $0.0005 | $0.0015 |
| GPT-3.5-Turbo-Instruct | 4K | $0.0015 | $0.002 |
| GPT-4-Turbo | 128K | $0.01 | $0.03 |
| GPT-4-Turbo-Vision | 128K | $0.01 | $0.03 |
| GPT-4 | 8K | $0.03 | $0.06 |
| GPT-4 | 32K | $0.06 | $0.12 |

## 3.0 Cost Saving Techniques

### 3.1 Model Selection

- Different models offer different features, performance, and cost.
- For example, consider the performance (TPM), price, and features of GPT 4 vs GPT 3.5 turbo.
  - Could you meet your requirements by using GPT 3.5? Or could you have a solution that goes to GPT 3.5 most of the time and GPT 4 with Vision some of the time?

### 3.2 LLM vs Chat model

- Some refer to LLM models (Davinci) as ones that return text.
- Chat models (GPT 3 or 4) are designed to have conversations.
- A Chat model can be used as an LLM model if no conversation history is sent as part of the context for Completion.
- Consider whether the solution can be served with an LLM model or a Chat model used as an LLM model. Do you need the conversation state?
- In a Chat model, the input will include all the tokens that make up the history.
- If the Chat model is required to meet the requirement, consider how much state you should keep and send for Completion.

### 3.3 Prompt Engineering

- Carefully design your prompts to be concise and relevant. Remove unnecessary words or phrases to reduce token usage.
- GPT models are foundational models, as such they can solve many problems (content generation, translation, analysis, intent, etc.).
- You could break the problem into pieces, but this may result in higher token usage.
- Combine information and questions in a single prompt to achieve more efficient interactions.

Example:

```python
car_description_prompt="Generate a car description for: {{$car}}"
translation_prompt="Translate the text from English to {{$target}}"
```

vs

```python
car__description_prompt="""Generate a car description for: 

{{$car}} 

and translate it into Spanish

JSON Output format:
{
    "en": // English description
    "es": // Spanish description
}
"""
```

### 3.4 Trim the Prompt for Completion

- There are advanced techniques for trimming the Prompt before submitting it for Completion.
- This is particularly important maybe after extracting text from documents like PDFs.
- Example package:
  - [GPT Trim](https://pypi.org/project/gptrim/)

#### 3.4.1 LLMLingua

- LLMLingua, developed by Microsoft Research, is a fascinating approach that aims to enhance the efficiency and performance of Large Language Models (LLMs) through prompt compression.
- By reducing both prompt and generation lengths, LLMLingua helps save computational resources and lowers token costs.

Reference:

- [LLMLingua](https://github.com/microsoft/LLMLingua)

### 3.5 Use Semantic Cache

- Cache intermediate results or context vectors to avoid redundant computations.
- This is a more advanced technique, it works by:
  - First determining if a user prompt has already been semantically added to the cache using embeddings
  - Added to the cache in case of a cache miss,
  - and then on subsequent calls using the cache results on a cache hit.

Sample:

- [Semantic Cache](https://github.com/msalemor/sk-dev-training/blob/main/notebooks/sk-semantic-cache-redis.ipynb)

### 3.6 Determine Intent

- Under this scenario, the system determines intent before replying
- The system could send a Prompt with context to a GPT endpoint for completion ("What is my itinerary?")
- Or call a dedicated service ("What is the weather in London?)

Sample:

- [Determine Intent](https://github.com/msalemor/llm-use-cases/blob/main/notebooks/adversarial-prompting/defense-intent-recognition-rag.ipynb)

### 3.7 Fine Tuning

- Fine-tuning involves taking a pre-trained model (which has already learned patterns and features on a large dataset) and further training it on a smaller, domain-specific dataset.
- Transfer Learning: Fine-tuning is essential for transfer learning. Instead of training a large model from scratch, you start with a pre-trained one and fine-tune it for your specific task.
- Token Efficiency: Compared to using prompts, fine-tuning is often more effective and efficient. By training the model on examples, you can shorten prompts and save input tokens without sacrificing quality.

### 3.8 Monitor the Completions

- Every Completion returns the usage information.
- Enable monitoring.

Reference:

- [OpenAI Monitoring](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/monitoring)
