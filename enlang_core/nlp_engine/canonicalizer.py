"""Expression Canonicalizer for Natural Indexing and Slicing."""
import re

class ExpressionCanonicalizer:
    """Canonicalizes natural language array access and slice ranges into bracket notation."""
    @classmethod
    def canonicalize(cls, text):
        res = text
        # Multi-word slice with length of: x from a to length of x -> x[a:len(x)]
        res = re.sub(r'\b([a-zA-Z_]\w*)\s+from\s+(.+?)\s+to\s+(length\s+of\s+[a-zA-Z_]\w*|[a-zA-Z_]\w*|\d+)\b', r'\1[\2:\3]', res, flags=re.IGNORECASE)
        # Natural indexing: x at index i -> x[i]
        res = re.sub(r'\b([a-zA-Z_]\w*)\s+at\s+index\s+([a-zA-Z_]\w*|\d+)\b', r'\1[\2]', res, flags=re.IGNORECASE)
        # 4th item of x -> x[4]
        res = re.sub(r'\b(\d+)(?:st|nd|rd|th)\s+(?:item|element|character|char)\s+(?:of|in)\s+([a-zA-Z_]\w*)\b', r'\2[\1]', res, flags=re.IGNORECASE)
        return res
