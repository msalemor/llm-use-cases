# M365 Copilots - Beyond the Basics

## Advanced prompt techniques

### Add system and user prompts

```text
system:
you are an English to Spanish translator.

user:
Hello how are you?

Copilot
Hola, ¿cómo estás?
```

### Sentiment analysis, Evaluations and classifications

#### Sentiment Analysis

```text
system:
You are a sentiment analysis bot. The user will provide a text and you need to classify it as positive, neutral or negative. Respond in JSON format. No prologue or epilogue.

user:
The new telephone has amazing features and works flawlessly.

Copilot:
{
  "sentiment": "positive"
}
```
#### Evaluator

> Note: In evaluations and scoring it is important to return the reason for the score.

```text
system:
You are bot that can help evalute the clarity and complexity of a text. Provide a complexity and clarity scores between 1-10 with ten being not complex and clear. Provide a reason for the scores. Respond in JSON format. No prologue or epilogue.

user:
Azure API Management (APIM) is an intricate orchestration platform that facilitates the governance and operationalization of APIs within a multifaceted cloud ecosystem. It encompasses a plethora of functionalities, including but not limited to, an API gateway, developer engagement portal, and comprehensive lifecycle management apparatus. The API gateway operates as an intermediary, orchestrating the ingress and egress of API traffic, while enforcing a myriad of policies and routing protocols.
```

## RAG with Word

## Excel analysis
