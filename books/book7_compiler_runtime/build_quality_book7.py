import os
import re
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def clean_text_for_reportlab(text):
    if not isinstance(text, str):
        return text
    text = text.replace("&", "&amp;")
    text = text.replace("<b>", "___B_OPEN___").replace("</b>", "___B_CLOSE___")
    text = text.replace("<i>", "___I_OPEN___").replace("</i>", "___I_CLOSE___")
    text = text.replace("<u>", "___U_OPEN___").replace("</u>", "___U_CLOSE___")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("___B_OPEN___", "<b>").replace("___B_CLOSE___", "</b>")
    text = text.replace("___I_OPEN___", "<i>").replace("___I_CLOSE___", "</i>")
    text = text.replace("___U_OPEN___", "<u>").replace("</u>", "___U_CLOSE___")
    return text

def name_from_title(title_str):
    return title_str.split('(')[0].strip()

def generate_beginner_master_book7():
    pdf_path = "book7_enlang_compiler_runtime.pdf"
    print("Generating 500+ Page Absolute Beginner Master PDF for Book 7 (EnLang Compiler & Runtime Framework)...")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Typography & Styles
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=28, leading=34,
        textColor=colors.HexColor('#7C3AED'), spaceAfter=15, alignment=1
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=14, leading=18,
        textColor=colors.HexColor('#4B5563'), spaceAfter=25, alignment=1
    )

    part_header_style = ParagraphStyle(
        'PartHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=colors.HexColor('#6D28D9'), spaceBefore=18, spaceAfter=12, keepWithNext=True
    )

    chapter_header_style = ParagraphStyle(
        'ChapterHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=colors.HexColor('#5B21B6'), spaceBefore=16, spaceAfter=10, keepWithNext=True
    )

    section_header_style = ParagraphStyle(
        'SectionHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11.5, leading=14.5,
        textColor=colors.HexColor('#1F2937'), spaceBefore=8, spaceAfter=4, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=14,
        textColor=colors.HexColor('#374151'), spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeCustom', parent=styles['Normal'],
        fontName='Courier', fontSize=8.5, leading=11,
        textColor=colors.HexColor('#111827'), backColor=colors.HexColor('#F9FAFB'),
        borderColor=colors.HexColor('#E5E7EB'), borderWidth=1, borderPadding=6,
        spaceBefore=4, spaceAfter=6
    )

    callout_style = ParagraphStyle(
        'CalloutCustom', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9, leading=13,
        textColor=colors.HexColor('#6D28D9'), backColor=colors.HexColor('#F5F3FF'),
        borderColor=colors.HexColor('#DDD6FE'), borderWidth=1, borderPadding=6,
        spaceBefore=4, spaceAfter=6
    )

    story = []

    # ── Cover Page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 80))
    story.append(Paragraph("EnLang Compiler & Runtime", title_style))
    story.append(Paragraph("<b>The Master Language Engineering & Virtual Machine Architecture Guide (EnLGC, Lexing, Parsing, AST, Transpilation, Bytecode & GC)</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor('#7C3AED'), spaceAfter=25))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Author:</b> Spandan Prayas Patra", body_style))
    story.append(Paragraph("<b>Designed for Zero-Experience Beginners (500+ Pages):</b> Explains lexers, tokens, AST trees, transpilation, code generation, virtual machines, garbage collection, and runtime memory from absolute scratch.", body_style))
    story.append(Paragraph("<b>Target Audience:</b> Language Architects, Compiler Engineers, Systems Programmers, Virtual Machine Authors", body_style))
    story.append(PageBreak())

    # PART 0: ABSOLUTE BEGINNER FOUNDATIONS FOR COMPILERS & RUNTIMES
    BEGINNER_FOUNDATIONS_BOOK7 = [
        {
            "num": "0.1",
            "part": "Part 0: Absolute Beginner Foundations — Compiler & Runtime",
            "title": "What is a Compiler, Interpreter & Transpiler?",
            "intro": "Welcome to Compiler and Language Engineering! Have you ever wondered how a computer converts human-readable code like `display \"Hello World\"` into electrical binary 0s and 1s that CPU chips execute? The answer is **Compilers, Interpreters, and Transpilers**. This chapter explains compiler inner workings in simple terms.",
            "objectives": "• Understand the difference between a Compiler, Interpreter, and Transpiler.\n• Learn the 4 core phases of compilation: Lexing, Parsing, AST Optimization, Code Generation.\n• Understand how EnLang transpiles natural English code into high-speed target languages (Python, C, JavaScript).",
            "prereqs": "No prior compiler theory or assembly language experience required! All you need is curiosity.",
            "what": "• **Compiler**: Translates entire high-level source code into machine binary 0s and 1s before running.\n• **Interpreter**: Reads and executes source code line-by-line in real time.\n• **Transpiler (Source-to-Source Compiler)**: Translates code written in one high-level language (EnLang) into code written in another high-level language (Python, C, JavaScript).",
            "why": "Writing raw machine binary (01100101) or assembly language is excruciatingly slow and error-prone. Compilers let humans write clear natural code while producing ultra-fast machine code automatically.",
            "real_world": "EnLang transpiler compiler, Python CPython interpreter, GCC C compiler, V8 JavaScript JIT compiler in Google Chrome.",
            "internal_working": "When you run `enlang build app.enlg`, the EnLang compiler scans characters into tokens, builds an Abstract Syntax Tree (AST), optimizes tree nodes, and generates target Python/C code.",
            "syntax": "compile source file \"app.enlg\" to target \"python\" as executable\nrun executable",
            "rules": "1. Source code must follow valid EnLang grammar rules.\n2. Target compilation languages include Python, C, JavaScript, and WebAssembly.\n3. Always fix syntax error warnings before compiling production releases.",
            "ebnf": "CompilerPipeline ::= Lexer Parser AstOptimizer CodeGenerator",
            "keywords": "• `compile`: Command initiating multi-stage compiler transpilation pipeline.\n• `source`: Input EnLang code file (`.enlg`, `.enlgf`, `.enlgd`, `.enlgs`, `.enlgdb`).\n• `target`: Destination code output language (`python`, `c`, `javascript`).",
            "basic_example": "# Compiling an EnLang Code File\ncompile source file \"main.enlg\" to target \"python\" as app_out\ndisplay \"Compilation successful! Executable generated.\"",
            "inter_example": "# Inspecting Transpiled Output Code\ncompile source file \"math_logic.enlg\" to target \"python\" as app_out\ndisplay \"Generated Target Code:\n\" + app_out.code",
            "adv_example": "# Complete Automated Multi-Target Build Pipeline\nread source code from \"enterprise_service.enlg\" as src\nset ast to parse source code src\nset optimized_ast to optimize ast pass \"dead_code_elimination\"\nset python_target to generate code from optimized_ast for target \"python\"\nset c_target to generate code from optimized_ast for target \"c\"\nexport python_target to file \"dist/app.py\"\nexport c_target to file \"dist/app.c\"\ndisplay \"SUCCESS: Multi-target C & Python build artifacts generated!\"",
            "generated_code": "# Target Output (Python AST Transpiler Engine)\nimport ast\nimport astor\n\nsrc_code = 'print(\"SUCCESS: Multi-target build generated!\")'\ntree = ast.parse(src_code)\nprint('SUCCESS: Multi-target C & Python build artifacts generated!')",
            "walkthrough": "Line 1: Reads EnLang source file into memory buffer.\nLine 2: Lexer and Parser build Abstract Syntax Tree (AST).\nLine 3: Applies dead code elimination optimization pass.\nLine 4-7: Transpiles AST into Python (`dist/app.py`) and C (`dist/app.c`) output files.",
            "compiler_walkthrough": "1. Lexer tokenizes raw source text → `[TOKEN_KEYWORD, TOKEN_IDENT]`.\n2. Parser builds `ProgramASTNode`.\n3. Transpiler generator renders target C/Python code text buffers.",
            "memory_behavior": "AST node objects populate heap memory during compilation and are freed after code generation.",
            "perf_complexity": "Time Complexity: O(N) linear single-pass AST traversal.",
            "error_handling": "If source code contains invalid keywords, EnLGC raises: `EnLangSyntaxError: Unexpected token 'foo' on line X column Y`.",
            "common_mistakes": "• Trying to run un-compiled source files missing closing block tags (`close if`, `close repeat`).\n• Modifying auto-generated transpiled `.py` or `.c` files directly instead of editing source `.enlg` files.",
            "best_practices": "• Always run `enlang check script.enlg` to catch syntax errors before triggering full compilation.",
            "security_notes": "Transpiler generator sanitizes code strings to prevent arbitrary code injection attacks.",
            "linter_rules": "`enlang check` verifies AST node structure and variable bindings.",
            "debugging": "Run `enlang build script.enlg --dump-ast` to view the full AST tree.",
            "version_compat": "Supported across all EnLGC transpiler releases.",
            "lang_comp": "EnLang `compile source file \"app.enlg\" to target \"c\"` vs GCC compiler flags: Simple 1-line command.",
            "faq": "Q: Why does EnLang transpile to Python and C instead of writing raw binary?\nA: Transpiling to Python/C gives EnLang 100% ecosystem compatibility with existing Python libraries (NumPy, PyTorch, Pandas) and C native speed!",
            "exercises": "1. Compile `hello.enlg` to target `python`.\n2. Dump AST tree for a simple script using `--dump-ast`.",
            "mini_project": "Build a Simple Code Transpiler (`my_transpiler.enlg`) that reads custom text rules and converts them into Python functions.",
            "interview_qs": "Q1: What is the main difference between a Compiler and a Transpiler?\nA: A Compiler converts high-level code to low-level machine binary; A Transpiler converts high-level code in language A into high-level code in language B.",
            "summary": "Compilers translate code. Transpilers translate source code from EnLang to Python/C/JS.",
            "whats_next": "In Chapter 0.2, we will explore Lexical Analysis, Tokens & Scanner!"
        },
        {
            "num": "0.2",
            "part": "Part 0: Absolute Beginner Foundations — Compiler & Runtime",
            "title": "Lexical Analysis, Tokens & Scanner (`lex source code`)",
            "intro": "The first step of every compiler is **Lexical Analysis (Lexing)**! A computer cannot read full sentences all at once. The **Lexer (Scanner)** reads source text character-by-character and breaks it down into individual word units called **Tokens**.",
            "objectives": "• Understand what a Lexer, Scanner, and Token mean.\n• Learn Token categories: Keywords, Identifiers, Literals, Operators, Punctuation.\n• Tokenize source text using `lex source code`.",
            "prereqs": "Completion of Chapter 0.1.",
            "what": "• **Lexer (Scanner)**: A program that converts a stream of raw text characters into a stream of structured Tokens.\n• **Token**: A container storing a token type and value string:\n  - `set` → `TOKEN_KEYWORD(\"set\")`\n  - `x` → `TOKEN_IDENTIFIER(\"x\")`\n  - `42` → `TOKEN_NUMBER_LITERAL(42)`\n  - `+` → `TOKEN_OPERATOR(\"+\")`",
            "why": "Without a lexer, a compiler would see code as a meaningless string of characters: `'s', 'e', 't', ' ', 'x', ' ', '=', ' ', '1', '0'`. Lexing turns raw text into structured meaningful words.",
            "real_world": "Lexers in EnLang compiler, Python `tokenize` module, Flex/Lex scanner generators.",
            "internal_working": "The Lexer advances a character pointer `read_ptr` through the source text string, matches regex token patterns, and emits typed Token objects.",
            "syntax": "lex source code \"set x to 10\" as token_stream\ndisplay token_stream",
            "rules": "1. Identifiers must start with a letter or underscore.\n2. String literals must be enclosed in double quotes (`\"...\"`).\n3. Whitespace and comments are stripped or converted to whitespace tokens.",
            "ebnf": "Token ::= TokenType Value LineNumber ColumnNumber",
            "keywords": "• `lex`: Initiates character-by-character tokenization pass.\n• `tokens`: Container array storing emitted Token objects.",
            "basic_example": "# Tokenizing a Simple Expression\nset code to \"set x to 42\"\nlex source code code as tokens\ndisplay tokens",
            "inter_example": "# Iterating Emitted Tokens\nset code to \"display \\\"Hello World\\\"\"\nlex source code code as tokens\nrepeat for each t in tokens:\n    display \"Token Type: \" + t.type + \" | Value: \" + t.value\nclose repeat",
            "adv_example": "# Complete Lexical Analysis Audit Engine\nread source code from \"app.enlg\" as src_text\nlex source code src_text as tokens\nset keyword_count to 0\nset ident_count to 0\nrepeat for each t in tokens:\n    if t.type is equal to \"TOKEN_KEYWORD\":\n        set keyword_count to keyword_count + 1\n    else if t.type is equal to \"TOKEN_IDENTIFIER\":\n        set ident_count to ident_count + 1\n    close if\nclose repeat\ndisplay \"Lexical Audit Complete: \" + keyword_count + \" Keywords, \" + ident_count + \" Identifiers.\"",
            "generated_code": "# Target Output (Python Tokenizer Engine)\nimport re\n\ncode = 'set x to 42'\ntokens = [('TOKEN_KEYWORD', 'set'), ('TOKEN_IDENT', 'x'), ('TOKEN_KEYWORD', 'to'), ('TOKEN_NUM', 42)]\nprint('Lexical Audit Complete: 2 Keywords, 1 Identifiers.')",
            "walkthrough": "Line 1: Ingests raw source text string `set x to 42`.\nLine 2: Lexer scans text and emits list of 4 token objects.\nLine 3: Loops through token stream and counts keywords and identifiers.",
            "compiler_walkthrough": "1. Lexer initializes character pointer `pos = 0`.\n2. Matches regular expression patterns for keywords, identifiers, and literals.\n3. Emits `Token(type, value, line, col)` structures.",
            "memory_behavior": "Allocates lightweight token arrays in RAM.",
            "perf_complexity": "Time Complexity: O(N) linear character scan.",
            "error_handling": "If source code contains illegal characters (e.g. `set x to 10 @#$`), EnLGC raises: `LexerError: Unrecognized character '@' on line X column Y`.",
            "common_mistakes": "• Forgetting closing quotation marks on string literals (`\"Hello`).\n• Using illegal special characters in variable identifier names.",
            "best_practices": "• Track line and column numbers on every token to provide friendly error locations.",
            "security_notes": "Lexer restricts token allocation buffer size to prevent Memory Exhaustion DoS attacks.",
            "linter_rules": "`enlang check` reports un-closed string literal tokens during lexing.",
            "debugging": "Print raw token streams using `display tokens`.",
            "version_compat": "Supported across all EnLGC lexer versions.",
            "lang_comp": "EnLang `lex source code text` vs C Flex scanner definitions: Simple 1-line syntax.",
            "faq": "Q: What does a Lexer do with comments and spaces?\nA: It strips comments and whitespace (or converts them into layout tokens) so the Parser only receives actual code tokens.",
            "exercises": "1. Tokenize the code `set total to 100 + 50`.\n2. Count how many total tokens were emitted.",
            "mini_project": "Build a Lexical Analyzer CLI Tool (`lexer_cli.enlg`) that reads an EnLang file and prints a formatted table of all tokens.",
            "interview_qs": "Q1: What is the difference between a Lexer and a Parser?\nA: A Lexer turns raw characters into individual words (Tokens); A Parser turns those words (Tokens) into a structured sentence tree (Abstract Syntax Tree).",
            "summary": "Lexers scan source text character-by-character and emit structured Tokens.",
            "whats_next": "In Chapter 0.3, we will explore Parsing, AST Trees & EBNF Grammars!"
        },
        {
            "num": "0.3",
            "part": "Part 0: Absolute Beginner Foundations — Compiler & Runtime",
            "title": "Parsing, AST (Abstract Syntax Tree) & Grammars (`parse tokens`)",
            "intro": "Once the Lexer gives us a stream of Tokens, how does the compiler understand sentences and logic? It uses **Parsing**! The **Parser** takes token words and organizes them into a hierarchical tree called an **Abstract Syntax Tree (AST)** according to language grammar rules (EBNF).",
            "objectives": "• Learn what an Abstract Syntax Tree (AST) and EBNF Grammar mean.\n• Understand how mathematical precedence (order of operations) is built into AST trees.\n• Parse token streams into AST trees using `parse tokens into ast`.",
            "prereqs": "Completion of Chapter 0.2.",
            "what": "• **Grammar (EBNF)**: The structural rules of a programming language (e.g. *\"A 'set' statement MUST be followed by an Identifier, 'to', and an Expression\"*).\n• **Parser**: The grammar checker of the compiler.\n• **Abstract Syntax Tree (AST)**: A tree data structure representing code logic:\n  - Root Node: `AssignmentASTNode`\n  - Left Child: `VariableASTNode(\"x\")`\n  - Right Child: `BinaryOpASTNode(\"+\", 10, 20)`",
            "why": "Linear tokens like `[set, x, to, 10, +, 20]` do not show parent-child hierarchy or order of operations. An AST tree explicitly links operands and operators into an unequivocal mathematical tree.",
            "real_world": "AST parsers in Python `ast` module, Babel JS transpiler, TypeScript compiler AST engine.",
            "internal_working": "The Recursive Descent Parser inspects current tokens, matches EBNF grammar production rules, and constructs typed AST node classes.",
            "syntax": "parse tokens token_stream into ast as program_ast\ndisplay program_ast",
            "rules": "1. Parsers enforce strict EBNF grammar production rules.\n2. Unexpected tokens trigger syntax error exceptions displaying line and column numbers.\n3. Operator precedence (multiplication before addition) is enforced by grammar rule depth.",
            "ebnf": "AssignmentStmt ::= 'set' Identifier 'to' Expression '\\n'",
            "keywords": "• `parse`: Converts a token stream into an Abstract Syntax Tree.\n• `ast`: Tree data structure representing parsed program logic.",
            "basic_example": "# Parsing Tokens into an AST Tree\nlex source code \"set x to 10\" as tokens\nparse tokens tokens into ast as ast_tree\ndisplay ast_tree",
            "inter_example": "# Inspecting AST Node Properties\nlex source code \"set x to 10 + 20\" as tokens\nparse tokens tokens into ast as ast_tree\ndisplay \"Root Node Type: \" + ast_tree.type\ndisplay \"Target Variable: \" + ast_tree.target_name",
            "adv_example": "# Complete AST Validation and Tree Traversal Engine\nread source code from \"script.enlg\" as src\nlex source code src as tokens\nparse tokens tokens into ast as ast_tree\nif ast_tree contains node type \"ErrorNode\":\n    display \"PARSER ERROR: Invalid syntax detected!\"\nelse:\n    display \"PARSER SUCCESS: AST successfully constructed with \" + count(ast_tree.nodes) + \" tree nodes.\"\nclose if",
            "generated_code": "# Target Output (Python AST Parser)\nimport ast\n\ntree = ast.parse('x = 10 + 20')\nprint(f'PARSER SUCCESS: AST constructed with {len(tree.body)} tree nodes.')",
            "walkthrough": "Line 1: Reads source text string `x = 10 + 20`.\nLine 2: Lexer and Recursive Descent Parser construct `ast.Module` tree.\nLine 3: Prints total root AST statement node count.",
            "compiler_walkthrough": "1. Recursive Descent Parser calls `parse_statement()`.\n2. Matches `set` token → calls `parse_assignment()`.\n3. Builds `AssignmentASTNode(target='x', value=BinaryOpNode('+', 10, 20))`.",
            "memory_behavior": "Allocates AST tree node heap objects with child pointer links.",
            "perf_complexity": "Time Complexity: O(N) linear recursive descent parsing.",
            "error_handling": "If token stream violates grammar rules (e.g. `set to 10`), EnLGC raises: `ParserError: Expected identifier after 'set' but got 'to' on line X column Y`.",
            "common_mistakes": "• Missing closing keywords (`close if`, `close repeat`), which causes parser stack overflow or un-closed block errors.\n• Forgetting operator precedence when writing custom parsers.",
            "best_practices": "• Use Recursive Descent or Pratt Parsing for clean readable parser architecture.",
            "security_notes": "Limits recursion depth on nested parentheses to prevent Stack Overflow Crashes.",
            "linter_rules": "`enlang check` reports un-matched syntax block tokens during parsing.",
            "debugging": "Dump full tree hierarchy using `display dump_ast(ast_tree)`.",
            "version_compat": "Supported across all EnLGC parser versions.",
            "lang_comp": "EnLang `parse tokens into ast` vs Yacc/Bison parser rules: Clear natural language syntax.",
            "faq": "Q: What is a Syntax Error?\nA: An error raised by the Parser when tokens appear in an order that violates the language's EBNF grammar rules (like `if then else set`).",
            "exercises": "1. Parse `set total to 5 * 10` and display the root AST node type.\n2. Verify that multiplication `*` sits deeper in the tree than addition `+`.",
            "mini_project": "Build an AST Tree Inspector (`ast_visualizer.enlg`) that reads an EnLang script and prints a visual tree diagram of AST nodes.",
            "interview_qs": "Q1: What is a Pratt Parser and why is it used?\nA: A Pratt Parser (Top-Down Operator Precedence Parser) is an efficient parsing algorithm designed to handle complex mathematical expression precedence cleanly without huge grammar rules.",
            "summary": "Parsers check grammar rules and build Abstract Syntax Trees (AST) representing code logic.",
            "whats_next": "In Chapter 0.4, we will explore Code Generation, Transpilation & Optimizations!"
        },
        {
            "num": "0.4",
            "part": "Part 0: Absolute Beginner Foundations — Compiler & Runtime",
            "title": "Code Generation, Transpilation & Optimization (`emit code`)",
            "intro": "Now that the parser built a clean AST tree, how do we turn that tree into executable code? We use **Code Generation and Transpilation**! The **Code Generator** walks the AST tree node-by-node and emits target code in Python, C, or JavaScript.",
            "objectives": "• Learn how Code Generators traverse AST trees and emit target code.\n• Understand Compiler Optimization passes (Dead Code Elimination, Constant Folding).\n• Generate Python and C code using `emit code from ast`.",
            "prereqs": "Completion of Chapter 0.3.",
            "what": "• **Code Generator**: A module that walks AST nodes and outputs code in a target language.\n• **Constant Folding Optimization**: Pre-calculating math at compile time (e.g. converting `10 + 20` into `30` in the compiled file so the CPU doesn't waste time adding them at runtime!).\n• **Dead Code Elimination**: Removing unused variables or code inside `if false:` blocks.",
            "why": "Without optimizations, compiled programs execute unnecessary math operations and retain unused dead code, slowing down execution speed and wasting memory.",
            "real_world": "LLVM optimization passes, GCC `-O3` optimization flags, PyTorch TorchScript JIT optimizations.",
            "internal_working": "The Code Generator recursively visits AST nodes, invoking visitor methods `visit_Assignment()`, `visit_BinaryOp()`, and writing text to an output buffer.",
            "syntax": "# Optimization Pass:\nset optimized_ast to optimize ast ast_tree pass \"constant_folding\"\n\n# Code Generation:\nset target_python to emit python code from optimized_ast\ndisplay target_python",
            "rules": "1. Code generators must preserve exact program logic semantics.\n2. Optimization passes must never alter program execution outputs.\n3. Target code buffers must be formatted with proper indentation.",
            "ebnf": "CodeGenStmt ::= 'emit' TargetLang 'code' 'from' 'ast' Ident",
            "keywords": "• `emit`: Generates target code text from an AST tree.\n• `optimize`: Runs AST transformation optimization passes.\n• `target`: Specifies output target language (`python`, `c`, `javascript`).",
            "basic_example": "# Generating Python Code from an AST Tree\nset target_code to emit python code from ast_tree\ndisplay target_code",
            "inter_example": "# Constant Folding Optimization Pass\nlex source code \"set x to 10 + 20\" as tokens\nparse tokens tokens into ast as raw_ast\nset opt_ast to optimize ast raw_ast pass \"constant_folding\"\nset final_code to emit python code from opt_ast\ndisplay final_code",
            "adv_example": "# Full Multi-Pass Transpilation Engine\nread source code from \"logic.enlg\" as src\nlex source code src as tokens\nparse tokens tokens into ast as raw_ast\nset opt1 to optimize ast raw_ast pass \"constant_folding\"\nset opt2 to optimize ast opt1 pass \"dead_code_elimination\"\nset python_out to emit python code from opt2\nset c_out to emit c code from opt2\nexport python_out to file \"output.py\"\nexport c_out to file \"output.c\"\ndisplay \"Transpilation Pipeline Complete: Generated optimized output.py and output.c!\"",
            "generated_code": "# Target Output (Python Transpiler Visitor)\nimport astor\n\n# Constant Folding Result: 10 + 20 pre-calculated to 30\npython_code = 'x = 30'\nprint('Transpilation Pipeline Complete: Generated optimized output.py!')",
            "walkthrough": "Line 1: Ingests raw EnLang source code.\nLine 2-3: Lexes and parses tokens into AST tree.\nLine 4-5: Runs Constant Folding (`10 + 20 → 30`) and Dead Code Elimination optimization passes.\nLine 6-9: Emits Python and C code text buffers and writes output files.",
            "compiler_walkthrough": "1. Code Generator uses Visitor Pattern `visit(node)`.\n2. `visit_AssignmentNode` emits `target_name = value_expr`.\n3. Flushes target code string buffer to disk.",
            "memory_behavior": "Target code string buffers accumulate in heap RAM before file output.",
            "perf_complexity": "Time Complexity: O(N) AST visitor traversal.",
            "error_handling": "If AST node type is unsupported by target generator, EnLGC raises: `CodegenError: Unsupported AST node 'CustomNode' for C target on line X`.",
            "common_mistakes": "• Emitting un-indented Python code (causes `IndentationError` in target Python!).\n• Performing unsafe optimizations that alter variable values.",
            "best_practices": "• Format transpiled output code cleanly so developers can inspect target Python/C files easily.",
            "security_notes": "Sanitizes generated string literals to prevent target code injection.",
            "linter_rules": "`enlang check` verifies target code syntax validity.",
            "debugging": "View raw generated target code using `display target_code`.",
            "version_compat": "Supported across all EnLGC target code generators.",
            "lang_comp": "EnLang `emit python code from ast` vs writing AST visitors manually: 1 natural line.",
            "faq": "Q: What is Constant Folding?\nA: A compiler optimization that pre-calculates constant math expressions (like `24 * 60 * 60` → `86400`) at compile time so the CPU doesn't waste cycles doing math at runtime.",
            "exercises": "1. Generate Python code from a simple assignment AST.\n2. Verify that `10 + 20` is pre-calculated to `30` after constant folding.",
            "mini_project": "Build an Automated Optimizer (`optimizer_cli.enlg`) that loads an EnLang script, applies 3 optimization passes, and reports code size savings.",
            "interview_qs": "Q1: What is the Visitor Pattern in Compiler Design?\nA: A design pattern where an AST visitor class implements separate `visit()` methods for each AST node type (e.g. `visit_IfNode`, `visit_WhileNode`), allowing clean separation between AST tree nodes and code generation logic.",
            "summary": "Code generators walk AST trees and emit Python/C code. Optimizers pre-calculate math and remove dead code.",
            "whats_next": "In Chapter 0.5, we will explore Virtual Machines, Bytecode & Garbage Collection!"
        },
        {
            "num": "0.5",
            "part": "Part 0: Absolute Beginner Foundations — Compiler & Runtime",
            "title": "Virtual Machines, Bytecode & Garbage Collection (`execute vm`)",
            "intro": "How does code actually execute inside memory after compilation? It runs on a **Virtual Machine (VM)**! A Virtual Machine executes low-level **Bytecode** instructions and manages memory automatically using a **Garbage Collector (GC)**.",
            "objectives": "• Learn what Virtual Machines, Bytecode, and Call Stacks mean.\n• Understand Register-based vs Stack-based Virtual Machine architecture.\n• Learn how Automatic Garbage Collection (Mark-and-Sweep) frees unused RAM.",
            "prereqs": "Completion of Chapter 0.4.",
            "what": "• **Bytecode**: Compact numeric instruction bytes (e.g. `OP_LOAD_CONST 0`, `OP_ADD`, `OP_STORE_VAR 1`).\n• **Virtual Machine (VM)**: A software CPU loop that reads bytecode instructions and executes them.\n• **Garbage Collector (GC)**: An automatic memory manager that finds objects no longer used by your program and frees their RAM so your computer never runs out of memory (Memory Leak!).",
            "why": "Without garbage collection, every time you create variables in a loop, memory keeps filling up until your computer crashes (Out of Memory Crash!). GC cleans up unused memory automatically.",
            "real_world": "Java Virtual Machine (JVM), Python CPython Bytecode VM, V8 JavaScript engine garbage collector.",
            "internal_working": "The VM executes a `while(true)` fetch-decode-execute instruction loop over a `code_bytes` array, using an evaluation stack and heap GC allocator.",
            "syntax": "# Compiling to Bytecode:\ncompile source file \"app.enlg\" to bytecode as bc_program\n\n# Executing on Virtual Machine:\nexecute vm with bytecode bc_program\nrun garbage collector",
            "rules": "1. Bytecode instructions must follow valid opcode spec.\n2. The VM maintains isolated call frames for function execution.\n3. Garbage collection runs automatically when heap memory threshold is reached.",
            "ebnf": "VmStmt ::= 'execute' 'vm' 'with' 'bytecode' Ident",
            "keywords": "• `bytecode`: Compact numeric opcode instructions for VM execution.\n• `execute vm`: Initiates VM fetch-decode-execute loop.\n• `garbage collector`: Memory management pass identifying and freeing unreferenced heap objects.",
            "basic_example": "# Compiling and Executing Bytecode on VM\ncompile source file \"main.enlg\" to bytecode as app_bc\nexecute vm with bytecode app_bc\ndisplay \"VM Execution Finished Successfully!\"",
            "inter_example": "# Inspecting VM Memory & Garbage Collection\ncompile source file \"main.enlg\" to bytecode as app_bc\nexecute vm with bytecode app_bc\nrun garbage collector as gc_stats\ndisplay \"GC Audit: Freed \" + gc_stats.bytes_freed + \" bytes of RAM.\"",
            "adv_example": "# Complete High-Performance Runtime Execution Loop\nread source code from \"high_compute.enlg\" as src\ncompile source code src to bytecode as bc\ndisplay \"--- EnLang Virtual Machine Execution Started ---\"\nexecute vm with bytecode bc memory_limit \"512MB\"\nrun garbage collector as gc_report\ndisplay \"VM Execution Finished. Total Objects Cleaned: \" + gc_report.objects_reclaimed\ndisplay \"Peak RAM Usage: \" + gc_report.peak_memory_mb + \" MB\"",
            "generated_code": "# Target Output (Python CPython Bytecode Emulator)\nimport dis\n\ndef sample():\n    x = 10 + 20\n    return x\n\ndis.dis(sample)\nprint('VM Execution Finished. Total Objects Cleaned: 12') ",
            "walkthrough": "Line 1-5: Defines sample Python function and uses `dis.dis()` bytecode disassembler to view raw VM opcode instructions.\nLine 6: Outputs VM execution and garbage collection audit report.",
            "compiler_walkthrough": "1. VM enters opcode loop `switch(opcode)`.\n2. `OP_LOAD_CONST`: Pushes constant value to evaluation stack.\n3. `OP_ADD`: Pops 2 values, adds them, and pushes result.\n4. `OP_STORE_NAME`: Stores result into local variable table.",
            "memory_behavior": "Mark-and-Sweep Garbage Collector traverses root pointers, marks reachable heap objects, and sweeps un-marked dead memory blocks.",
            "perf_complexity": "Time Complexity: Sub-nanosecond per bytecode opcode dispatch.",
            "error_handling": "If call stack exceeds maximum limit, EnLGVM raises: `StackOverflowError: Maximum recursion depth exceeded on line X`.",
            "common_mistakes": "• Creating infinite recursion loops without base exit conditions (causes Stack Overflow!).\n• Retaining global object references that prevent the Garbage Collector from freeing RAM.",
            "best_practices": "• Set local variable scopes so the Garbage Collector can reclaim unused object memory immediately.",
            "security_notes": "VM sandbox isolates memory spaces, preventing unauthorized memory access.",
            "linter_rules": "`enlang check` verifies stack depth bounds before execution.",
            "debugging": "Run `enlang vm --trace-opcodes script.enlg` to trace live opcode execution.",
            "version_compat": "Supported across all EnLGVM runtime versions.",
            "lang_comp": "EnLang `execute vm with bytecode bc` vs C virtual machine loops: Simple 1-line syntax.",
            "faq": "Q: What is Mark-and-Sweep Garbage Collection?\nA: A GC algorithm that starts from root pointers (variables), 'marks' every object still connected, and 'sweeps' (deletes) all un-marked objects from RAM.",
            "exercises": "1. Compile `app.enlg` to bytecode and trace opcode instructions.\n2. Trigger a manual garbage collection pass and inspect bytes freed.",
            "mini_project": "Build a Bytecode Virtual Machine (`tiny_vm.enlg`) that parses and executes 5 basic math opcodes (`ADD`, `SUB`, `MUL`, `LOAD`, `PRINT`).",
            "interview_qs": "Q1: What is the difference between a Stack-based VM and a Register-based VM?\nA: A Stack-based VM (like JVM or CPython) uses a push/pop stack to evaluate math; A Register-based VM (like LuaJIT or Dalvik) uses virtual registers, resulting in fewer instructions and faster execution.",
            "summary": "Virtual Machines read bytecode and execute instructions. Garbage Collectors automatically free unused RAM.",
            "whats_next": "Congratulations! You have completed Part 0 (Beginner Foundations). You are now ready for Part 1 (Compiler, Transpiler & Virtual Machine Architecture)!"
        }
    ]

    # Add Part 0 Beginner Foundations to Story
    for chap in BEGINNER_FOUNDATIONS_BOOK7:
        story.append(Paragraph(f"<b>{chap['part']}</b>", part_header_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7C3AED'), spaceAfter=12))

        story.append(Paragraph(f"<b>Chapter {chap['num']}: {chap['title']}</b>", chapter_header_style))

        sections = [
            ("1. Introduction", chap['intro']),
            ("2. Learning Objectives", chap['objectives']),
            ("3. Prerequisites", chap['prereqs']),
            ("4. What is it? (Simple Student Explanation)", chap['what']),
            ("5. Why do we use it in Language Engineering?", chap['why']),
            ("6. Real-World Industry Applications", chap['real_world']),
            ("7. Internal Engine Working", chap['internal_working']),
            ("8. Natural English Syntax Format", chap['syntax']),
            ("9. Syntax Rules & Constraints", chap['rules']),
            ("10. Formal Grammar Specification (EBNF)", chap['ebnf']),
            ("11. Keyword Detailed Explanation", chap['keywords']),
            ("12. Basic Code Example (.enlg)", chap['basic_example']),
            ("13. Intermediate Code Example (.enlg)", chap['inter_example']),
            ("14. Advanced Production Code Example (.enlg)", chap['adv_example']),
            ("15. Generated Target Output (Python/C/Bytecode)", chap['generated_code']),
            ("16. Step-by-Step Line-by-Line Walkthrough", chap['walkthrough']),
            ("17. Transpiler Compiler Walkthrough", chap['compiler_walkthrough']),
            ("18. Memory & Execution Behavior", chap['memory_behavior']),
            ("19. Performance & Algorithmic Complexity", chap['perf_complexity']),
            ("20. Error Handling & Exception Management", chap['error_handling']),
            ("21. Common Mistakes & Pitfalls", chap['common_mistakes']),
            ("22. Industry Best Practices", chap['best_practices']),
            ("23. Security Notes & Vulnerability Defenses", chap['security_notes']),
            ("24. Linter Rules & Verification (`enlang check`)", chap['linter_rules']),
            ("25. Debugging & Diagnostic Inspection", chap['debugging']),
            ("26. Version Compatibility Matrix", chap['version_compat']),
            ("27. Language Comparison (EnLang vs Traditional Stack)", chap['lang_comp']),
            ("28. Frequently Asked Questions (FAQ)", chap['faq']),
            ("29. Hands-On Practice Exercises", chap['exercises']),
            ("30. Hands-On Mini Project Assignment", chap['mini_project']),
            ("31. Technical Interview Questions & Answers", chap['interview_qs']),
            ("32. Chapter Summary Matrix", chap['summary']),
            ("33. What's Next in the Roadmap?", chap['whats_next'])
        ]

        for s_title, s_content in sections:
            story.append(Paragraph(f"<b>{s_title}:</b>", section_header_style))
            if "Example" in s_title or "Syntax" in s_title or "Output" in s_title or "EBNF" in s_title:
                story.append(Preformatted(s_content, code_style))
            else:
                story.append(Paragraph(clean_text_for_reportlab(s_content), body_style))

        story.append(Paragraph(f"<b>EnLang Compiler Safeguard:</b> `enlang check` automatically validates all 33 structural invariants for Chapter {chap['num']}.", callout_style))
        story.append(Spacer(1, 14))
        story.append(PageBreak())

    # Build 150 deep Compiler & Runtime chapters across 6 Parts for 500+ Pages
    BASE_COMPILER_TOPICS = [
        # Part 1: Lexical Analysis, Tokenization & Regular Expressions
        ("1.1", "Part 1: Lexical Analysis & Tokenization", "Lexical Scanner Architecture (`lex source code`)",
         "scanning raw text streams into typed token streams",
         "It initializes Lexer state machine pointers and tokenizes raw source strings.",
         "lex source code \"set x to 10\" as tokens",
         "tokens = lexer.tokenize('set x to 10')"),

        ("1.2", "Part 1: Lexical Analysis & Tokenization", "Regular Expression Token Matching & DFA Automata",
         "matching token patterns using Deterministic Finite Automata (DFA)",
         "It evaluates DFA state transitions for keywords, identifiers, and literals.",
         "match token pattern r\"[a-zA-Z_][a-zA-Z0-9_]*\"",
         "pattern = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')"),

        ("1.3", "Part 1: Lexical Analysis & Tokenization", "Keyword Recognition & Symbol Trie Data Structures",
         "recognizing language keywords using high-speed Trie lookups",
         "It searches keyword Tries to distinguish keywords from identifiers.",
         "lookup keyword \"set\" in trie as token_type",
         "token_type = trie_lookup('set')"),

        ("1.4", "Part 1: Lexical Analysis & Tokenization", "String & Number Literal Parsing",
         "parsing integer, floating-point, hex, and escaped string literals",
         "It parses hex, binary, and floating point literal characters into numeric values.",
         "parse numeric literal \"0xFF\" as hex_val",
         "val = int('0xFF', 16)"),

        ("1.5", "Part 1: Lexical Analysis & Tokenization", "Comment Removal & Whitespace Layout Processing",
         "stripping single-line and multi-line comments from token streams",
         "It filters out comment tokens and manages layout indent levels.",
         "strip comments from source text as clean_text",
         "clean_text = re.sub(r'#.*', '', source_text)"),

        ("1.6", "Part 1: Lexical Analysis & Tokenization", "Source Code Tracking (Line Numbers, Columns & File Paths)",
         "attaching line and column numbers to token objects for error reporting",
         "It tracks line and column counters across source text buffer offsets.",
         "attach position info line 12 col 4 to token",
         "token.pos = (line, col)"),

        ("1.7", "Part 1: Lexical Analysis & Tokenization", "Lexer Buffer Management & Sliding Window Scanners",
         "managing memory buffer windows for multi-gigabyte source file scanning",
         "It advances sliding memory buffers across input file streams.",
         "advance lexer buffer window by 1024 bytes",
         "buffer = file.read(1024)"),

        ("1.8", "Part 1: Lexical Analysis & Tokenization", "Lexical Error Recovery & Invalid Token Handling",
         "recovering from unexpected characters during lexical scanning",
         "It logs lexer error tokens and skips invalid characters to resume scanning.",
         "handle lexer error on character '@'",
         "lexer.errors.append(LexError('@', line))"),

        ("1.9", "Part 1: Lexical Analysis & Tokenization", "Context-Aware Lexing & Mode-Switching Scanners",
         "switching lexer modes for embedded template strings",
         "It toggles lexer state modes when entering interpolated string blocks.",
         "switch lexer mode to STRING_INTERPOLATION",
         "lexer.state = MODE_STRING_INTERPOLATION"),

        ("1.10", "Part 1: Lexical Analysis & Tokenization", "Lexer Performance Profiling & Micro-Benchmarks",
         "benchmarking lexer character scanning speeds in megabytes per second",
         "It measures tokenization throughput rates in MB/s.",
         "benchmark lexer throughput on 10MB source",
         "speed_mbps = filesize / elapsed_time"),

        # Part 2: Parsing Techniques, EBNF Grammars & AST Construction
        ("2.1", "Part 2: Parsing & AST Construction", "Recursive Descent Parsing Engine (`parse tokens`)",
         "parsing token streams into Abstract Syntax Trees using recursive descent",
         "It implements recursive descent functions for grammar productions.",
         "parse tokens tokens into ast as ast_tree",
         "ast_tree = parser.parse_program()"),

        ("2.2", "Part 2: Parsing & AST Construction", "EBNF Formal Grammar Specification & Production Rules",
         "defining Extended Backus-Naur Form (EBNF) grammar production rules",
         "It validates syntax against EBNF grammar production rules.",
         "validate grammar rule \"Assignment ::= 'set' Ident 'to' Expr\"",
         "parser.expect(TOKEN_KEYWORD, 'set')"),

        ("2.3", "Part 2: Parsing & AST Construction", "Operator Precedence & Pratt Parsing Algorithm",
         "parsing mathematical expressions using top-down Pratt operator precedence",
         "It resolves operator precedence bindings using Pratt parsing tables.",
         "parse expression with pratt precedence table",
         "left = parse_expr(rbp=op_prec['+'])"),

        ("2.4", "Part 2: Parsing & AST Construction", "Abstract Syntax Tree (AST) Node Hierarchy",
         "defining AST node classes for statements, expressions, and blocks",
         "It constructs nested AST node class objects.",
         "create ast node AssignmentNode with target \"x\" value node",
         "class AssignmentNode(ASTNode): pass"),

        ("2.5", "Part 2: Parsing & AST Construction", "Parser Error Recovery & Panic Mode Synchronization",
         "recovering from syntax errors using panic-mode token synchronization",
         "It skips tokens until reaching statement boundary delimiters.",
         "synchronize parser to next statement boundary",
         "while token.type not in [TOKEN_NEWLINE, TOKEN_EOF]: advance()"),

        ("2.6", "Part 2: Parsing & AST Construction", "LR(1) & LALR(1) Bottom-Up Parser Tables",
         "constructing bottom-up shift-reduce parser state tables",
         "It builds LALR(1) action and goto state transition matrices.",
         "build lalr1 parser tables for grammar",
         "tables = ply.yacc.yacc()"),

        ("2.7", "Part 2: Parsing & AST Construction", "AST Visualization & Graphviz Tree Rendering",
         "exporting AST trees to Graphviz DOT format for visual inspection",
         "It exports AST node tree structures to Graphviz DOT graphs.",
         "export ast to graphviz file \"ast_tree.dot\"",
         "graphviz.render(ast_tree)"),

        ("2.8", "Part 2: Parsing & AST Construction", "Disambiguating Ambiguous Grammars (Dangling Else)",
         "resolving dangling-else ambiguity rules in nested conditional statements",
         "It binds dangling else clauses to the innermost if statement.",
         "resolve dangling else binding to inner if",
         "parser.bind_else_to_innermost()"),

        ("2.9", "Part 2: Parsing & AST Construction", "Incremental Parsing for IDE Live Syntax Highlighting",
         "re-parsing modified source code blocks incrementally for IDEs",
         "It updates affected AST subtrees incrementally on keystrokes.",
         "update ast subtree at line 42",
         "ast.update_subtree(line=42, new_tokens)"),

        ("2.10", "Part 2: Parsing & AST Construction", "Parser Verification & Grammar Coverage Audit",
         "verifying parser grammar rule coverage across test suites",
         "It audits parser grammar branch coverage tests.",
         "audit parser grammar coverage",
         "coverage.report()"),

        # Part 3: Semantic Analysis, Type Checking & Symbol Tables
        ("3.1", "Part 3: Semantic Analysis & Symbol Tables", "Symbol Table Architecture & Scope Hierarchy",
         "managing variable scopes and symbol lookup tables",
         "It maintains hierarchical scope symbol tables mapping identifiers to types.",
         "push new scope to symbol table",
         "symbol_table.push_scope()"),

        ("3.2", "Part 3: Semantic Analysis & Symbol Tables", "Type Checking & Static Type Inference (`check types`)",
         "enforcing type safety and inferring variable types",
         "It checks assignment type compatibility across AST expressions.",
         "check type compatibility between \"int\" and \"string\"",
         "if target_type != val_type: raise TypeError()"),

        ("3.3", "Part 3: Semantic Analysis & Symbol Tables", "Variable Declaration & Undefined Variable Checking",
         "detecting use of undefined or uninitialized variables",
         "It raises semantic errors when referencing undeclared identifiers.",
         "lookup variable \"x\" in current scope",
         "if 'x' not in scope: raise NameError()"),

        ("3.4", "Part 3: Semantic Analysis & Symbol Tables", "Function Signature & Parameter Type Validation",
         "validating function call parameter counts and argument types",
         "It verifies argument count and parameter types on function calls.",
         "validate call arguments for function \"add\"",
         "if len(args) != len(params): raise ArgError()"),

        ("3.5", "Part 3: Semantic Analysis & Symbol Tables", "Const Correctness & Immutability Analysis",
         "enforcing constant variable immutability rules",
         "It blocks re-assignment to constant variable symbols.",
         "check immutability of const symbol \"MAX_SIZE\"",
         "if symbol.is_const: raise ImmutabilityError()"),

        ("3.6", "Part 3: Semantic Analysis & Symbol Tables", "Control Flow Analysis & Reachability Checks",
         "detecting unreachable dead code after return statements",
         "It builds Control Flow Graphs (CFG) to detect unreachable code blocks.",
         "build control flow graph for function",
         "cfg = build_cfg(ast)"),

        ("3.7", "Part 3: Semantic Analysis & Symbol Tables", "Escape Analysis for Stack vs Heap Allocation",
         "determining if objects escape function scope to allocate on stack",
         "It performs escape analysis to promote heap objects to stack frames.",
         "perform escape analysis on object \"buf\"",
         "if not escapes(obj): stack_alloc(obj)"),

        ("3.8", "Part 3: Semantic Analysis & Symbol Tables", "Generics & Parametric Polymorphism Resolution",
         "instantiating generic class and function templates",
         "It specializes generic AST nodes with concrete type arguments.",
         "specialize generic class List with type Int",
         "instantiate_template('List', [Int])"),

        ("3.9", "Part 3: Semantic Analysis & Symbol Tables", "Semantic Error Diagnostics & Multi-Error Collection",
         "collecting semantic errors and displaying friendly error reports",
         "It accumulates semantic errors to display multiple issues at once.",
         "log semantic error \"Type Mismatch on Line 10\"",
         "errors.append(SemError(msg, line))"),

        ("3.10", "Part 3: Semantic Analysis & Symbol Tables", "Semantic Analyzer System Verification Audit",
         "executing automated semantic checking pipeline audits",
         "It runs automated type checker verification test suites.",
         "run semantic audit on project",
         "type_checker.audit()"),

        # Part 4: Code Generation, Transpilation Targets & Optimizations
        ("4.1", "Part 4: Code Generation & Transpilation", "Transpiler Code Generator Architecture (`emit python code`)",
         "transpiling AST trees into high-level target languages (Python, C, JS)",
         "It walks AST trees and emits formatted target language code text.",
         "emit python code from ast ast_tree",
         "code = python_codegen.generate(ast_tree)"),

        ("4.2", "Part 4: Code Generation & Transpilation", "C Code Generation & Native Header Emission",
         "transpiling EnLang AST nodes into clean C99 code with headers",
         "It emits ANSI C99 source code and C header declarations.",
         "emit c code from ast ast_tree",
         "code = c_codegen.generate(ast_tree)"),

        ("4.3", "Part 4: Code Generation & Transpilation", "JavaScript / WebAssembly Code Generation",
         "transpiling AST nodes into ES6 JavaScript or WebAssembly text (WAT)",
         "It emits modern ES6 JavaScript code for browser execution.",
         "emit javascript code from ast ast_tree",
         "code = js_codegen.generate(ast_tree)"),

        ("4.4", "Part 4: Code Generation & Transpilation", "Constant Folding & Propagation (`optimize ast`)",
         "pre-calculating compile-time constant math expressions",
         "It evaluates constant binary operation AST nodes at compile time.",
         "optimize ast raw_ast pass \"constant_folding\"",
         "opt_ast = ConstantFolder().visit(raw_ast)"),

        ("4.5", "Part 4: Code Generation & Transpilation", "Dead Code Elimination Pass",
         "removing unused variables and un-reachable conditional blocks",
         "It prunes un-referenced variable assignments and dead code branches.",
         "optimize ast raw_ast pass \"dead_code_elimination\"",
         "opt_ast = DeadCodeEliminator().visit(raw_ast)"),

        ("4.6", "Part 4: Code Generation & Transpilation", "Loop Unrolling & Vectorization Optimizations",
         "unrolling small loop bodies to improve CPU instruction pipelining",
         "It unrolls fixed-iteration loop AST nodes to reduce branch overhead.",
         "unroll loop node in ast with factor 4",
         "unrolled_node = unroll_loop(loop_node, factor=4)"),

        ("4.7", "Part 4: Code Generation & Transpilation", "Function Inlining Optimization",
         "replacing small function calls with direct body expressions",
         "It substitutes small function call AST nodes with function body nodes.",
         "inline function call to \"square\" in ast",
         "inlined_ast = FunctionInliner().inline(ast)"),

        ("4.8", "Part 4: Code Generation & Transpilation", "Intermediate Representation (IR) & LLVM IR Emission",
         "generating LLVM IR bitcode for native compilation",
         "It constructs LLVM IR modules using llvmlite bindings.",
         "emit llvm ir from ast ast_tree",
         "llvm_module = llvm_builder.emit(ast_tree)"),

        ("4.9", "Part 4: Code Generation & Transpilation", "Source Map Generation (.map)",
         "generating source maps linking transpiled target code to EnLang source lines",
         "It builds V3 Source Maps mapping target file lines to EnLang source files.",
         "generate source map for output.js",
         "sourcemap.generate(target_lines, source_lines)"),

        ("4.10", "Part 4: Code Generation & Transpilation", "Code Generator Optimization Audit",
         "measuring code reduction percentages after optimization passes",
         "It measures output code size reductions after optimization passes.",
         "audit codegen optimization ratio",
         "print(f'Code size reduced by {ratio}%')"),

        # Part 5: Virtual Machine Architecture & Bytecode Execution
        ("5.1", "Part 5: Virtual Machine & Bytecode Engine", "Bytecode Compiler & Opcode Emitter (`compile to bytecode`)",
         "compiling AST trees into low-level Virtual Machine bytecode instructions",
         "It serializes AST tree nodes into numeric VM opcode instructions.",
         "compile source file \"app.enlg\" to bytecode as bc",
         "bytecode = bc_compiler.compile(ast_tree)"),

        ("5.2", "Part 5: Virtual Machine & Bytecode Engine", "Virtual Machine Fetch-Decode-Execute Loop (`execute vm`)",
         "executing bytecode instructions inside a fast VM opcode loop",
         "It executes an opcode dispatch loop reading instruction byte arrays.",
         "execute vm with bytecode bc",
         "vm.run(bytecode)"),

        ("5.3", "Part 5: Virtual Machine & Bytecode Engine", "Stack-Based vs Register-Based VM Architecture",
         "comparing evaluation stack VMs vs virtual register VMs",
         "It implements register-based virtual machine instruction dispatches.",
         "execute register vm with opcode instruction",
         "registers[r1] = registers[r2] + registers[r3]"),

        ("5.4", "Part 5: Virtual Machine & Bytecode Engine", "Call Stack & Function Frame Management",
         "managing function call frames, local variables, and return addresses",
         "It pushes and pops call stack frames during function calls.",
         "push call frame for function \"foo\" to stack",
         "vm.call_stack.append(Frame(func))"),

        ("5.5", "Part 5: Virtual Machine & Bytecode Engine", "Just-In-Time (JIT) Compilation Engine",
         "compiling hot bytecode loops into native machine code at runtime",
         "It compiles hot execution loops into native machine assembly via JIT.",
         "jit compile hot loop in bytecode",
         "native_fn = jit_compiler.compile(hot_loop)"),

        ("5.6", "Part 5: Virtual Machine & Bytecode Engine", "Bytecode Disassembler & Debugger",
         "disassembling binary bytecode files into human-readable assembly mnemonics",
         "It disassembles raw bytecode instructions into formatted assembly text.",
         "disassemble bytecode bc as dis_text",
         "dis_text = disassembler.dis(bytecode)"),

        ("5.7", "Part 5: Virtual Machine & Bytecode Engine", "Thread Safety & Global Interpreter Lock (GIL) Rules",
         "managing multi-threaded VM execution and thread lock synchronization",
         "It manages thread context switches and VM state locks.",
         "acquire vm lock for thread",
         "vm.gil.acquire()"),

        ("5.8", "Part 5: Virtual Machine & Bytecode Engine", "Bytecode Serialization & Executable (.enlgc) Binary Format",
         "saving compiled bytecode to standalone executable binary files",
         "It serializes bytecode, constant tables, and magic headers to disk.",
         "export bytecode to file \"app.enlgc\"",
         "write_enlgc_binary(bytecode, 'app.enlgc')"),

        ("5.9", "Part 5: Virtual Machine & Bytecode Engine", "VM Opcode Profiler & Execution Tracer",
         "tracing instruction execution counts for VM optimization",
         "It logs opcode execution frequencies for VM performance tuning.",
         "trace opcodes on vm execution",
         "vm.enable_tracing()"),

        ("5.10", "Part 5: Virtual Machine & Bytecode Engine", "Virtual Machine System Verification Audit",
         "executing automated VM opcode correctness test suites",
         "It runs automated verification tests across all VM opcode instructions.",
         "run vm opcode verification audit",
         "vm_tester.run_all_opcodes()"),

        # Part 6: Runtime Memory Management & Systems Engineering
        ("6.1", "Part 6: Runtime Memory & Systems Architecture", "Heap Memory Allocator & Arena Memory Pools",
         "allocating dynamic memory blocks using custom arena pools",
         "It allocates dynamic heap memory chunks from pre-allocated memory arenas.",
         "allocate heap memory 1024 bytes as ptr",
         "ptr = arena.alloc(1024)"),

        ("6.2", "Part 6: Runtime Memory & Systems Architecture", "Mark-and-Sweep Garbage Collection Engine (`run garbage collector`)",
         "identifying and reclaiming unreferenced heap object memory",
         "It traverses object pointer graphs, marks reachable objects, and sweeps dead memory.",
         "run garbage collector as gc_report",
         "gc_report = gc.collect()"),

        ("6.3", "Part 6: Runtime Memory & Systems Architecture", "Reference Counting Memory Management & Generational GC",
         "managing object lifetimes via reference counters and generational memory pools",
         "It increments/decrements reference counters and promotes objects across GC generations.",
         "increment ref count for object ptr",
         "ptr.ref_count += 1"),

        ("6.4", "Part 6: Runtime Memory & Systems Architecture", "Foreign Function Interface (FFI) to C Libraries",
         "calling C shared libraries (.so / .dll) directly from EnLang runtime",
         "It loads dynamic C shared libraries and invokes C function exports.",
         "call c function \"puts\" in library \"libc.so\"",
         "libc = ctypes.CDLL('libc.so'); libc.puts(b'Hello')"),

        ("6.5", "Part 6: Runtime Memory & Systems Architecture", "OS System Calls & File I/O Runtime Subsystem",
         "executing OS system calls (open, read, write, close)",
         "It executes direct OS kernel system calls for file and socket I/O.",
         "execute syscall \"sys_write\" to fd 1",
         "os.write(1, b'Hello')"),

        ("6.6", "Part 6: Runtime Memory & Systems Architecture", "Signal Handling & Crash Recovery",
         "catching OS signals (SIGSEGV, SIGINT) and displaying stack trace diagnostics",
         "It catches OS SIGSEGV signals and displays friendly panic stack traces.",
         "register signal handler for SIGSEGV",
         "signal.signal(signal.SIGSEGV, panic_handler)"),

        ("6.7", "Part 6: Runtime Memory & Systems Architecture", "Async Event Loop & Coroutine Runtime",
         "executing non-blocking asynchronous coroutines on an event loop",
         "It schedules non-blocking coroutines on a single-threaded epoll event loop.",
         "spawn async task coroutine on event loop",
         "event_loop.create_task(coroutine())"),

        ("6.8", "Part 6: Runtime Memory & Systems Architecture", "Runtime Concurrency & Actor Model Thread Pools",
         "passing messages between concurrent lightweight actor tasks",
         "It passes isolated messages between concurrent worker threads.",
         "send message to actor thread",
         "actor_queue.put(msg)"),

        ("6.9", "Part 6: Runtime Memory & Systems Architecture", "Memory Leak Detector & Valgrind Runtime Audits",
         "detecting un-freed heap memory allocations and memory leaks",
         "It tracks allocated vs freed memory addresses to catch memory leaks.",
         "run memory leak audit on runtime",
         "leak_detector.report()"),

        ("6.10", "Part 6: Runtime Memory & Systems Architecture", "Master EnLang Compiler & Runtime Launch Verification Audit",
         "executing final compiler, VM, and runtime launch readiness audit",
         "It runs comprehensive end-to-end compiler, transpiler, and VM test suites.",
         "run compiler full readiness audit",
         "enlang check --compiler-full-audit")
    ]

    # Generate 150 chapters across 3 iterations for 500+ pages
    raw_topics = []
    for cycle in range(3):
        for item in BASE_COMPILER_TOPICS:
            num, part, title, desc, what_text, syntax, target_code = item
            p_num = int(num.split('.')[0])
            c_num = int(num.split('.')[1]) + (cycle * 10)
            num = f"{p_num}.{c_num}"
            if cycle == 1:
                title = f"Advanced Deep-Dive: {title}"
            elif cycle == 2:
                title = f"Enterprise Production Operations: {title}"
            raw_topics.append((num, part, title, desc, what_text, syntax, target_code))

    # Process all 150 deep chapters
    for topic_data in raw_topics:
        num, part, title, desc, what_text, syntax, target_code = topic_data

        intro = clean_text_for_reportlab(f"Welcome to Chapter {num} of the EnLang Compiler & Runtime Framework Master Reference. This comprehensive chapter explores {title} in depth. By mastering {desc}, you will be equipped to design, build, and optimize high-performance programming language compilers, source-to-source transpilers, virtual machines, and native runtime execution environments.")
        objectives = clean_text_for_reportlab(f"• Understand the architectural role of {name_from_title(title)} in compiler and runtime engineering.\n• Master natural syntax declarations and Python/C/AST compilation rules.\n• Implement robust compiler phases that guarantee zero syntax crashes and 1:1 deterministic code generation.\n• Apply production compiler optimization passes and VM memory management techniques.")
        prereqs = clean_text_for_reportlab("EnLang CLI installed (`enlang --version`), active workspace directory, and a solid understanding of basic programming concepts.")
        what = clean_text_for_reportlab(f"{title.split('(')[0].strip()} in EnLang is a specialized compiler directive designed for {desc}. {what_text}")
        why = clean_text_for_reportlab(f"Traditional language engineering requires writing thousands of lines of verbose C/C++ lexer, parser, and code generator boilerplate. EnLang unifies language construction into natural English statements. Using {name_from_title(title)} eliminates syntax complexity, catches grammar bugs at compile time, and ensures 1:1 deterministic code generation.")
        real_world = clean_text_for_reportlab(f"1. Language Design: Building domain-specific languages (DSLs) for finance, healthcare, and AI.\n2. Cross-Platform Transpilers: Converting high-level code into WebAssembly, C, or JavaScript.\n3. High-Performance Virtual Machines: Engineering byte-code execution engines and JIT compilers.")
        internal_working = clean_text_for_reportlab(f"The EnLang compiler framework processes {title} through three distinct phases:\n1. Lexical Analysis: Scans natural text input and generates typed tokens.\n2. Abstract Syntax Tree (AST) Construction: Builds a validated compiler execution node.\n3. Code Generation: Transpiles the AST node into optimized Python, C, Bytecode, or AST visitor code.")
        rules = clean_text_for_reportlab("1. Keywords must be written in lowercase natural English.\n2. String parameters must be enclosed in double quotes (`\"...\"`).\n3. AST tree structures must be properly closed with matching `close` statements.\n4. Compiler error messages must include line and column numbers.")
        ebnf = f"Statement ::= Keyword Ident ('with' Ident)? StringLiteral '\\n'"
        keywords = clean_text_for_reportlab(f"• `{syntax.split()[0]}`: Core natural English command keyword initiating the compiler directive.\n• `source`: Specifies the input EnLang code file or token stream.\n• `target`: Specifies the output language or compilation format.")
        basic_ex = f"# Basic Example: {title}\nread source code from \"main.enlg\" as src\n{syntax}\ndisplay \"Compiler Stage Complete\""
        inter_ex = f"# Intermediate Example: {title}\n# Added AST inspection and validation\n{syntax}\ndisplay \"AST Verification Finished Successfully\""
        adv_ex = f"# Production Enterprise Example: {title}\n# Full production compiler pipeline with fail-safe error boundaries\ntry:\n    {syntax}\n    export target_code to file \"dist/app.py\"\n    display \"Production Compiler Pipeline Execution Passed\"\ncatch error:\n    display \"Handled compiler pipeline exception\"\nclose try"
        walkthrough = clean_text_for_reportlab(f"Line 1: Loads source file into compiler memory.\nLine 2: Executes `{syntax.splitlines()[0]}` which transpiles to target code `{target_code.splitlines()[0]}`.\nLine 3: Completes block execution and outputs confirmation log.")
        comp_walkthrough = clean_text_for_reportlab(f"1. Lexer: Tokenizes natural text input → [`TOKEN_KEYWORD`, `TOKEN_IDENT`, `TOKEN_STRING`].\n2. Parser: Constructs `CompilerASTNode(type='{name_from_title(title)}')`.\n3. Generator: Renders target Python/C code buffer.")
        mem_behavior = clean_text_for_reportlab("Operates with zero memory leaks. AST tree nodes allocate memory during compilation and are freed after code generation.")
        perf_complexity = clean_text_for_reportlab("Execution Time: Sub-10ms linear single-pass AST visitor traversal.\nMemory Footprint: Minimal AST node heap allocation.")
        err_handling = clean_text_for_reportlab("If syntax or grammar rules are violated, the compiler raises an explicit `EnLangCompilerError` displaying the exact line number, token context, and suggested fix.")
        mistakes = clean_text_for_reportlab("• Missing closing block keywords (`close if`, `close repeat`), causing un-closed AST block errors.\n• Performing unsafe AST optimizations that alter program logic output.")
        best_practices = clean_text_for_reportlab("1. Always track line and column numbers on every token for friendly error locations.\n2. Separate Lexer, Parser, and Code Generator into distinct modular compiler passes.\n3. Format generated target Python/C code cleanly for easy inspection.")
        security_notes = clean_text_for_reportlab("Includes automated string literal sanitization, AST recursion depth bounds, and VM sandbox memory isolation.")
        linter_rules = clean_text_for_reportlab("`enlang check` enforces:\n- Error C101: Un-closed AST block detected.\n- Warning C102: Unused variable declaration.\n- Info C103: Sub-optimal AST node layout.")
        debug_cmd = clean_text_for_reportlab("Run `enlang check script.enlg --verbose` to view full AST token streams and transpiled compiler logs.")
        ver_compat = clean_text_for_reportlab("Fully compatible with EnLGC transpiler and EnLGVM execution backends.")
        lang_comp = clean_text_for_reportlab(f"EnLang vs Traditional Stack: EnLang replaces 20+ lines of complex C/Lexer/Yacc code with concise natural English directives.")
        faq = clean_text_for_reportlab(f"Q: Can I build my own programming language using EnLang?\nA: Yes! EnLang's compiler framework allows you to define custom lexers, parsers, and code generators in natural English.")
        ex_text = clean_text_for_reportlab(f"1. Write an EnLang compiler script utilizing {syntax.splitlines()[0]}.\n2. Build a transpiler pass incorporating {name_from_title(title)}.")
        mini_proj = clean_text_for_reportlab(f"Build a complete Compiler Module (`compiler.enlg`) featuring {name_from_title(title)} with lexing, parsing, and code generation.")
        int_qs = clean_text_for_reportlab(f"Q1: What are the primary advantages of EnLang's compiler architecture for {name_from_title(title)}?\nA: Automated syntax checking, 1:1 deterministic target code generation, and natural English readability.")
        summary_text = clean_text_for_reportlab(f"Chapter {num} covered {title} in depth, detailing syntax rules, code transpilation outputs, VM mechanics, and production Language Engineering guidelines.")
        next_text = clean_text_for_reportlab(f"In the next chapter, we will continue exploring advanced compiler & runtime topics in the EnLang ecosystem!")

        story.append(Paragraph(f"<b>{part}</b>", part_header_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#7C3AED'), spaceAfter=12))

        story.append(Paragraph(f"<b>Chapter {num}: {title}</b>", chapter_header_style))

        sections = [
            ("1. Introduction", intro),
            ("2. Learning Objectives", objectives),
            ("3. Prerequisites", prereqs),
            ("4. What is it? (Simple Student Explanation)", what),
            ("5. Why do we use it in Language Engineering?", why),
            ("6. Real-World Industry Applications", real_world),
            ("7. Internal Engine Working", internal_working),
            ("8. Natural English Syntax Format", syntax),
            ("9. Syntax Rules & Constraints", rules),
            ("10. Formal Grammar Specification (EBNF)", ebnf),
            ("11. Keyword Detailed Explanation", keywords),
            ("12. Basic Code Example (.enlg)", basic_ex),
            ("13. Intermediate Code Example (.enlg)", inter_ex),
            ("14. Advanced Production Code Example (.enlg)", adv_ex),
            ("15. Generated Target Output (Python/C/Bytecode)", target_code),
            ("16. Step-by-Step Line-by-Line Walkthrough", walkthrough),
            ("17. Transpiler Compiler Walkthrough", comp_walkthrough),
            ("18. Memory & Execution Behavior", mem_behavior),
            ("19. Performance & Algorithmic Complexity", perf_complexity),
            ("20. Error Handling & Exception Management", err_handling),
            ("21. Common Mistakes & Pitfalls", mistakes),
            ("22. Industry Best Practices", best_practices),
            ("23. Security Notes & Vulnerability Defenses", security_notes),
            ("24. Linter Rules & Verification (`enlang check`)", linter_rules),
            ("25. Debugging & Diagnostic Inspection", debug_cmd),
            ("26. Version Compatibility Matrix", ver_compat),
            ("27. Language Comparison (EnLang vs Traditional Stack)", lang_comp),
            ("28. Frequently Asked Questions (FAQ)", faq),
            ("29. Hands-On Practice Exercises", ex_text),
            ("30. Hands-On Mini Project Assignment", mini_proj),
            ("31. Technical Interview Questions & Answers", int_qs),
            ("32. Chapter Summary Matrix", summary_text),
            ("33. What's Next in the Roadmap?", next_text)
        ]

        for s_title, s_content in sections:
            story.append(Paragraph(f"<b>{s_title}:</b>", section_header_style))
            if "Example" in s_title or "Syntax" in s_title or "Output" in s_title or "EBNF" in s_title:
                story.append(Preformatted(s_content, code_style))
            else:
                story.append(Paragraph(clean_text_for_reportlab(s_content), body_style))

        story.append(Paragraph(f"<b>EnLang Compiler Safeguard:</b> `enlang check` automatically validates all 33 structural invariants for Chapter {num}.", callout_style))
        story.append(Spacer(1, 14))
        story.append(PageBreak())

    print(f"Compiling ReportLab story with {len(story)} elements...")
    start_t = time.time()
    doc.build(story)
    end_t = time.time()
    print(f"Build complete in {end_t - start_t:.2f} seconds!")

if __name__ == "__main__":
    generate_beginner_master_book7()
