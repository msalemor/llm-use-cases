# Azure OpenAI GPT Models<br/>Token Cost Optimization

## Pricing models

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

## Current Azure OpenAI Prices (02/2024)

| Models | Context | Input (Per 1,000 tokens) | Output (Per 1,000 tokens) |
|------------------------|---------|-------------------------|--------------------------|
| GPT-3.5-Turbo-0125 | 16K | $0.0005 | $0.0015 |
| GPT-3.5-Turbo-Instruct | 4K | $0.0015 | $0.002 |
| GPT-4-Turbo | 128K | $0.01 | $0.03 |
| GPT-4-Turbo-Vision | 128K | $0.01 | $0.03 |
| GPT-4 | 8K | $0.03 | $0.06 |
| GPT-4 | 32K | $0.06 | $0.12 |

## Cost Saving Techniques

### Model Selection

- Different models offer different features, performance and cost.
- For example, consider the the price and features of GPT 4 vs GPT 3.5 turbo. Could you do the meet your requirements by using GPT 3.5?

### Prompt Engineering

- Carefully design your prompts to be concise and relevant. Remove unnecessary words or phrases to reduce token usage.
- GPT models are foundational models, as such they can solve many problems.
- You could break the problem into pieces, but this may results in higher token usage.
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

### Trim the Prompt before Completion

- There are advanced techniques for trimming the Prompt before submitting for Completion.
- This is particularly important maybe after extracting text from documents like PDFs.
- Example package:
  - [GPT Trim](https://pypi.org/project/gptrim/)

#### LLMLingua

- LLMLingua, developed by Microsoft Research, is a fascinating approach that aims to enhance the efficiency and performance of Large Language Models (LLMs) through prompt compression.
- By reducing both prompt and generation lengths, LLMLingua helps save computational resources and lowers token costs.

### Use Semantic Cache

- Cache intermediate results or context vectors to avoid redundant computations.
- This is a more advanced technique, it works by:
  - First determining if a user prompt has already been semantically added to the cache, using embeddings
  - Added to the cache in case of a cache miss,
  - and then on subsequent calls using the cache results on a cache hit.

Sample:

- [Semantic Cache](https://github.com/msalemor/sk-dev-training/blob/main/notebooks/sk-semantic-cache-redis.ipynb)

### Fine Tuning

- Fine-tuning involves taking a pre-trained model (which has already learned patterns and features on a large dataset) and further training it on a smaller, domain-specific dataset.
- Transfer Learning: Fine-tuning is essential for transfer learning. Instead of training a large model from scratch, you start with a pre-trained one and fine-tune it for your specific task.
- Token Efficiency: Compared to using prompts, fine-tuning is often more effective and efficient. By training the model on examples, you can shorten prompts and save input tokens without sacrificing quality.

### Monitor the Completions

- Every Completion return the usage information.
- Add tooling in your application to keep track of this usage.
