# LLM/Foundational Model

## Requirements

- Python 3.7-3.10
- Create `notebooks\.env` file

```
OPENAI_URI=https://<NAME>.openai.azure.com/
OPENAI_KEY=<API_KEY>
OPENAI_VERSION=2023-07-01-preview
OPENAI_GPT_DEPLOYMENT=<GPT_DEPLOYMENT_NAME>
OPENAI_ADA_DEPLOYMENT=<ADA_DEPLOYMENT_NAME>
```

- Open a Notebook and click play on the cells

## Common Use Cases

- [Summarization & Risk Analysis](SUMMARIZATION.md)
  - Get a contract, summarize it, and identify the risks.
- [Recommendation system](RECOMMENDATION.md)
  - Recommend from an up-to-date list of restaurants
- [Language Translation](TRANSLATION.md)
  - Translate technical text from a target to a source language
- [Content generation and Personalization](GENERATION.md)
  - Generate a sales car description 
- [Intent and entities - A LUIS-like scenario](INTENT.md)
  - Find the user's intent and entities
- [Sentiment Analysis - Zero Short](SENTIMENT.md)
  - Sentiment Analysis  
- [RAG Pattern without a vector database](RAGNODB.md)
  - Provide the container and answer the question based only on the provided content.