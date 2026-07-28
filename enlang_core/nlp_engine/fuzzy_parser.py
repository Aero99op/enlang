"""Fuzzy Intent Parser and Native NLP Runtime Primitives."""
import re
from typing import Tuple, Dict, Any, List, Optional

POSITIVE_WORDS = {'good', 'great', 'awesome', 'excellent', 'fantastic', 'superb', 'happy', 'love', 'wonderful', 'successful', 'best', 'smooth', 'easy'}
NEGATIVE_WORDS = {'bad', 'terrible', 'horrible', 'poor', 'awful', 'sad', 'hate', 'worst', 'failed', 'error', 'slow', 'difficult', 'bug'}

class NLPParser:
    def __init__(self):
        self.filler_patterns = [
            r'^\s*(please|kindly|can\s+you|could\s+you|would\s+you|i\s+want\s+to|let\s+us|lets)\s+',
            r'^\s*(hey|hi|hello|enlang)\s*,?\s*',
        ]

    def normalize_sentence(self, text: str) -> str:
        res = text.strip()
        for pat in self.filler_patterns:
            res = re.sub(pat, '', res, flags=re.IGNORECASE)
        return res.strip()

    def parse_intent(self, text: str) -> Optional[Dict[str, Any]]:
        clean_text = self.normalize_sentence(text)

        m = re.match(r'^(?:assign|store|put|make|create\s+variable)\s+(.+?)\s+(?:to|in|as|with\s+value)\s+([a-zA-Z_]\w*)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "ASSIGNMENT", "target": m.group(2), "value": m.group(1)}

        m = re.match(r'^(?:create\s+variable|initialize)\s+([a-zA-Z_]\w*)\s+(?:to|as|with|with\s+value)\s+(.+)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "ASSIGNMENT", "target": m.group(1), "value": m.group(2)}

        m = re.match(r'^(?:print\s+out|output|say|log|display\s+message)\s+(.+)$', clean_text, re.IGNORECASE)
        if m:
            return {"intent": "OUTPUT", "value": m.group(1)}

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

def analyze_sentiment(text: str) -> str:
    tokens = re.findall(r'\b\w+\b', str(text).lower())
    pos_count = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg_count = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    return "Neutral"

def extract_keywords(text: str, max_words: int = 5) -> List[str]:
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'this', 'that', 'it', 'with'}
    tokens = [t.lower() for t in re.findall(r'\b[a-zA-Z]{3,}\b', str(text)) if t.lower() not in stopwords]
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    sorted_words = sorted(freq.keys(), key=lambda w: freq[w], reverse=True)
    return sorted_words[:max_words]

def calculate_similarity(text1: str, text2: str) -> float:
    set1 = set(re.findall(r'\b\w+\b', str(text1).lower()))
    set2 = set(re.findall(r'\b\w+\b', str(text2).lower()))
    if not set1 or not set2:
        return 0.0
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return round(len(intersection) / len(union), 2)
