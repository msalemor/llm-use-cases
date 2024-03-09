# Improving RAG results

## Overview

So you have developed an intelligent application that leverages RAG. You are getting answers, but would like to get better answers. This document provides recommendations for improving RAG (Retrieval-Augmented Generation) results. It suggests techniques such as text splitting, determining optimal chunk size, setting result limits and model context window, adjusting relevance scores, utilizing native vector database nearest search functionality, and performing trimming and document cleanup. It also suggests taking control of the ingestion process, creating and ingesting synthetic documents, and considering full document summarization if necessary. Evaluating the results and potentially involving subject matter experts in writing baseline responses is emphasized. Overall, these recommendations aim to enhance the performance and accuracy of RAG.

## Adjust the RAG paramenters

- Text splitting techniques
  - Split by token counts and overflow
  - Split by paragrpahs
  - Put markers in the documents
  - Maybe even consider manual splitting
  - Etc.

- Text chunk size
  - Determine what is the best chunk size for your content  

- Result limits & model context window
  - Some models support 4k, 32k, and 128k context windows
  - Try to take advantage of the context window, but be mindful of costs

- Relevance
  - Increase or decrease the relevance score to get more or less chunks from the vector database

- Native vector database nearest search functionality
  - Evaluate if the vector database has better search functionality
    - For example, in Azure AI Search for example, Hybrid Search is a powerful technique that combines both full text and vector queries to retrieve relevant information from a search index.

## Trimming and document cleaunup

- For example, converting PDF documents to text may generate a lot of white space and character
- Evaluate if there's a way to trim and clean these documents

## Take control of ingestion

- Automatic ingesting techniques may be great for POC scenarios
- Improving the RAG results may involve taking control of the ingestion stage where you may be able to apply different text splitting techniques and chunk sizes to your data.

## Syntethic documents

- Create and ingest synthetic documents
- If you know that your users will be searching for data, maybe there's an opportunity to summarize, and classify the documents for ingestion into synthetic documents specially designed for RAG consumption.

## Move to full summarization, if needed

- If you are looking the most precise answers, you may have to summarize entire documents
- Under this summarization technique, a map reduce recursive tecnhique is applied to pieces of of a ducument, and then get a final summary.

## Evaluate your results

- Make sure you evaluate your results
- It many instances, SMEs may be needed to write the baseline responses.

Example:
- [Evaluation Notebook Sample](https://github.dev/msalemor/llm-use-cases/notebooks/evaluation.ipynb)