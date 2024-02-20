# Azure OpenAI GPT Models<br/>Token Cost Optimization

## How are costs calculated

- Input tokens
- Output tokens

### Current Azure OpenAI Prices (02/2024)

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

- GPT models are foundational models, as such they can solve many problems.
- You could break the problem into pieces, but this may results in higher token usage.
- Or you could ask the prompt to return the results in one prompt.

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
- Solutions heavy on RAG might benefit in the LLMLingua compression technique:
microsoft/LLMLingua: To speed up LLMs' inference and enhance LLM's perceive of key information, compress the prompt and KV-Cache, which achieves up to 20x compression with minimal performance loss. (github.com)

### Monitor the Completions

- Every Completion return the usage information.
- Add tooling in your application to keep track of this usage.

### Use Semantic Cache

- This is a more advanced technique, it works by:
  - First determining if a user prompt has already been semantically added to the cache, using embeddings
  - Added to the cache in case of a cache miss,
  - and then on subsequent calls using the cache results on a cache hit.

Sample:

- [Semantic Cache](https://github.com/msalemor/sk-dev-training/blob/main/notebooks/sk-semantic-cache-redis.ipynb)

### Fine Tuning

- Instructions that tell the model how to behave and go on every prompt might be a good candidate to be fine-tuned (it means you don't need to send them every time)
