### Intent

Code:

```python
print(intent_func("I want to make a reservation for 2 people at 7pm on Friday at Friday's Restaurant"))

print(intent_func("What is my upcoming travel itinerary"))

print(intent_func("What is the weather like in London"))
```

Output:

```Text
{
  "intent": "Reserve",
  "entities": ["Friday's Restaurant", "2 people", "7pm", "Friday"]
}
{
  "intent": "GetItinerary",
  "entities": []
}
{
  "intent": "GetWeather",
  "entities": ["London"]
}
```
