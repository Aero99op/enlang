# EnLang v2.0.0 — The Grand Industrial Compiler & AI Ecosystem Blueprint
==============================================================================
VERSION: 2.0.0-SPEC | SPEC_REVISION: 2026.2 | STATUS: APPROVED MASTER SPECIFICATION

---

## 🏛️ 1. ARCHITECTURAL MANIFESTO & CORE PHILOSOPHY

1. **Parser Determinism First**: The core compiler is 100% deterministic, offline, and sub-millisecond fast. Natural English ambiguity, fuzzy matching, and intent normalization live strictly **before** the parser in the modular `nlp_engine/` preprocessing layer.
2. **Single Source of Truth (Manifest Pattern)**: All grammar rules, reserved keywords, operators, data types, and standard library modules are stored in separate, machine-readable JSON/EBNF files inside `spec/`. A central manifest (`enlang_spec.json`) links them together. The Lexer, Parser, Linter, AST, and AI Assistant (`enlang ai`) all consume this exact specification.
3. **First-Class AST & Intermediate Representation (IR)**: Compilation follows a layered pipeline: `Source -> Lexer -> Parser -> AST -> IR -> Semantic Analyzer -> Optimizer -> Modular Emitter`. The IR layer enables multi-backend generation (Python, HTML, CSS, JS, SQLite, Rust, Go, Java) without redesigning the frontend.
4. **Complete Decoupling (Compiler vs. AI)**: `enlang-core` operates independently as an offline, deterministic compiler. `enlang-ai` is an optional AI frontend that reads the formal spec and translates raw user intent into Canonical EnLang.

---

## 🔄 2. THE COMPLETE 7-STAGE COMPILATION PIPELINE

```
[ Raw Natural English Input (Any Style / Any Domain) ]
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ STAGE 1: NLP INTENT NORMALIZER (nlp_engine/)             │
│  1. Tokenizer ➔ 2. Context-Aware Synonyms ➔ Rewriter    │
│  3. Expression Canonicalizer ➔ 4. Ambiguity Detector     │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
               [ Canonical EnLang Code ]
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ STAGE 2: DETERMINISTIC LEXER & PARSER (parser/)          │
│  Produces standard Abstract Syntax Tree (AST Nodes)      │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ STAGE 3: INTERMEDIATE REPRESENTATION (ir/)               │
│  Low-level backend-agnostic IR (Instructions & Blocks)   │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ STAGE 4: SEMANTIC ANALYZER (analyzer/)                   │
│  Type checking, scope rules, duplicate symbols, returns  │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ STAGE 5: IR OPTIMIZER (optimizer/)                       │
│  Constant folding, dead code elimination, loop unrolling │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│ STAGE 6: MODULAR TARGET EMITTERS (emitters/)             │
│  Python 3 | HTML5 | CSS3 | JS ES6+ | SQLite | Future: Rust │
└──────────────────────────────────────────────────────────┘
```

---

## 📁 3. DIRECTORY & MODULE SPECIFICATION

```
d:\enlangg\
├── spec/                                # Single Source of Truth Specification
│   ├── enlang_spec.json                # Master Manifest linking all specs below
│   ├── grammar.ebnf                    # Formal EBNF Grammar Definition
│   ├── keywords.json                   # Reserved Keywords & Canonical Verbs
│   ├── operators.json                  # Math, Logical & Relational Operators
│   ├── types.json                      # Primitive & Compound Type Definitions
│   ├── builtins.json                   # Built-in Global Functions & Constants
│   ├── stdlib.json                     # Standard Library (Math, String, File, HTTP)
│   └── version.json                    # Component Versioning Manifest
│
├── docs/                                # Formal Reference Documentation
│   ├── LANGUAGE_REFERENCE.md           # Deep-dive language semantics
│   ├── GRAMMAR_REFERENCE.md            # EBNF and syntax rules
│   ├── STDLIB_REFERENCE.md             # Standard library docs
│   ├── AST_REFERENCE.md                # AST node specification
│   ├── COMPILER_ARCHITECTURE.md        # Pipeline & module documentation
│   └── CHANGELOG.md                    # Release and migration notes
│
├── enlang_core/
│   ├── nlp_engine/                      # Pre-Parser Natural English Preprocessor
│   │   ├── __init__.py
│   │   ├── tokenizer.py                # Lexical Token Extraction & Literal Protection
│   │   ├── synonym_engine.py           # Context-Aware Verb/Noun Canonicalization
│   │   ├── grammar_rewriter.py         # Phrasal Structure to Canonical EnLang
│   │   ├── canonicalizer.py            # Natural Indexing (x at i -> x[i]) & Slicing
│   │   ├── ambiguity_detector.py       # Domain Disambiguation (.enlg vs .enlgf vs .enlgdb)
│   │   └── pipeline.py                 # 5-Stage Intent Pipeline Orchestrator
│   │
│   ├── parser/                          # Deterministic Frontend Engine
│   │   ├── __init__.py
│   │   ├── lexer.py                    # Deterministic Tokenizer
│   │   ├── ast_nodes.py                # Universal AST Node Classes
│   │   └── parser.py                   # Recursive Descent AST Generator
│   │
│   ├── ir/                              # Intermediate Representation Layer
│   │   ├── __init__.py
│   │   ├── ir_nodes.py                 # Backend-Agnostic IR Instructions
│   │   └── ir_builder.py               # AST-to-IR Converter
│   │
│   ├── analyzer/                        # Semantic Analysis & Verification
│   │   ├── __init__.py
│   │   ├── symbol_table.py             # Scope Tree & Symbol Visibility
│   │   ├── type_checker.py             # Static/Dynamic Type Validation
│   │   └── semantic_analyzer.py        # Scope, Return, and Signature Checks
│   │
│   ├── optimizer/                       # IR Optimization Engine
│   │   ├── __init__.py
│   │   ├── constant_folder.py          # Compile-time Expression Evaluation
│   │   └── dead_code.py                # Unreachable Instruction Removal
│   │
│   ├── emitters/                        # Modular Backend Code Generators
│   │   ├── __init__.py
│   │   ├── base_emitter.py             # Abstract Target Emitter Interface
│   │   ├── python_emitter.py           # .enlg  -> Python 3 Code Emitter
│   │   ├── html_emitter.py             # .enlgf -> HTML5 Markup Emitter
│   │   ├── css_emitter.py              # .enlgd -> CSS3 Stylesheet Emitter
│   │   ├── js_emitter.py               # .enlgs -> ES6+ JavaScript Emitter
│   │   └── sql_emitter.py              # .enlgdb -> SQLite SQL Emitter
│   │
│   ├── chatbot/                         # Grounded AI Assistant Subsystem
│   │   ├── __init__.py
│   │   ├── brain.py                    # RAG & Reasoning Engine
│   │   └── prompt_builder.py           # Spec-Driven Prompt Generator
│   │
│   ├── __init__.py
│   ├── cli.py                           # Unified Terminal CLI (`enlang run/check/ai`)
│   ├── transpiler.py                    # Master Orchestrator (Legacy Bridge & Pipeline)
│   └── interpreter.py                 # Runtime Sandbox & Execution Engine
│
└── tests/                               # Comprehensive Categorized Test Suite
    ├── test_lexer.py                    # Tokenizer & Lexical Tests
    ├── test_parser.py                   # Syntax Tree Generation Tests
    ├── test_ast.py                      # AST Node Integrity Tests
    ├── test_ir.py                       # Intermediate Representation Tests
    ├── test_semantic.py                 # Scope & Type Checker Tests
    ├── test_optimizer.py                # Constant Folding & Optimization Tests
    ├── test_emitters.py                 # Multi-backend Output Validation
    ├── test_nlp_pipeline.py            # Synonym & Ambiguity Resolution Tests
    ├── test_regression.py               # 64+ Historical Bug & Feature Tests
    ├── test_golden.py                   # Golden File Output Comparison
    └── test_comprehensive.py            # Master End-to-End Test Suite
```

