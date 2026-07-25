"""
EnLang Natural Language Processing (NLP) Engine
Provides Fuzzy Intent Matching, Entity Extraction, Token Normalization,
Native Sentiment / Keyword / Similarity primitives, and ML Dataset Helpers.
"""

import re
import math
import csv
from typing import Tuple, Dict, Any, List, Optional

# Positive & Negative Sentiment Lexicon for lightweight NLP analysis
POSITIVE_WORDS = {'good', 'great', 'awesome', 'excellent', 'fantastic', 'superb', 'happy', 'love', 'wonderful', 'successful', 'best', 'smooth', 'easy'}
NEGATIVE_WORDS = {'bad', 'terrible', 'horrible', 'poor', 'awful', 'sad', 'hate', 'worst', 'failed', 'error', 'slow', 'difficult', 'bug'}

class NLPParser:
    def __init__(self):
        # Conversational / Filler words to strip out for flexible natural input
        self.filler_patterns = [
            r'^\s*(please|kindly|can\s+you|could\s+you|would\s+you|i\s+want\s+to|let\s+us|lets)\s+',
            r'^\s*(hey|hi|hello|enlang)\s*,?\s*',
        ]

    def normalize_sentence(self, text: str) -> str:
        """Strips conversational filler phrases and normalizes whitespace."""
        res = text.strip()
        for pat in self.filler_patterns:
            res = re.sub(pat, '', res, flags=re.IGNORECASE)
        return res.strip()

    def parse_intent(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parses fuzzy intent when standard syntax matcher fails.
        Returns a structured dictionary with intent type and extracted parameters.
        """
        clean_text = self.normalize_sentence(text)

        # Fuzzy Intent 1: Variable assignment (e.g. "assign 100 to score", "make score 100", "create variable score with value 100")
        m = re.match(r'^(?:assign|store|put|make|create\s+variable)\s+(.+?)\s+(?:to|in|as|with\s+value)\s+([a-zA-Z_]\w*)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "ASSIGNMENT", "target": m.group(2), "value": m.group(1)}

        m = re.match(r'^(?:create\s+variable|initialize)\s+([a-zA-Z_]\w*)\s+(?:to|as|with|with\s+value)\s+(.+)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "ASSIGNMENT", "target": m.group(1), "value": m.group(2)}

        # Fuzzy Intent 2: Output (e.g. "please print out the total sum", "say Hello World", "log the result")
        m = re.match(r'^(?:print\s+out|output|say|log|display\s+message)\s+(.+)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "OUTPUT", "value": m.group(1)}

        # Fuzzy Intent 3: NLP Operations (e.g. "check sentiment of text into s", "find keywords in text into kw")
        m = re.match(r'^(?:analyze|check|find|get)\s+sentiment\s+(?:of|for)\s+(.+?)\s+(?:and\s+store\s+in|into|as)\s+([a-zA-Z_]\w*)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "NLP_SENTIMENT", "target": m.group(2), "text": m.group(1)}

        m = re.match(r'^(?:extract|get|find)\s+keywords\s+(?:from|in)\s+(.+?)\s+(?:and\s+store\s+in|into|as)\s+([a-zA-Z_]\w*)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "NLP_KEYWORDS", "target": m.group(2), "text": m.group(1)}

        m = re.match(r'^(?:calculate|compute|check)\s+similarity\s+between\s+(.+?)\s+and\s+(.+?)\s+(?:and\s+store\s+in|into|as)\s+([a-zA-Z_]\w*)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "NLP_SIMILARITY", "target": m.group(3), "text1": m.group(1), "text2": m.group(2)}

        return None

# Built-in NLP Helper functions executed in runtime
def analyze_sentiment(text: str) -> str:
    """Analyzes text sentiment and returns 'Positive', 'Negative', or 'Neutral'."""
    tokens = re.findall(r'\b\w+\b', str(text).lower())
    pos_count = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg_count = sum(1 for t in tokens if t in NEGATIVE_WORDS)

    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    return "Neutral"

def extract_keywords(text: str, max_words: int = 5) -> List[str]:
    """Extracts prominent non-stopword tokens from text."""
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'this', 'that', 'it', 'with'}
    tokens = [t.lower() for t in re.findall(r'\b[a-zA-Z]{3,}\b', str(text)) if t.lower() not in stopwords]
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    sorted_words = sorted(freq.keys(), key=lambda w: freq[w], reverse=True)
    return sorted_words[:max_words]

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculates Jaccard similarity score between two texts (0.0 to 1.0)."""
    set1 = set(re.findall(r'\b\w+\b', str(text1).lower()))
    set2 = set(re.findall(r'\b\w+\b', str(text2).lower()))
    if not set1 or not set2:
        return 0.0
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return round(len(intersection) / len(union), 2)

def load_csv_dataset(file_path: str) -> Tuple[List[str], List[int]]:
    """Loads text and binary target labels from a CSV dataset file."""
    x_data, y_data = [], []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                x_data.append(row[0])
                try:
                    y_data.append(int(row[1]))
                except ValueError:
                    y_data.append(0)
    return x_data, y_data

def train_ml_classifier(x_data: List[str], y_data: List[int], train_pct: int = 80, test_pct: int = 20):
    """Trains a TF-IDF + Multinomial Naive Bayes classifier model on dataset with split ratio."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    test_size = float(test_pct) / 100.0
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=test_size, random_state=42)

    vec = TfidfVectorizer(stop_words='english', max_features=5000)
    x_train_v = vec.fit_transform(x_train)
    x_test_v = vec.transform(x_test)

    clf = MultinomialNB()
    clf.fit(x_train_v, y_train)

    accuracy = round(accuracy_score(y_test, clf.predict(x_test_v)) * 100, 2)

    class EnLangMLModel:
        def __init__(self, classifier, vectorizer, accuracy):
            self.classifier = classifier
            self.vectorizer = vectorizer
            self.accuracy = accuracy

    return EnLangMLModel(clf, vec, accuracy)
