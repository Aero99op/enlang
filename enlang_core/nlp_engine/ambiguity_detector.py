"""Domain Disambiguation and Confidence Scoring Engine."""

class AmbiguityDetector:
    """Detects domain context and scores intent confidence based on file extension and keyword density."""
    DOMAIN_KEYWORDS = {
        ".enlg": ["calculate", "set", "function", "return", "if", "for", "while"],
        ".enlgf": ["hero", "nav", "button", "form", "table", "card", "modal", "create"],
        ".enlgd": ["style", "theme", "margin", "padding", "border", "radius", "shadow", "glass"],
        ".enlgs": ["when clicked", "on click", "fetch", "document", "alert", "toggle"],
        ".enlgdb": ["table", "columns", "insert", "select", "query", "where"]
    }

    @classmethod
    def detect_domain(cls, text, file_ext=".enlg"):
        # Explicit file extension always overrides ambiguity with 98% confidence
        if file_ext in cls.DOMAIN_KEYWORDS:
            return file_ext, 0.98
        # Otherwise, score by keyword density
        scores = {}
        for ext, kw_list in cls.DOMAIN_KEYWORDS.items():
            count = sum(1 for kw in kw_list if kw in text.lower())
            scores[ext] = count
        best_ext = max(scores, key=scores.get)
        total = sum(scores.values()) or 1
        confidence = min(0.95, (scores[best_ext] / total) + 0.2)
        return best_ext, confidence
