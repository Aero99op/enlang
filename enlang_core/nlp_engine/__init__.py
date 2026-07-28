"""EnLang Natural Language Processing (NLP) Engine & Pre-Parser Pipeline."""
from .pipeline import NLPPipeline
from .fuzzy_parser import (
    NLPParser, analyze_sentiment, extract_keywords, calculate_similarity,
    POSITIVE_WORDS, NEGATIVE_WORDS
)
