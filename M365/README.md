# M365 Copilots - Beyond the Basics

## Overview

Office 365 copilots are powerful intent engines. In other words, the copilots will not just execute your prompt, your prompt will be analyzed first, and then the Copil will decide if it has to call other services to get the weather, to get data web or corporate data (a la RAG), or just call an GenAI engine. Understanding the intent nature of a Copilot prompt, should help you maximize of productiviy of using these copilots.

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
You are a sentiment analysis bot. The user will provide a text and you need to classify it as positive,
neutral or negative. Respond in JSON format. No prologue or epilogue.

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
You are bot that can help evalute the clarity and complexity of a text. Provide a complexity and clarity scores
between 1-10 with ten being not complex and clear. Provide a reason for the scores. Respond in JSON format. No
prologue or epilogue.

user:
Azure API Management (APIM) is an intricate orchestration platform that facilitates the governance and
operationalization of APIs within a multifaceted cloud ecosystem. It encompasses a plethora of functionalities,
including but not limited to, an API gateway, developer engagement portal, and comprehensive lifecycle management
apparatus. The API gateway operates as an intermediary, orchestrating the ingress and egress of API traffic, while
enforcing a myriad of policies and routing protocols.

Copilot:
{
  "complexity": 8,
  "clarity": 4,
  "reason": "The text uses complex language and technical jargon, making it difficult for readers unfamiliar with the subject to understand. The sentence structure is intricate, contributing to the overall complexity. However, the text is well-organized, which slightly aids clarity."
}
```

### Copilots can connect to the web and corporate data

```
A saw is a tool with a serrated blade used for cutting wood, metal, or other materials

Copilot Web:
A saw is a tool with a serrated blade used for cutting wood, metal, or other materials

Copilot Work:
A Secure Admin Workstation (SAW) is a securely controlled and provisioned workstation designed for managing valuable production systems. 
```

## RAG with Word

- Paste all the text you think you will need to query
- Save the word document
> Note: On the copilot settings, consider turning off the `web content` to force to use only the content on the document
- On the copilot type, `With this doc, in one paragraph, what is the ...`

> Note: to make sure that copilot is responing correctly, the Copilot response should include references to the paragraphs where it got the information.


## Excel analysis

### Overview

Excel Copilot is an even more specialized copilot. In many cases, Copilot will write an application in the background, execute the application, and proivde the results of running this application presented using maybe both Excel sheets and copilot dialogs. In some agent systems. this functionality is called Code Interpreter.
