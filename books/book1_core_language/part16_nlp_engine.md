# Part 16: Built-in Natural Language Processing (NLP) Engine

One of EnLang's most unique capabilities is built-in Natural Language Processing (NLP). You can perform sentiment analysis, keyword extraction, and text similarity calculations using plain English syntax.

## 1. Sentiment Analysis (`analyze sentiment`)

Analyze whether a body of text is positive, negative, or neutral:

```enlg
define text review as "EnLang is an amazingly intuitive and fast language!"

analyze sentiment of review and store in sentiment_score
display "Sentiment: " + sentiment_score
```

### Transpiled Target Output:
```python
review = "EnLang is an amazingly intuitive and fast language!"
from enlang_core.nlp_engine import analyze_sentiment
sentiment_score = analyze_sentiment(review)
print("Sentiment: " + str(sentiment_score))
```

## 2. Keyword Extraction (`extract keywords`)

Automatically extract key terms from unstructured text:

```enlg
define text article as "Artificial intelligence and compiler design are advancing rapidly in 2026."

extract keywords from article into keywords_list
display "Keywords: " + keywords_list
```

### Transpiled Target Output:
```python
article = "Artificial intelligence and compiler design are advancing rapidly in 2026."
from enlang_core.nlp_engine import extract_keywords
keywords_list = extract_keywords(article)
print("Keywords: " + str(keywords_list))
```

## 3. Text Similarity Calculation (`calculate similarity`)

Compare two text strings and calculate their similarity score:

```enlg
define text text1 as "Build full-stack web applications in English"
define text text2 as "Create web apps using natural English code"

calculate similarity between text1 and text2 and store in score
display "Similarity Score: " + score
```

### Transpiled Target Output:
```python
text1 = "Build full-stack web applications in English"
text2 = "Create web apps using natural English code"
from enlang_core.nlp_engine import calculate_similarity
score = calculate_similarity(text1, text2)
print("Similarity Score: " + str(score))
```
