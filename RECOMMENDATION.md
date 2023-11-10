### Recommendation System

OpenAI can be used to develop recommendation systems that can suggest products, services, or content to users based on their preferences and behavior.

```mermaid
flowchart LR
  A((Start))-->B{From curated<br/>content}
  B--No-->O([OpenAI])
  B--Yes-->D([Add curated<br/>content as context])
  D-->O
  classDef blue fill:blue,color:#fefefe
  class A,B,O,D blue
```

Jupyter notebook:

- [Recommendation](https://github.com/msalemor/openai-use-cases/blob/main/notebooks/recommendation.ipynb)

Examples:

- Without context

```python
prompt = "List the best restaurants in Miami, FL."
```

- With context

```python
target_text=""
for restaurant in mock_get_restaurant_list("MIA"):
    target_text += f"{restaurant}\n"

prompt = f'List two top restaurants in Miami, FL\n{target_text}'
```
