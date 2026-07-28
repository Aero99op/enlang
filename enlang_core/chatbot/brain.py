"""Grounded AI Reasoning Engine for EnLang."""
from .prompt_builder import SpecPromptBuilder
from ..nlp_engine.pipeline import NLPPipeline

class AIBrain:
    """Orchestrates intent normalization and spec-grounded prompt building for LLM queries."""
    def __init__(self):
        self.prompt_builder = SpecPromptBuilder()
        self.nlp_pipeline = NLPPipeline()

    def prepare_query(self, user_text: str, file_ext: str = ".enlg"):
        """Preprocesses user text through NLP pipeline and generates spec-grounded system prompt."""
        canonical_code, domain, conf = self.nlp_pipeline.process(user_text, file_ext)
        sys_prompt = self.prompt_builder.build_system_prompt(domain)
        return {
            "canonical_code": canonical_code,
            "domain": domain,
            "confidence": conf,
            "system_prompt": sys_prompt
        }