---

## 📜 4. CANONICAL SYNTAX & SEMANTIC RULES FREEZE

### 4.1 Canonical Syntax Constructs
* **Variable Assignment**: `set <var> to <expr>` | `set <var>[<idx>] to <expr>`
* **Console Output**: `display <expr>`
* **User Input**: `set <var> to ask <prompt>`
* **Function Definition**: `function <name> with <arg1> and <arg2>:` | `function <name>:`
* **Function Call**: `call <name> with <arg1> and <arg2>` | `call <name>`
* **Conditional Control**: `if <cond> then:` ... `else if <cond> then:` ... `else:`
* **Iterative Loops**: `for each <item> in <list>:` | `for each <var> from <start> to <end>:` | `repeat <n> times:` | `while <cond> do:`
* **Collections**: `create map` | `{}` | `[]`
* **Indexing & Slicing**: `<var>[<idx>]` | `<var>[<start>:<end>]`

### 4.2 Core Semantic Rules
1. **Variable Declaration & Scope**: Variables are implicitly declared upon first assignment in the local scope. Function scopes enclose variables; inner blocks inherit outer scope symbols.
2. **Type System**: Dynamic duck-typing with runtime validation. Primitives: `Number` (int/float), `String`, `Boolean`, `Null` (`None`). Compounds: `List`, `Map`.
3. **Function Semantics**: Functions must be defined or imported before invocation. Recursion is fully supported. Overloading by argument count is evaluated at AST resolution time.
4. **Evaluation Strategy**: Pass-by-object-reference (identical to Python). Primitives behave immutably; collections (`List`, `Map`) are mutated in place.

---

## 🚀 5. RELEASE MILESTONES & ROADMAP

### 🏁 Milestone 1: v2.0.0-alpha (Foundation & Architecture)
* ✅ Create formal `spec/` directory and freeze `enlang_spec.json`, `grammar.ebnf`, `keywords.json`, `operators.json`, `builtins.json`, and `stdlib.json`.
* ✅ Document comprehensive semantic rules and language references in `docs/`.
* ✅ Define universal AST nodes in `enlang_core/parser/ast_nodes.py` and implement the deterministic parser.
* ✅ Implement initial unit tests for Lexer, Parser, and AST.

### 🏁 Milestone 2: v2.0.0-beta (IR, Emitters & Semantic Analysis)
* ✅ Build Intermediate Representation (`ir/`) layer and basic IR optimizer.
* ✅ Build Semantic Analyzer (`analyzer/`) for scope and symbol validation.
* ✅ Implement modular target emitters in `emitters/` (`python`, `html`, `css`, `js`, `sql`).
* ✅ Integrate modular `nlp_engine/` preprocessing pipeline (Tokenizer ➔ Synonyms ➔ Rewriter ➔ Canonicalizer).
* ✅ Expand automated test suite across all 10 test categories (200+ tests).

### 🏁 Milestone 3: v2.0.0-stable (AI Grounding & Global Release)
* ✅ Ground `enlang ai` (`chatbot/`) to directly read `spec/` files for zero-hallucination canonical code generation.
* ✅ Verify 100% test pass rate across all domains (`.enlg`, `.enlgf`, `.enlgd`, `.enlgs`, `.enlgdb`).
* ✅ Publish official production release on PyPI (`enlang-2.0.0-py3-none-any.whl`) and VS Code Marketplace (`enlang-2.0.0.vsix`).

---
*END OF MASTER BLUEPRINT — ENLANG CORE ENGINEERING TEAM*
