# EnLang v2.0.0 Compiler Architecture Reference
==============================================================================

## Overview
The EnLang compiler follows a 7-stage deterministic pipeline decoupled from AI generation:
`Source -> NLP Normalizer -> Canonical EnLang -> Lexer -> Parser -> AST -> IR -> Semantic Analyzer -> Optimizer -> Modular Emitter`

## Pipeline Stages
1. **NLP Intent Normalizer (`enlang_core/nlp_engine/`)**:
   - Preprocesses raw natural English variations into canonical EnLang syntax.
   - Stage 1: Tokenizer & string literal preservation.
   - Stage 2: Context-aware synonym reduction.
   - Stage 3: Phrasal grammar rewriting (`store X in Y` -> `set Y to X`).
   - Stage 4: Expression canonicalization (`X at index Y` -> `X[Y]`).
   - Stage 5: Domain ambiguity detection (.enlg vs .enlgf vs .enlgd vs .enlgs vs .enlgdb).

2. **Deterministic Frontend (`enlang_core/parser/`)**:
   - Receives Canonical EnLang and generates universal AST nodes (`ast_nodes.py`).

3. **Intermediate Representation (`enlang_core/ir/`)**:
   - Backend-agnostic IR instructions enabling multi-target code generation.

4. **Semantic Analyzer (`enlang_core/analyzer/`)**:
   - Validates symbol tables, scoping rules, function signatures, and type inference.

5. **Modular Target Emitters (`enlang_core/emitters/`)**:
   - Generates native output for Python 3, HTML5, CSS3, JavaScript ES6+, and SQLite.
