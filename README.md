# OpenAI - Common Use Cases

## Common Use Cases

- Recommendation system
- Language transation
- Personalization and content generation
- Prompting and complition from your own content
- Image generation
- Image recognition

### Recommendation System

OpenAI can be used to develop recommendation systems that can suggest products, services, or content to users based on their preferences and behavior.

```mermaid
flowchart LR
  A((start))-->B{From curated<br/>content}  
  B--No-->C[Do not<br/>add context]
  B--Yes-->D[Add curated<br/>content as context]
  C-->E[Prompt<br/>OpenAI API]
  D-->E
```

Examples:

- Without context
```python
prompt = "List the best restaurants in downtown London."
```

- With context
```python
list = get_restaurants("London").join("\n")
prompt = "List the best restaurants in downtown London. The answer should come from the following list:\n{list}"
```

### Language Translation

OpenAI can be used to develop language translation models that can translate text from one language to another.

```mermaid
flowchart LR
  A((start))-->B[Add text<br/>to be translated]
  B-->O[Prompt<br/>OpenAI API]
```

Examples:

```python
source_lang = "English" 
target_lang = "Japanese"
text = load_text()
prompt = "Translate the following text from {source_lang} to {target_lang}:\n{text}"
```


### Personalization & Content Generation

OpenAI can be used to develop personalized content and experiences for users based on their interests and behavior.

```mermaid
flowchart LR
  A((start))-->B[Get structured<br/>properties]
  B-->D[Build a simple description<br/>from the properties]
  D-->O[Prompt<br/>OpenAI API]
```

Examples:

```python
item = {"make","Ford","model":"Explorer","year":2020,"Color":"red","condition":"excellent"}
item_description = get_item_description(item)
prompt = "Get a full sales description for the following used vehicle:\n" + item_description
```

```
Prompt:
Get a full sales description for a used very good condition red 2020 Ford Explorer

Completion:
This used 2020 Ford Explorer is in very good condition and is a great choice for anyone looking for a reliable and stylish SUV. It has a bold red exterior and a comfortable interior with plenty of room for passengers and cargo. The exterior features a sleek design with a bold grille, LED headlights, and fog lights. The interior is equipped with leather seating, power windows and locks, a power liftgate, and a rearview camera. The 3.5L V6 engine provides plenty of power and the 6-speed automatic transmission ensures smooth shifting. The Ford Explorer also comes with a variety of safety features such as blind spot monitoring, lane keeping assist, and adaptive cruise control. This vehicle is perfect for anyone looking for a reliable and stylish SUV.
```

### Search Your Own Content

