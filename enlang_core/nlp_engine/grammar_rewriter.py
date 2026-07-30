"""Phrasal Structure Grammar Rewriter."""
import re

class GrammarRewriter:
    """Transforms conversational sentence structures into canonical EnLang syntax."""
    REWRITE_RULES = [
        (r'^\s*(?:set|store|save|put)\s+(.+?)\s+in\s+([a-zA-Z_]\w*(?:\[[^\]]+\])*)\s*:?\s*$', r'set \2 to \1'),
        (r'^\s*(?:set|store|save|put)\s+(.+?)\s+to\s+([a-zA-Z_]\w*(?:\[[^\]]+\])*)\s*:?\s*$', r'set \2 to \1'),
        (r'^\s*loop\s+([a-zA-Z_]\w*)\s+from\s+(.+?)\s+to\s+(.+?)\s*:?\s*$', r'for each \1 from \2 to \3:'),
        (r'\b([a-zA-Z_]\w*|\d+)\s+is\s+not\s+divisible\s+by\s+([a-zA-Z_]\w*|\d+)\b', r'\1 % \2 != 0'),
        (r'\b([a-zA-Z_]\w*|\d+)\s+is\s+divisible\s+by\s+([a-zA-Z_]\w*|\d+)\b', r'\1 % \2 == 0'),
        (r'\b([a-zA-Z_]\w*|\d+)\s+is\s+even\b', r'\1 % 2 == 0'),
        (r'\b([a-zA-Z_]\w*|\d+)\s+is\s+odd\b', r'\1 % 2 != 0'),
    ]

    @classmethod
    def rewrite(cls, text):
        res = text
        for pat, repl in cls.REWRITE_RULES:
            res = re.sub(pat, repl, res, flags=re.IGNORECASE)
        return res
