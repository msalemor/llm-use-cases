# Improve the RAG response quality and accuracy

## Overview

This document offers techniques to improvce quality and accuracy of the results when deploying an intelligent application that includes Resource-Augmented Generation (RAG). The suggestions include techniques such as adjusting the RAG paramenter, utilizing the native vector database nearest search functionality, and performing trimming and document cleanup. Additionally, it proposes taking control of the ingestion process, creating and ingesting synthetic documents, and considering full document summarization if necessary. It emphasizes the importance of evaluating the results and involving subject matter experts in writing baseline responses.

By implementing these techniques, you could improve the quality and accurary of your RAG enabled system.

### Adjust the RAG paramenters

- Text splitting techniques
  - Split by token counts and overflow
  - Split by paragrpahs
  - Put markers in the documents
  - Maybe even consider manual splitting
  - Etc.

- Text chunk size
  - Determine what is the best chunk size for your content  

- Relevance
  - Increase or decrease the relevance score to get more or less chunks from the vector database

- Result limits & model context window
  - Some models support 4k, 32k, and 128k context windows
  - Try to take advantage of the context window, but be mindful of costs

- Evaluate and leverage the vector database nearest search capabilities  
  - For example, in Azure AI Search for example, Hybrid Search is a powerful technique that combines both full text and vector queries to retrieve relevant information from a search index.

### Trimming and document cleanup

- For example, converting PDF documents to text may generate a lot of white space and character
- Evaluate if there's a way to trim and clean these documents

### Take control of ingestion

- Automatic ingesting techniques may be provide good results
- Improving the RAG results may involve taking control of the ingestion stage where you may be able to apply different text splitting techniques, trimming and cleanup, and chunk sizes to your data.

Samples:
- [Nearest Search Notebook - C#](https://github.com/msalemor/llm-use-cases/blob/main/notebooks/embeddings-cosine-similarity-search-c%23.ipynb)
- [Nearest Search Notebook - Python](https://github.com/msalemor/llm-use-cases/blob/main/notebooks/embeddings-cosine-similarity-search.ipynb)

### Syntethic documents

- Create and ingest synthetic documents
- If you know that your users will be searching for data, maybe there's an opportunity to summarize, and classify the documents for ingestion into synthetic documents specially designed for RAG consumption.

Sample:
- [FAQ Generator - C#](notebooks/faq-generator-c%23.ipynb)
- [FAQ Generator - Python](notebooks/faq-generator.ipynb)

### Move to full summarization, if needed

- If you are looking the most precise answers, you may have to summarize entire documents
- Under this summarization technique, a map reduce recursive tecnhique is applied to the entire document, and then get a final summary.

Sample:
- [Semantic Kernel Summarization Notebook - C#](https://github.com/msalemor/sk-dev-training/blob/main/notebooks/sk-summarizer-pattern.ipynb)

### Evaluate RAPTOR

Reference:
- [RAPTOR: RECURSIVE ABSTRACTIVE PROCESSING FOR TREE-ORGANIZED RETRIEVAL-PDF](https://arxiv.org/pdf/2401.18059.pdf)
- [RAPTOR Repo & Notebook](https://github.com/profintegra/raptor-rag/blob/master/demo.ipynb)

### Prompt Engineering

- Give instruction to the prompt to just use the data provided.

### Evaluate your results

- Make sure you evaluate your results
- It many instances, SMEs may be needed to write the baseline responses.
- It is a team effort:
  - Data team could help in preparing the input sources, data prepartion, and setting up the output target
  - Data Science team could help determining the best text splitting, chunk Size, results evaluation, etc.
  - SMEs could help develop the reference evaluation questions
  - Apps team could help in making the application secure, resilient and performance
  
Example:
- [Evaluation Notebook Sample - C#](https://github.com/msalemor/llm-use-cases/blob/main/notebooks/evaluation-c%23.ipynb)
- [Evaluation Notebook Sample - Python](notebooks/evaluation.ipynb)
