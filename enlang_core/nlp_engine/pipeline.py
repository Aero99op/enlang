"""Master 5-Stage Pre-Parser Intent Preprocessing Pipeline."""
from .tokenizer import PreprocessTokenizer
from .synonym_engine import SynonymEngine
from .grammar_rewriter import GrammarRewriter
from .canonicalizer import ExpressionCanonicalizer
from .ambiguity_detector import AmbiguityDetector

class NLPPipeline:
    """Orchestrates the 5-stage pre-parser intent normalization pipeline."""
    def __init__(self):
        self.tokenizer = PreprocessTokenizer()

    def process(self, raw_text, file_ext=".enlg"):
        # Stage 1: Tokenize and protect string literals
        protected_text = self.tokenizer.protect_strings(raw_text)
        
        # Stage 2: Context-aware synonym reduction
        syn_text = SynonymEngine.normalize_synonyms(protected_text)
        
        # Stage 3: Phrasal grammar rewriting
        rewritten_text = GrammarRewriter.rewrite(syn_text)
        
        # Stage 4: Expression canonicalization
        canon_text = ExpressionCanonicalizer.canonicalize(rewritten_text)
        
        # Stage 5: Restore string literals
        final_canonical = self.tokenizer.restore_strings(canon_text)
        
        # Determine domain and confidence
        domain, conf = AmbiguityDetector.detect_domain(final_canonical, file_ext)
        return final_canonical, domain, conf
