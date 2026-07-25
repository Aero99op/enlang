"""
EnLang Natural Language Processing (NLP) Engine
Provides Fuzzy Intent Matching, Entity Extraction, Token Normalization,
Native Sentiment / Keyword / Similarity primitives, and General ML Dataset & Classifier Helpers.
"""

import re
import math
import csv
from typing import Tuple, Dict, Any, List, Optional, Union

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

        # Fuzzy Intent 1: Variable assignment
        m = re.match(r'^(?:assign|store|put|make|create\s+variable)\s+(.+?)\s+(?:to|in|as|with\s+value)\s+([a-zA-Z_]\w*)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "ASSIGNMENT", "target": m.group(2), "value": m.group(1)}

        m = re.match(r'^(?:create\s+variable|initialize)\s+([a-zA-Z_]\w*)\s+(?:to|as|with|with\s+value)\s+(.+)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "ASSIGNMENT", "target": m.group(1), "value": m.group(2)}

        # Fuzzy Intent 2: Output
        m = re.match(r'^(?:print\s+out|output|say|log|display\s+message)\s+(.+)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "OUTPUT", "value": m.group(1)}

        # Fuzzy Intent 3: NLP Operations
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

def load_csv_dataset(file_path: str, text_col: int = 0, label_col: int = 1) -> Tuple[List[str], List[Any]]:
    """Universal CSV dataset loader for text features and target labels."""
    x_data, y_data = [], []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        next(reader, None) # Skip header
        for row in reader:
            if len(row) > max(text_col, label_col):
                x_val = row[text_col]
                y_val = row[label_col].strip()
                # Parse numeric or keep string label
                if y_val.isdigit() or (y_val.startswith('-') and y_val[1:].isdigit()):
                    y_parsed = int(y_val)
                else:
                    try:
                        y_parsed = float(y_val)
                    except ValueError:
                        y_parsed = y_val
                x_data.append(x_val)
                y_data.append(y_parsed)
    return x_data, y_data

def train_ml_classifier(x_data: List[str], y_data: List[Any], model_type: str = "naive bayes", train_pct: int = 80, test_pct: int = 20):
    """
    Universal ML Classifier Trainer.
    Supports Naive Bayes, Logistic Regression, Random Forest, Decision Tree, SVM with dynamic train-test split ratios.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    test_size = float(test_pct) / 100.0 if test_pct > 0 else 0.20
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=test_size, random_state=42)

    vec = TfidfVectorizer(stop_words='english', max_features=5000)
    x_train_v = vec.fit_transform(x_train)
    x_test_v = vec.transform(x_test)

    m_lower = str(model_type).lower()
    if 'logistic' in m_lower:
        from sklearn.linear_model import LogisticRegression
        clf = LogisticRegression(max_iter=1000)
    elif 'random' in m_lower or 'forest' in m_lower:
        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=100)
    elif 'tree' in m_lower:
        from sklearn.tree import DecisionTreeClassifier
        clf = DecisionTreeClassifier()
    elif 'svm' in m_lower or 'support vector' in m_lower:
        from sklearn.svm import SVC
        clf = SVC(probability=True)
    else:
        # Default: Multinomial Naive Bayes
        from sklearn.naive_bayes import MultinomialNB
        clf = MultinomialNB()

    clf.fit(x_train_v, y_train)
    accuracy = round(accuracy_score(y_test, clf.predict(x_test_v)) * 100, 2)

    class EnLangMLModel:
        def __init__(self, classifier, vectorizer, accuracy, model_name):
            self.classifier = classifier
            self.vectorizer = vectorizer
            self.accuracy = accuracy
            self.model_name = model_name

        def predict_text(self, text: str) -> str:
            in_v = self.vectorizer.transform([text])
            pred = self.classifier.predict(in_v)[0]
            if hasattr(self.classifier, "predict_proba"):
                proba = self.classifier.predict_proba(in_v)[0]
                conf = round(max(proba) * 100, 2)
            else:
                conf = 100.0
            
            if pred == 1 or str(pred).lower() in ("1", "spam", "true", "yes", "positive"):
                return f"[SPAM DETECTED] (Confidence: {conf}%)"
            elif pred == 0 or str(pred).lower() in ("0", "ham", "false", "no", "negative"):
                return f"[NOT SPAM / HAM] (Confidence: {conf}%)"
            return f"[PREDICTION: {pred}] (Confidence: {conf}%)"

    return EnLangMLModel(clf, vec, accuracy, model_type)
