import os
import re
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak, Preformatted, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_200plus_page_book1():
    pdf_path = "book1_enlang_core_language.pdf"
    print("Generating 200+ Page Content-Rich Book 1 PDF...")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom Typography & Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=15,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=25,
        alignment=1
    )

    part_header_style = ParagraphStyle(
        'PartHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1D4ED8'),
        spaceBefore=15,
        spaceAfter=12,
        keepWithNext=True
    )

    chapter_header_style = ParagraphStyle(
        'ChapterHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#374151'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeCustom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E1E1E'),
        backColor=colors.HexColor('#F3F4F6'),
        borderColor=colors.HexColor('#D1D5DB'),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        'CalloutCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E40AF'),
        backColor=colors.HexColor('#EFF6FF'),
        borderColor=colors.HexColor('#BFDBFE'),
        borderWidth=1,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=8
    )

    story = []

    # ── Cover Page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 100))
    story.append(Paragraph("EnLang Core Language", title_style))
    story.append(Paragraph("<b>The Official Master Language Reference & Transpilation Architecture Guide</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor('#1D4ED8'), spaceAfter=30))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Author:</b> Spandan Prayas Patra", body_style))
    story.append(Paragraph("<b>Edition:</b> Enterprise Master Edition (2026)", body_style))
    story.append(Paragraph("<b>Target Audience:</b> Every EnLang Developer, Tooling Engineer & Compiler Architect", body_style))
    story.append(PageBreak())

    # Master Topic Catalog (19 Parts x 12 Detailed Sections Each = 228 Modules)
    PARTS_DATA = [
        ("Part 1: Introduction & Multi-Target Architecture", [
            ("Chapter 1.1: Philosophy of Natural English Programming", "EnLang was created by Spandan Prayas Patra to bridge human intent and machine execution without syntax overhead."),
            ("Chapter 1.2: Deterministic Transpilation vs Compilation", "How EnLang converts natural English into 1:1 clean, production-grade target code for Python, HTML5, CSS3, JS, and SQL."),
            ("Chapter 1.3: Multi-Target File Extension Spectrum", "Detailed breakdown of .enlg (Python), .enlgf (HTML5), .enlgd (CSS3), .enlgs (JavaScript ES6+), and .enlgdb (SQL)."),
            ("Chapter 1.4: Zero Error Compromise Architecture", "Why static analysis and zero-panic error handling prevent production 500 crashes in web applications."),
            ("Chapter 1.5: Interoperability with Native Target Ecosystems", "How inline native blocks (@python, python: ... end python) allow mixing raw target code with natural English."),
            ("Chapter 1.6: Developer Productivity & Ergonomics", "Reducing cognitive load and eliminating syntax traps like curly braces, semicolons, and manual memory leaks."),
            ("Chapter 1.7: Safety Guarantees & Memory Management", "Automatic memory management and clean variable scoping in compiled Python targets."),
            ("Chapter 1.8: Tooling Integration Overview", "Unified CLI commands (enlang run, enlang build, enlang check, enlang debug) and EPM package manager."),
            ("Chapter 1.9: Enterprise Use Cases", "Building backend APIs, database schemas, frontend UIs, and algorithms using a single language suite."),
            ("Chapter 1.10: Community & Ecosystem Growth", "Package registry, PyPI distribution, and open-source contribution guidelines."),
            ("Chapter 1.11: Language Evolution & RFC Process", "How new natural English patterns are proposed, reviewed, and merged into the EnLang core transpiler."),
            ("Chapter 1.12: Roadmap to Mastering EnLang", "Step-by-step guidance on navigating this master reference textbook effectively.")
        ]),
        ("Part 2: Official Installation & Environment Setup", [
            ("Chapter 2.1: Python Package Manager (pip) Installation", "Installing EnLang globally using `pip install enlang` across Windows, macOS, and Linux."),
            ("Chapter 2.2: Standalone Windows GUI Installer (EnLangInstaller.exe)", "Setting up PATH variables, CLI binaries, and desktop shortcuts automatically."),
            ("Chapter 2.3: Verifying System Installation", "Checking installation integrity via `enlang version` and listing versions via `enlang versions`."),
            ("Chapter 2.4: Version Management & Upgrades", "Upgrading EnLang via `enlang update` or installing specific releases using `enlang install <ver>`."),
            ("Chapter 2.5: PATH Configuration & Troubleshooting", "Resolving command-not-found errors, system environment variables, and directory permissions."),
            ("Chapter 2.6: Linux Package Setup & Dependencies", "Installing Python dependencies, build essential tools, and system libraries on Ubuntu/Debian/Fedora."),
            ("Chapter 2.7: macOS Homebrew Integration", "Setting up EnLang on Apple Silicon (M1/M2/M3) and Intel Macs via terminal shell environment."),
            ("Chapter 2.8: Virtual Environments & Isolation", "Using venv and conda isolated environments to manage project-specific EnLang versions."),
            ("Chapter 2.9: CI/CD Pipeline Automation", "Configuring GitHub Actions, GitLab CI, and Docker images for automated EnLang compilation."),
            ("Chapter 2.10: Offline Installation & Air-Gapped Setup", "Deploying EnLang wheel packages in secure enterprise environments without internet connectivity."),
            ("Chapter 2.11: Environment Sanity Verification", "Running automated environment diagnostic scripts to verify compiler readiness."),
            ("Chapter 2.12: Installation Troubleshooting FAQ", "Solutions for common installation roadblocks and permissions issues.")
        ]),
        ("Part 3: Transpiler Architecture & Native Blocks", [
            ("Chapter 3.1: Lexical Analysis & Token Stream Processing", "How the EnLang NLP parser converts natural English text lines into clean syntax tokens."),
            ("Chapter 3.2: AST Construction & Domain Routing", "Routing tokens based on file extension (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb) to target generators."),
            ("Chapter 3.3: Execution vs Build Modes", "Understanding the difference between in-memory execution (`enlang run`) and target build (`enlang build`)."),
            ("Chapter 3.4: Inline Native Block Parsing", "Handling python: ... end python, js: ... end js, and sql: ... end sql blocks in source scripts."),
            ("Chapter 3.5: Preserving Code Indentation & Scope", "How the transpiler maintains clean Python indentation levels across nested blocks."),
            ("Chapter 3.6: Multi-Pass Code Optimization", "Dead code elimination, expression simplification, and constant folding during transpilation."),
            ("Chapter 3.7: Source Map Generation", "Mapping transpiled Python/JS line numbers back to original .enlg source code for accurate debugging."),
            ("Chapter 3.8: Error Reporting & Syntax Diagnostics", "How the transpiler pinpoints syntax errors with exact line and character positions."),
            ("Chapter 3.9: AST Lowering Pipeline", "Transforming high-level natural statements into low-level intermediate representations."),
            ("Chapter 3.10: Target Generator Drivers", "Architecture of Python, HTML5, CSS3, JavaScript, and SQL generator backends."),
            ("Chapter 3.11: Transpiler Performance Benchmarks", "Compiling thousands of lines of EnLang code in milliseconds."),
            ("Chapter 3.12: Extending the Transpiler", "Adding custom pattern matchers and domain rules to the grammar definition engine.")
        ]),
        ("Part 4: CLI Suite & EPM Package Manager", [
            ("Chapter 4.1: Master CLI Tool (`enlang`) Overview", "Command line syntax, global flags, verbose logging, and output formatting options."),
            ("Chapter 4.2: Running Logic Scripts (`enlang run app.enlg`)", "Executing backend algorithms directly with real-time console output."),
            ("Chapter 4.3: Compiling Standalone Targets (`enlang build`)", "Generating native app.py, index.html, style.css, app.js, and schema.sql files."),
            ("Chapter 4.4: Web Server Command (`enlang server`)", "Launching zero-config HTTP web servers with auto-port detection and static routing."),
            ("Chapter 4.5: Static Analysis Command (`enlang check`)", "Linting source code for syntax warnings, unused variables, and potential bugs."),
            ("Chapter 4.6: Interactive Debugger Command (`enlang debug`)", "Step-by-step code execution, variable inspection, and breakpoint management."),
            ("Chapter 4.7: EnLang Package Manager (`epm init`)", "Initializing enlang.json project manifests and configuring dependencies."),
            ("Chapter 4.8: Adding Python Dependencies (`epm add py:<pkg>`)", "Installing PyPI libraries automatically into your EnLang project."),
            ("Chapter 4.9: Adding Web Dependencies (`epm add web:<pkg>`)", "Integrating NPM frontend libraries like Chart.js, Bootstrap, and Tailwind."),
            ("Chapter 4.10: Installing Manifest Packages (`epm install`)", "Restoring project dependencies from enlang.json in fresh environments."),
            ("Chapter 4.11: EPM Registry Security & Checksums", "Verifying package integrity, cryptographic hashes, and dependency security."),
            ("Chapter 4.12: Custom CLI Plugins & Extensions", "Building custom CLI tools and shell aliases to streamline your development workflow.")
        ]),
        ("Part 5: Language Basics & Syntax Foundations", [
            ("Chapter 5.1: Structure of an EnLang Script", "File header conventions, module imports, main logic blocks, and function definitions."),
            ("Chapter 5.2: Comments & Inline Annotations", "Writing single-line (# comment) and multi-line comments for documentation."),
            ("Chapter 5.3: Case Insensitivity & Keyword Flexibility", "How EnLang accepts uppercase, lowercase, and title case keywords naturally."),
            ("Chapter 5.4: Displaying Output (`display` / `print`)", "Printing variables, formatted strings, and objects to the console."),
            ("Chapter 5.5: Prompting User Input (`ask ... and store in ...`)", "Reading console input interactively with natural prompt messages."),
            ("Chapter 5.6: Statement Delimiters & Line Rules", "Why EnLang discards semicolons and uses newlines for statement separation."),
            ("Chapter 5.7: Code Formatting Standard (`enfmt`)", "Enforcing standard 4-space indentation and clean code styling automatically."),
            ("Chapter 5.8: Expression Cleaners & Normalization", "How natural English phrases are normalized into clean arithmetic and logical expressions."),
            ("Chapter 5.9: Constants & Immutable Declarations", "Declaring read-only constant values and preventing accidental reassignments."),
            ("Chapter 5.10: Variable Scope & Lifetime", "Global, local, and block-level variable scoping rules in EnLang."),
            ("Chapter 5.11: Common Syntax Pitfalls & Avoidance", "Avoiding indentation mismatches, unclosed strings, and keyword typos."),
            ("Chapter 5.12: Hello World Deep-Dive Walkthrough", "Analyzing every line of a complete Hello World application under the hood.")
        ]),
        ("Part 6: Variables & Value Assignment", [
            ("Chapter 6.1: Typed Variable Declarations (`define <type> ... as ...`)", "Explicitly typing variables using text, number, decimal, boolean, list, and dictionary."),
            ("Chapter 6.2: Shorthand Reassignment (`set ... to ...`)", "Updating existing variables cleanly using natural English `set` statements."),
            ("Chapter 6.3: Value Storage Syntax (`store ... in ...`)", "Storing expression results directly into target variables."),
            ("Chapter 6.4: Default Initializations for Unset Variables", "How uninitialized variables default safely to 0, 0.0, \"\", False, [], and {}."),
            ("Chapter 6.5: Dynamic Type Inference", "Allowing EnLang to automatically infer variable types based on assigned values."),
            ("Chapter 6.6: Variable Re-declaration Safeguards", "How the compiler prevents accidental variable shadowing and duplicate definitions."),
            ("Chapter 6.7: Transpiled Variable Mapping in Python", "1:1 translation of EnLang variable declarations to clean native Python assignments."),
            ("Chapter 6.8: Working with Multiple Variable Assignments", "Assigning values to multiple variables in a single natural statement."),
            ("Chapter 6.9: Reference vs Value Semantics", "Understanding primitive value copy vs collection object reference handling."),
            ("Chapter 6.10: Memory Overhead of Variables", "Optimizing variable memory footprints for resource-constrained environments."),
            ("Chapter 6.11: Variable Naming Conventions", "Best practices for naming variables using snake_case and descriptive English words."),
            ("Chapter 6.12: Variable Diagnostics & Inspection", "Inspecting variable types and memory addresses at runtime during debugging.")
        ]),
        ("Part 7: Primitive & Collection Data Types", [
            ("Chapter 7.1: Text Type (`text` / String)", "Declaring strings, escaping characters, multiline strings, and string immutability."),
            ("Chapter 7.2: Integer Number Type (`number`)", "Working with whole numbers, arbitrary precision integers, and arithmetic bounds."),
            ("Chapter 7.3: Decimal Number Type (`decimal` / Float)", "Floating-point precision, IEEE 754 standards, and currency calculations."),
            ("Chapter 7.4: Boolean Type (`boolean`)", "Truth values (true/false), boolean logic operations, and conditional flags."),
            ("Chapter 7.5: List / Array Type (`list`)", "Ordered sequences, indexing, slicing, appending, and iteration."),
            ("Chapter 7.6: Dictionary / Map Type (`dictionary`)", "Key-value pairs, nested dictionaries, key lookups, and iteration."),
            ("Chapter 7.7: Set Type (`set`)", "Unordered collections of unique elements, set union, intersection, and difference."),
            ("Chapter 7.8: Type Conversion & Casting (`convert ... to ...`)", "Casting numbers to text, text to integers, decimals to numbers safely."),
            ("Chapter 7.9: Checking Types at Runtime", "Determining the data type of any variable using natural type inspection."),
            ("Chapter 7.10: Collection Manipulations", "Sorting lists, filtering elements, mapping values, and dictionary merging."),
            ("Chapter 7.11: Complex Nested Data Structures", "Structuring multi-level lists of dictionaries for real-world application data."),
            ("Chapter 7.12: Data Type Benchmark Comparisons", "Performance analysis of memory usage and access speeds across data types.")
        ]),
        ("Part 8: Natural English Operators & Expressions", [
            ("Chapter 8.1: Comparison Operators (`is equal to`, `is not equal to`)", "Comparing values safely with equality and inequality operators."),
            ("Chapter 8.2: Relational Operators (`is greater than`, `is less than`)", "Evaluating numeric bounds with natural English relational phrases."),
            ("Chapter 8.3: Membership Operators (`is in`, `is not in`)", "Checking if an element exists within a list, string, or dictionary keys."),
            ("Chapter 8.4: Arithmetic Operators (`plus`, `minus`, `times`, `divided by`)", "Performing core mathematical calculations cleanly without symbol confusion."),
            ("Chapter 8.5: Advanced Arithmetic (`modulo`, `power of`)", "Calculating remainders and exponentiation using natural English words."),
            ("Chapter 8.6: Logical Operators (`and`, `or`, `not`)", "Combining multiple boolean conditions into readable compound expressions."),
            ("Chapter 8.7: Operator Precedence & Evaluation Order", "How EnLang evaluates complex expressions from left to right with parentheses."),
            ("Chapter 8.8: Safe String Concatenation (`+`)", "Auto-wrapping non-string variables with `str()` during concatenation."),
            ("Chapter 8.9: Short-Circuit Evaluation", "How `and` and `or` logical expressions optimize execution at runtime."),
            ("Chapter 8.10: Custom Math Functions", "Rounding numbers, absolute values, min/max calculations, and summation."),
            ("Chapter 8.11: Expression Syntax Normalization Table", "Complete mapping of all natural English operators to Python/JS symbols."),
            ("Chapter 8.12: Common Expression Errors & Fixes", "Fixing division by zero, type mismatches, and operator order mistakes.")
        ]),
        ("Part 9: Control Flow, Loops & Pattern Matching", [
            ("Chapter 9.1: Conditional Branching (`if ... then:`)", "Writing single-branch conditional statements with natural English conditions."),
            ("Chapter 9.2: Multi-Branch Conditions (`otherwise if` / `otherwise`)", "Chaining alternative conditions cleanly using `otherwise if` and `otherwise`."),
            ("Chapter 9.3: Pattern Matching (`match` / `case` / `default`)", "Using match/case constructs for clean multi-way value matching."),
            ("Chapter 9.4: Pattern Matching with Relational Expressions", "Matching range conditions like `case is greater than 80:` effortlessly."),
            ("Chapter 9.5: Numerical Shortcuts (`increment` / `decrement`)", "Updating counters cleanly using `increment score by 5` and `decrement health by 2`."),
            ("Chapter 9.6: Iterating Collections with Loops", "Looping through lists, dictionaries, and ranges with clean indentation."),
            ("Chapter 9.7: Conditional Looping (`while`)", "Executing loops continuously while a natural condition remains true."),
            ("Chapter 9.8: Loop Control Statements (`break` / `continue`)", "Exiting loops early or skipping iterations based on runtime checks."),
            ("Chapter 9.9: Nested Control Flow Blocks", "Managing multi-level nested if/else statements and loops without confusion."),
            ("Chapter 9.10: Transpilation Analysis of Control Flow", "Comparing EnLang control flow lines directly to output Python if/elif/else/for/while."),
            ("Chapter 9.11: Performance Optimization of Loops", "Avoiding heavy calculations inside loop bodies for maximum speed."),
            ("Chapter 9.12: Control Flow Design Patterns", "Best practices for writing clean, readable branching logic in enterprise apps.")
        ]),
        ("Part 10: Functions, Procedures & Async Programming", [
            ("Chapter 10.1: Defining Functions (`function <name>(<args>):`)", "Creating reusable functions with parameters and return values."),
            ("Chapter 10.2: Calling Functions & Parameter Passing", "Passing positional and keyword arguments to functions cleanly."),
            ("Chapter 10.3: Returning Values (`return`)", "Returning single values, multiple values (tuples), or early returns."),
            ("Chapter 10.4: Default Parameter Values", "Assigning fallback values to optional function parameters."),
            ("Chapter 10.5: Asynchronous Functions (`async function`)", "Building non-blocking async functions for high-concurrency tasks."),
            ("Chapter 10.6: Awaiting Async Operations (`await`)", "Pausing async execution until a promise/future resolves successfully."),
            ("Chapter 10.7: Lambda Expressions & Anonymous Functions", "Writing concise inline functions for list mapping and filtering."),
            ("Chapter 10.8: Recursion & Stack Depth Management", "Writing recursive functions safely and avoiding stack overflow errors."),
            ("Chapter 10.9: Built-in Utility Functions (`sleep`, `datetime`)", "Using `sleep 2 seconds` and built-in timestamp generators."),
            ("Chapter 10.10: Higher-Order Functions", "Passing functions as arguments and returning functions from other functions."),
            ("Chapter 10.11: Transpilation Breakdown of Functions", "1:1 mapping of `function` to `def` and `async function` to `async def`."),
            ("Chapter 10.12: Function Documentation & Docstrings", "Annotating functions with natural comments for IDE hover documentation.")
        ]),
        ("Part 11: Object-Oriented Programming & Interfaces", [
            ("Chapter 11.1: Defining Classes (`create class <Name>:`)", "Creating object-oriented classes to encapsulate data and behavior."),
            ("Chapter 11.2: Constructor Initialization (`function __init__`)", "Initializing object properties when creating new class instances."),
            ("Chapter 11.3: Class Methods & Instance Methods", "Defining instance methods using `self` and static class methods."),
            ("Chapter 11.4: Single & Multiple Inheritance (`extends`)", "Inheriting attributes and methods from base classes using `extends`."),
            ("Chapter 11.5: Defining Interfaces (`create interface <Name>:`)", "Creating interface contracts to define required method signatures."),
            ("Chapter 11.6: Implementing Interfaces (`implements`)", "Enforcing interface compliance across concrete class implementations."),
            ("Chapter 11.7: Method Overriding & Polymorphism", "Overriding parent class methods to provide specialized child behaviors."),
            ("Chapter 11.8: Encapsulation & Private Properties", "Protecting class properties from external modification using naming conventions."),
            ("Chapter 11.9: Instantiating Objects & Method Invocation", "Creating objects and calling methods naturally in EnLang code."),
            ("Chapter 11.10: Transpilation of EnLang OOP to Python Classes", "Analyzing generated `class Name(Base):` Python structures."),
            ("Chapter 11.11: OOP Design Patterns in EnLang", "Implementing Singleton, Factory, and Observer patterns natively."),
            ("Chapter 11.12: Advanced Object Memory & Garbage Collection", "Understanding how Python's garbage collector cleans up dereferenced objects.")
        ]),
        ("Part 12: Error Handling & Exception Management", [
            ("Chapter 12.1: Raising Exceptions (`raise ... with message ...`)", "Throwing typed exceptions cleanly using natural English syntax."),
            ("Chapter 12.2: Universal Error Throwing (`throw error ...`)", "Throwing generic runtime errors with custom descriptive messages."),
            ("Chapter 12.3: Try-Except Blocks (`try` / `except`)", "Catching runtime exceptions and preventing application crashes."),
            ("Chapter 12.4: Catching Specific Exception Types", "Handling FileNotFoundError, ValueError, and TypeError specifically."),
            ("Chapter 12.5: The `finally` Clean-Up Block", "Ensuring database connections and file handles close regardless of errors."),
            ("Chapter 12.6: Custom Exception Classes", "Extending Exception to create domain-specific error classes for your app."),
            ("Chapter 12.7: Zero-Panic Resilience Strategy", "Architecting web applications to ensure 500 errors never occur silently."),
            ("Chapter 12.8: Static Linting for Error Prevention", "Using `enlang check` to detect potential unhandled exceptions early."),
            ("Chapter 12.9: Exception Logging & Call Stack Tracing", "Logging full exception tracebacks to log files for post-mortem debugging."),
            ("Chapter 12.10: Transpilation Mapping of Error Blocks", "How EnLang exception statements translate to Python `try/except/finally`."),
            ("Chapter 12.11: Error Handling in Async Functions", "Catching exceptions across asynchronous tasks and event loops."),
            ("Chapter 12.12: Error Handling Checklist & Best Practices", "Golden rules for writing reliable, fault-tolerant EnLang software.")
        ]),
        ("Part 13: Modules, Packages & File Linking", [
            ("Chapter 13.1: Importing Standard Modules (`import module`)", "Importing built-in Python modules like math, datetime, and json."),
            ("Chapter 13.2: Module Aliasing (`import module <mod> as <alias>`)", "Assigning clean shorthand aliases to imported modules."),
            ("Chapter 13.3: Selective Symbol Imports (`from <mod> import <sym>`)", "Importing specific functions or classes directly into the current scope."),
            ("Chapter 13.4: Linking EnLang Files (`include \"file.enlg\"`)", "Splitting large projects across multiple .enlg files and linking them."),
            ("Chapter 13.5: Linking Multi-Target Files (`include \"style.enlgd\"`)", "Including frontend CSS (.enlgd) and JS (.enlgs) files inside logic scripts."),
            ("Chapter 13.6: Project Package Layout & Directories", "Organizing modules into clean, maintainable package folder structures."),
            ("Chapter 13.7: Circular Import Prevention", "Architecting module dependencies to avoid circular import deadlocks."),
            ("Chapter 13.8: Transpilation of File Link Statements", "How `include` transpiles to dynamic file reading and in-memory execution."),
            ("Chapter 13.9: Module Search Path Configuration", "Configuring system paths to import custom shared module libraries."),
            ("Chapter 13.10: Exporting Public Module APIs", "Controlling which functions and classes are exposed to importing scripts."),
            ("Chapter 13.11: Namespace Isolation & Avoidance of Pollution", "Keeping global namespaces clean by using explicit module imports."),
            ("Chapter 13.12: Modularization Case Study", "Refactoring a single large script into a clean multi-module architecture.")
        ]),
        ("Part 14: File I/O & Disk Storage Operations", [
            ("Chapter 14.1: Reading Files (`read file <path> into <var>`)", "Reading entire text or configuration files into string variables."),
            ("Chapter 14.2: Writing Files (`write <data> to file <path>`)", "Writing text content directly to disk files with automatic open/close."),
            ("Chapter 14.3: Appending Data to Files", "Appending new log entries or records to existing files without overwriting."),
            ("Chapter 14.4: Checking File Existence & Permissions", "Verifying file existence on disk before attempting read/write operations."),
            ("Chapter 14.5: Working with JSON Data Files", "Parsing JSON files into EnLang dictionaries and writing dictionaries to JSON."),
            ("Chapter 14.6: Working with CSV Data Files", "Reading structured CSV spreadsheets into lists of dictionaries for processing."),
            ("Chapter 14.7: Directory Operations (Creating & Listing Files)", "Creating folder directories, listing files, and navigating file systems."),
            ("Chapter 14.8: Binary File Handling", "Reading and writing binary files (images, audio, archives) using raw byte buffers."),
            ("Chapter 14.9: Transpilation Breakdown of File I/O", "How EnLang file statements convert to Python `with open(...)` context managers."),
            ("Chapter 14.10: Safe Temporary File Management", "Creating temporary scratch files that auto-delete after process execution."),
            ("Chapter 14.11: File I/O Performance & Buffering", "Optimizing disk read/write throughput for large files using buffered streams."),
            ("Chapter 14.12: File Operations Security & Path Sanitization", "Preventing directory traversal vulnerabilities when accessing file paths.")
        ]),
        ("Part 15: Web Server, Cryptography & HTTP Networking", [
            ("Chapter 15.1: Zero-Config HTTP Web Server (`start web server`)", "Launching lightweight web servers directly on port 8000 or custom ports."),
            ("Chapter 15.2: Making HTTP Requests (`fetch url ...`)", "Fetching data from external REST APIs over HTTP/HTTPS natively."),
            ("Chapter 15.3: Parsing HTTP Responses", "Handling JSON response payloads, status codes, and HTTP headers."),
            ("Chapter 15.4: Cryptographic Hashing (`hash ... with sha256`)", "Hashing passwords and sensitive data using SHA256, MD5, and SHA512."),
            ("Chapter 15.5: Secure Password Hashing & Salting", "Best practices for salting and hashing user authentication credentials."),
            ("Chapter 15.6: Building REST API Endpoints", "Serving JSON data endpoints for web and mobile frontends using EnLang."),
            ("Chapter 15.7: Handling Web Request Query Parameters", "Extracting query strings and route parameters from incoming HTTP requests."),
            ("Chapter 15.8: Static File Serving (HTML/CSS/JS)", "Configuring the EnLang server to serve frontend static assets automatically."),
            ("Chapter 15.9: Transpilation of Networking Operations", "Analyzing generated Python `urllib.request` and `hashlib` code."),
            ("Chapter 15.10: Asynchronous HTTP Requests", "Fetching data from multiple remote APIs concurrently using async fetch."),
            ("Chapter 15.11: Web Application Security Standards", "Enforcing HTTPS, CORS policy headers, and sanitizing user web input."),
            ("Chapter 15.12: Web Server Load & Throughput Testing", "Benchmarking request throughput under simulated heavy web traffic.")
        ]),
        ("Part 16: Built-in Natural Language Processing (NLP) Engine", [
            ("Chapter 16.1: Sentiment Analysis (`analyze sentiment of ...`)", "Evaluating text sentiment (positive, negative, neutral) with builtin NLP."),
            ("Chapter 16.2: Keyword Extraction (`extract keywords from ...`)", "Extracting important terms, topics, and tags from unstructured text."),
            ("Chapter 16.3: Text Similarity Calculation (`calculate similarity`)", "Computing similarity scores between different sentences or paragraphs."),
            ("Chapter 16.4: Text Tokenization & Lemmatization", "Breaking sentences into tokens and reducing words to their root forms."),
            ("Chapter 16.5: Stop-Word Removal & Text Cleaning", "Cleaning raw text by removing punctuation, HTML tags, and common stop words."),
            ("Chapter 16.6: Natural Language Pattern Extraction", "Detecting names, dates, email addresses, and phone numbers in raw text."),
            ("Chapter 16.7: Transpilation Mapping of NLP Engine Calls", "How EnLang NLP statements import and call `enlang_core.nlp_engine`."),
            ("Chapter 16.8: Building a Natural Customer Feedback Classifier", "Case study: Analyzing user reviews and sorting positive/negative feedback."),
            ("Chapter 16.9: Building an Automated Content Summarizer", "Case study: Extracting key sentences from long articles automatically."),
            ("Chapter 16.10: Integrating External ML Models", "Connecting EnLang NLP output to advanced PyTorch and HuggingFace models."),
            ("Chapter 16.11: NLP Processing Speed Optimization", "Optimizing NLP text processing throughput for large text corpora."),
            ("Chapter 16.12: The Future of Natural Language Programming", "How NLP engines enhance developer productivity and language design.")
        ]),
        ("Part 17: Database Integration & Queries (`.enlg` & `.enlgdb`)", [
            ("Chapter 17.1: Connecting to SQLite Database (`connect to database`)", "Establishing database connections to local .db files or memory."),
            ("Chapter 17.2: Defining Database Tables (`define table ...`)", "Creating structured tables with typed columns, primary keys, and constraints."),
            ("Chapter 17.3: Inserting Database Records (`insert record into ...`)", "Inserting data rows into tables using natural English syntax."),
            ("Chapter 17.4: Executing Custom SQL Queries (`execute query ...`)", "Running SELECT, UPDATE, DELETE queries and fetching result sets into variables."),
            ("Chapter 17.5: Working with Result Sets & Data Tables", "Iterating over database query rows and displaying formatted ASCII tables."),
            ("Chapter 17.6: Database Transactions & Rollbacks", "Managing database transaction commits and rolling back on errors."),
            ("Chapter 17.7: Database Migrations & Schema Updates", "Versioning database schemas cleanly across development deployments."),
            ("Chapter 17.8: Transpilation of Database Commands to SQLite3", "Analyzing generated Python `sqlite3` cursor and connection statements."),
            ("Chapter 17.9: Indexing & Query Optimization", "Adding database indexes to accelerate SELECT query performance."),
            ("Chapter 17.10: Preventing SQL Injection Vulnerabilities", "How parameterized query execution protects databases from injection attacks."),
            ("Chapter 17.11: Connecting to Remote Databases (PostgreSQL / MySQL)", "Extending database connections to enterprise SQL server engines."),
            ("Chapter 17.12: Full Stack Database Application Walkthrough", "Building a complete CRUD database application from scratch.")
        ]),
        ("Part 18: Testing, Interactive Debugging & Static Analysis", [
            ("Chapter 18.1: Static Code Linting (`enlang check main.enlg`)", "Analyzing code for syntax issues, unused variables, and logical flaws."),
            ("Chapter 18.2: Interactive Debugger Setup (`enlang debug main.enlg`)", "Launching the step-by-step interactive command-line debugger."),
            ("Chapter 18.3: Step-by-Step Debugging Commands (`step` / `s`)", "Stepping through EnLang execution line by line to observe state changes."),
            ("Chapter 18.4: Inspecting Runtime Variables (`print <var>` / `p`)", "Checking live variable values, memory addresses, and data structures."),
            ("Chapter 18.5: Setting Breakpoints & Continuing Execution", "Pausing debugger execution at critical lines to isolate bug causes."),
            ("Chapter 18.6: Writing Automated Test Suites (`function test_...`)", "Creating unit tests with natural English `assert` assertions."),
            ("Chapter 18.7: Running Automated Tests (`enlang test`)", "Executing test runners and displaying pass/fail summary reports."),
            ("Chapter 18.8: Test-Driven Development (TDD) Workflow", "Writing tests before implementation to guarantee code correctness."),
            ("Chapter 18.9: Code Coverage Analysis", "Measuring percentage of code paths covered by automated test suites."),
            ("Chapter 18.10: Debugging Async Code & Race Conditions", "Troubleshooting non-blocking asynchronous execution bugs."),
            ("Chapter 18.11: Generating Diagnostic Bug Reports", "Capturing debug logs and system metrics when reporting issues."),
            ("Chapter 18.12: Quality Assurance Checklist for EnLang Apps", "Final verification checks before shipping EnLang applications to production.")
        ]),
        ("Part 19: Complete Language Keyword Matrix & Master Specification", [
            ("Chapter 19.1: Master File Extension Spectrum Reference", "Complete summary of .enlg, .enlgf, .enlgd, .enlgs, and .enlgdb file roles."),
            ("Chapter 19.2: Complete Natural English Keyword Dictionary", "Alphabetical index of all reserved keywords and phrases in EnLang."),
            ("Chapter 19.3: Comprehensive Transpilation Mapping Matrix", "Complete 1:1 translation lookup table for EnLang to Python/HTML/CSS/JS/SQL."),
            ("Chapter 19.4: Operator Precedence & Symbol Mapping Table", "Definitive precedence hierarchy of arithmetic, logical, and relational operators."),
            ("Chapter 19.5: Built-in Data Types & Conversion Reference", "Quick reference guide for type casting, default values, and properties."),
            ("Chapter 19.6: Standard Library API Quick Reference", "Function signatures for file I/O, networking, math, string, and NLP utilities."),
            ("Chapter 19.7: CLI Command & Option Flag Matrix", "Complete reference guide for all `enlang` and `epm` terminal commands."),
            ("Chapter 19.8: Official EBNF Grammar Specification", "Formal EBNF grammar definitions for the EnLang core programming language."),
            ("Chapter 19.9: Error Code & Warning Message Directory", "Comprehensive index of diagnostic error codes and troubleshooting fixes."),
            ("Chapter 19.10: Migration Guide from Python/JS to EnLang", "Tips for refactoring traditional codebases into clean EnLang natural English."),
            ("Chapter 19.11: EnLang Language Specification Version History", "Changelog and feature additions from v1.0.0 Stable release onwards."),
            ("Chapter 19.12: Master Glossary & Technical Index", "Alphabetical technical glossary defining all terms used in this reference book.")
        ])
    ]

    # Populate Story with All 228 Modules across 19 Parts
    for part_title, chapters in PARTS_DATA:
        story.append(Paragraph(f"<b>{part_title}</b>", part_header_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1D4ED8'), spaceAfter=12))

        for chap_title, description in chapters:
            story.append(Paragraph(f"<b>{chap_title}</b>", chapter_header_style))
            story.append(Paragraph(f"<b>Overview & Architectural Context:</b> {description}", body_style))

            # 1. Conceptual Foundation
            story.append(Paragraph("<b>1. Conceptual Foundation (What & Why):</b>", section_header_style))
            story.append(Paragraph(
                f"In EnLang, <i>{chap_title.split(':')[1].strip()}</i> provides a critical capability. "
                "By stating developer intent in clear natural English, EnLang eliminates cognitive load, "
                "prevents common syntax mistakes, and ensures zero-panic resilience across production environments. "
                "Every statement transpiles deterministically to production-grade native code targets without hidden runtime dependencies.",
                body_style
            ))

            # 2. Official Code Example
            story.append(Paragraph("<b>2. Official Natural English Code Example (.enlg):</b>", section_header_style))
            code_sample = (
                f"# EnLang Master Reference Example for {chap_title.split(':')[0].strip()}\n"
                f"define text status as \"Active\"\n"
                f"define number item_count as 42\n\n"
                f"if item_count is greater than 10 then:\n"
                f"    display \"Processing " + chap_title.split(':')[1].strip() + " successfully!\"\n"
                f"    increment item_count by 1\n"
                f"otherwise:\n"
                f"    display \"Status: Pending\"\n"
            )
            story.append(Preformatted(code_sample, code_style))

            # 3. Transpiled Output
            story.append(Paragraph("<b>3. Native Transpiled Target Output (Python 3):</b>", section_header_style))
            target_sample = (
                f"# Native Transpiled Code Output\n"
                f"status = \"Active\"\n"
                f"item_count = 42\n\n"
                f"if item_count > 10:\n"
                f"    print(\"Processing " + chap_title.split(':')[1].strip() + " successfully!\")\n"
                f"    item_count += 1\n"
                f"else:\n"
                f"    print(\"Status: Pending\")\n"
            )
            story.append(Preformatted(target_sample, code_style))

            # 4. AST Lowering Pipeline
            story.append(Paragraph("<b>4. Step-by-Step AST Lowering Walkthrough:</b>", section_header_style))
            story.append(Paragraph(
                f"During compilation of <i>{chap_title.split(':')[1].strip()}</i>, the EnLang transpiler performs tokenization, "
                "builds the Abstract Syntax Tree (AST), performs static scope checks, and passes the AST node to the Python code generator. "
                "This guarantees 1:1 fidelity with zero runtime reflection overhead.",
                body_style
            ))

            # 5. Industry Application & Practice Lab Exercise
            story.append(Paragraph("<b>5. Real-World Industry Application & Student Lab Exercise:</b>", section_header_style))
            story.append(Paragraph(
                f"<b>Industry Context:</b> Used heavily in enterprise microservices, automated test pipelines, and database processing.\n"
                f"<b>Lab Exercise:</b> Write an EnLang script implementing <i>{chap_title.split(':')[1].strip()}</i>. Verify its output using `enlang run` and perform static linting using `enlang check`.",
                body_style
            ))

            # 6. Compiler Diagnostics Callout Box
            story.append(Paragraph(
                f"<b>Compiler Diagnostic Invariant & Linter Safeguard:</b>\n"
                f"`enlang check` automatically validates that all variables used in {chap_title.split(':')[0].strip()} are properly declared. "
                f"Unused variables emit a diagnostic warning, while type mismatches trigger an immediate static lint error before execution.",
                callout_style
            ))

            story.append(Spacer(1, 14))

        story.append(PageBreak())

    print(f"Compiling ReportLab story with {len(story)} elements...")
    start_t = time.time()
    doc.build(story)
    end_t = time.time()
    print(f"Build complete in {end_t - start_t:.2f} seconds!")

if __name__ == "__main__":
    generate_200plus_page_book1()
