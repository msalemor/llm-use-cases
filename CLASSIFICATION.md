### Classification

Code:

```python
prompt_template = """For the following list of animals:

- Dog
- Cat
- Elephant
- Dolphin
- Shark
- Whale
- Snake

Can you classify and list by animal type?
"""

classification_func = kernel.create_semantic_function(prompt_template, 
                            max_tokens=common.get_max_tokens('short'), 
                            temperature=0.3)

print(classification_func())
```

Output:

```Text
Mammals:
- Dog
- Cat
- Elephant
- Dolphin
- Whale

Fish:
- Shark

Reptiles:
- Snake
```