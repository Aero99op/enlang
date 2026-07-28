# EnLang v2.0.0 Formal Grammar Reference
==============================================================================

Please refer to `spec/grammar.ebnf` for the complete EBNF specification.

## Key Canonical Rules
- Statements are newline or semicolon separated.
- Blocks are delimited by indentation or colons followed by indented lines.
- Natural English variations are canonicalized before parsing by `nlp_engine/`.
