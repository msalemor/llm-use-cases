### Intent

Code:

```python
# Execute the SK function
prompt_template = """You are an agent who can help determine how easy it would be for an English speaker to learn to sing a song in Spanish. Easy songs have straightforward vocabulary and grammar and avoid complex sentence structures, metaphors, poetic structures and language, and uncommon words. Songs with familiar or universal themes, such as love, emotions, or everyday activities, can be easier for learners to relate to and understand. It helps when the context of the song is relatable to the listener. 

Rate the following song lyrics in Spanish from 1-10, with 10 being the hardest, for an English speaker to learn:

Lyrics: \"\"\"
{{$input}}
\"\"\"

Output format:
{ \"score\":-1, \"explanation\": \"\"}

Provide an explanation in one sentence. Output in JSON format only.
"""
scoring_func = kernel.create_semantic_function(prompt_template, max_tokens=50, temperature=0.1)

for song in songs:
    print(f'Title: {song[0]}, Score: {scoring_func(song[1])}')
```

Output:

```Text
Title: La Canción de los Gatos, Score: {"score":2, "explanation": "The straightforward vocabulary and grammar, familiar theme of cats, and repetition of the chorus make this song relatively easy for an English speaker to learn."}
Title: Conquistando el Amor, Score: {"score": 10, "explanation": "The song contains complex metaphors, poetic language, and uncommon words, making it very difficult for an English speaker to learn."}
```
