"""Context-Aware Synonym Reduction Engine."""
import re

class SynonymEngine:
    """Reduces thousands of natural English verb and noun variations to canonical keywords."""
    SYNONYM_MAP = [
        (r'\b(?:compute|determine|evaluate|find|calculate)\b', 'calculate'),
        (r'\b(?:print|show|output|log)\b', 'display'),
        (r'\b(?:let|store|assign|save)\b', 'set'),
        (r'\b(?:same as|matches|equals)\b', 'is equal to'),
        (r'\b(?:differs from)\b', 'is not equal to'),
        (r'\b(?:contained in|present in)\b', 'is in'),
    ]

    @classmethod
    def normalize_synonyms(cls, text):
        res = text
        for pat, repl in cls.SYNONYM_MAP:
            res = re.sub(pat, repl, res, flags=re.IGNORECASE)
        # Context-aware rewriting for 'put'
        if re.search(r'\bput\s+(.+?)\s+into\s+table\b', res, flags=re.IGNORECASE):
            res = re.sub(r'\bput\s+(.+?)\s+into\s+table\s+([a-zA-Z_]\w*)', r'insert \1 into \2', res, flags=re.IGNORECASE)
        elif re.search(r'\bput\s+(.+?)\s+into\s+([a-zA-Z_]\w*)', res, flags=re.IGNORECASE):
            res = re.sub(r'\bput\s+(.+?)\s+into\s+([a-zA-Z_]\w*)', r'add \1 to \2', res, flags=re.IGNORECASE)
        elif re.search(r'\bput\s+(.+?)\s+in\s+([a-zA-Z_]\w*)', res, flags=re.IGNORECASE):
            res = re.sub(r'\bput\s+(.+?)\s+in\s+([a-zA-Z_]\w*)', r'set \2 to \1', res, flags=re.IGNORECASE)
        return res
