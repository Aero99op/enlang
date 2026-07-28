"""Unit tests for EnLang 5-Stage Pre-Parser NLP Pipeline."""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enlang_core.nlp_engine.pipeline import NLPPipeline

class TestNLPPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = NLPPipeline()

    def test_synonym_reduction(self):
        code, domain, conf = self.pipeline.process("compute 5 + 10", ".enlg")
        self.assertIn("calculate", code)
        self.assertEqual(domain, ".enlg")

    def test_grammar_rewriting(self):
        code, _, _ = self.pipeline.process("store 100 in my_var", ".enlg")
        self.assertEqual(code.strip(), "set my_var to 100")

    def test_canonical_indexing(self):
        code, _, _ = self.pipeline.process("set x to s at index left", ".enlg")
        self.assertEqual(code.strip(), "set x to s[left]")

    def test_context_aware_put(self):
        code_var, _, _ = self.pipeline.process("put 5 in x", ".enlg")
        self.assertEqual(code_var.strip(), "set x to 5")
        
        code_list, _, _ = self.pipeline.process("put user into users", ".enlg")
        self.assertEqual(code_list.strip(), "add user to users")
        
        code_db, _, _ = self.pipeline.process("put user into table users", ".enlgdb")
        self.assertEqual(code_db.strip(), "insert user into users")

if __name__ == "__main__":
    unittest.main()
