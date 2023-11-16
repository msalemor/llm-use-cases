### Intent

Code:

```python
# Execute the SK function
total_score = 0
for review in reviews:
    data = str(sentiment_func(review))
    score = json.loads(data)['sentiment']
    print(f'Review: {review[0:60]}, Score: {score}')
    total_score += score

print("Average sentiment score: {}".format(total_score/len(reviews)))
```

Output:

```Text
Review: Mark S.: "This smartphone has exceeded my expectations in ev, Score: 10
Review: Maya L.: "I've been using this phone for a few weeks now, an, Score: 9
Review: Positive Review - David W.: "What sets this smartphone apart, Score: 9
Review: Jennifer P.: "The smartphone is decent overall. The camera t, Score: 5
Review: Ryan M.: "This smartphone is a complete disappointment. The , Score: 2
Average sentiment score: 7.0
```
