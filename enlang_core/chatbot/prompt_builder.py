"""Spec-Driven AI Prompt Generator for Zero-Hallucination EnLang Code Generation."""
import os
import json

class SpecPromptBuilder:
    """Reads spec/ files to dynamically build system prompts grounded in formal language specifications."""
    def __init__(self, spec_dir=None):
        if spec_dir is None:
            # Locate spec/ relative to package root
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            self.spec_dir = os.path.join(base, 'spec')
        else:
            self.spec_dir = spec_dir
        self.spec_data = {}
        self.load_specs()

    def load_specs(self):
        for fname in ['enlang_spec.json', 'keywords.json', 'operators.json', 'types.json', 'builtins.json']:
            path = os.path.join(self.spec_dir, fname)
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        self.spec_data[fname] = json.load(f)
                except Exception:
                    pass

    def build_system_prompt(self, domain=".enlg") -> str:
        prompt_lines = [
            "You are EnLang AI, the official AI assistant for EnLang v2.0.0.",
            "You MUST generate canonical code following this EXACT machine-readable specification:",
            ""
        ]
        if 'keywords.json' in self.spec_data:
            prompt_lines.append("### RESERVED CANONICAL KEYWORDS:")
            prompt_lines.append(json.dumps(self.spec_data['keywords.json'], indent=2))
            prompt_lines.append("")
        if 'operators.json' in self.spec_data:
            prompt_lines.append("### SUPPORTED OPERATORS:")
            prompt_lines.append(json.dumps(self.spec_data['operators.json'], indent=2))
            prompt_lines.append("")
        prompt_lines.append(f"Generate valid EnLang code for domain: {domain}")
        return "\n".join(prompt_lines)
