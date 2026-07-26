"""
EnLang Book 1 Generator — 500+ Page Comprehensive Student Textbook Builder
Generates 30 rich part modules across 150 chapters to produce a 500+ page PDF.
Author: Spandan Prayas Patra
"""
import os
import sys

PARTS_DATA = [
    ("Part I — Introduction, Vision & History", [
        (1, "Welcome to EnLang Platform", "EnLang is a Universal Natural English Programming Language Platform designed for deterministic execution.", "What is EnLang?", "Why EnLang? Vision & Goals"),
        (2, "History & Evolution of EnLang", "Tracing the development from early transpiler prototypes to version 1.1.2.", "Historical Milestones", "Language Evolution"),
        (3, "EnLang vs Traditional Languages", "Comprehensive comparative analysis against Python, C++, Java, and Rust.", "Comparative Matrix", "Performance & Safety Metrics"),
        (4, "First Principles & Language Philosophy", "Deterministic AST mapping without probabilistic NLP hallucination.", "Deterministic Mapping", "Zero Syntax Friction"),
        (5, "The 14 Core Platform Specifications", "Overview of the 14 foundational charters governing EnLang compiler standards.", "Platform Charter Overview", "Specification Alignment"),
    ]),
    ("Part II — Cross-Platform Installation & Tooling", [
        (6, "System Requirements & Prerequisites", "Hardware requirements, OS support, Python dependencies, and environment setup.", "Hardware Specs", "OS Compatibility"),
        (7, "Windows Installation Guide", "Step-by-step Windows installation via PyPI and standalone installer.", "PyPI Command Line", "Environment Variables"),
        (8, "Linux & macOS Installation Guide", "Installing EnLang on Ubuntu, Debian, Fedora, Arch, and macOS Homebrew.", "Terminal Commands", "Permission Setup"),
        (9, "Verifying Installation & CLI Tools", "Using enlang check, enlang run, and enlang versions to confirm operational health.", "CLI Diagnostics", "Verification Commands"),
        (10, "VS Code Extension & IDE Setup", "Configuring language server, syntax highlighting, snippets, and linting in VS Code.", "VS Code Extension", "Snippets & Autocomplete"),
    ]),
    ("Part III — Compiler & Interpreter Architecture", [
        (11, "Compiler Engine Overview", "High-level overview of the EnLang translation graph and code generator.", "Compilation Pipeline", "Target Code Emitters"),
        (12, "Interpreter Engine Overview", "The fast AST-interpreter engine for interactive REPL execution.", "AST Interpreter", "REPL Architecture"),
        (13, "Dual-Engine Execution Model", "How compiler and interpreter co-exist for development vs production.", "Dual Engine Workflow", "Performance Trade-offs"),
        (14, "Transpilation Targets", "Emitting clean code for Python 3, C++17, Rust, HTML5, CSS3, and SQL.", "Target Languages", "Zero-Overhead Binding"),
        (15, "Build Systems & Native Compilation", "Compiling EnLang source code into standalone binary executables.", "Standalone Binaries", "Build Configuration"),
    ]),
    ("Part IV — Command Line Interface (CLI) Suite", [
        (16, "EnLang CLI Command Structure", "Command line options, positional arguments, and execution flags.", "CLI Command Reference", "Flag Matrix"),
        (17, "Executing Scripts with 'enlang run'", "Running .enlg scripts, passing command-line arguments, and displaying target code.", "Execution Workflow", "Target Debug Flags"),
        (18, "Compiling Executables with 'enlang build'", "Compiling standalone binaries for distribution.", "Binary Creation", "Release Optimization"),
        (19, "Static Checking with 'enlang check'", "Running static analysis, symbol checking, and syntax linting.", "Linting Engine", "Diagnostic Output"),
        (20, "Web Runner with 'enlang server'", "Launching local HTTP server and web app runner engine.", "Web Server Execution", "Port Binding"),
    ]),
    ("Part V — EnLang Language Basics", [
        (21, "Lexical Structure & Tokens", "Character sets, UTF-8 unicode encoding, and lexical tokens.", "UTF-8 Encoding", "Tokenization Rules"),
        (22, "Keywords & Reserved Terms", "Exhaustive list of reserved natural English keywords and verbs.", "Keyword Registry", "Forbidden Identifiers"),
        (23, "Identifiers & Naming Rules", "Variable, function, and class naming conventions in EnLang.", "Naming Standards", "Snake Case Conventions"),
        (24, "Comments & Documentation", "Single-line and multi-line comments, docstrings, and docgen tags.", "Inline Comments", "Docstring Formatting"),
        (25, "Whitespace & Indentation Rules", "Block structure, indentation rules, and scope demarcation.", "Block Indentation", "Scope Bounds"),
    ]),
    ("Part VI — Variables, Mutability & Scope", [
        (26, "Concept: What is a Variable?", "Memory representation, references, and value containers.", "Memory Layout", "Value Binding"),
        (27, "Variable Declaration Syntax", "Declaring variables using 'define <type> <name> as <val>'.", "Define Statement", "Initialization Rules"),
        (28, "Updating Variables", "Re-assigning values using 'set <name> to <val>'.", "Set Statement", "Re-assignment Rules"),
        (29, "Scope & Mutability Rules", "Lexical scoping, block isolation, and mutability behavior.", "Scope Chain", "Block Isolation"),
        (30, "Constants & Immutable Values", "Declaring read-only constant bindings.", "Constant Declarations", "Immutability Guards"),
    ]),
    ("Part VII — Primitive & Domain Data Types", [
        (31, "Integer Data Type", "Signed 64-bit integer values, operations, and limits.", "Integer Representation", "Numeric Bounds"),
        (32, "Float & Decimal Types", "Floating-point numbers, precision, and decimal math.", "Floating Point Math", "Decimal Precision"),
        (33, "Text (String) Data Type", "Unicode text strings, string operations, and escape sequences.", "Text Manipulation", "Unicode Encoding"),
        (34, "Boolean Data Type", "Logical truth values (true, false) and boolean logic.", "Truth Values", "Boolean Operations"),
        (35, "Null & Optional Types", "Handling missing data, null values, and optional wrappers.", "Null Semantics", "Optional Types"),
    ]),
    ("Part VIII — Operators & Natural Expressions", [
        (36, "Arithmetic Operators", "plus, minus, times, divided by, modulo, and exponentiation.", "Arithmetic Verbs", "Precedence Rules"),
        (37, "Comparison Operators", "is equal to, is not equal to, is greater than, is less than.", "Comparison Phrases", "Logical Truth Tables"),
        (38, "Logical Operators", "and, or, not, and complex boolean expressions.", "Logical Combination", "Short-Circuiting"),
        (39, "Range & Pipeline Operators", "from A to B, range syntax, and pipeline operators.", "Range Expressions", "Pipeline Chaining"),
        (40, "Operator Precedence Matrix", "Formal operator precedence and evaluation hierarchy.", "Precedence Table", "Parentheses Folding"),
    ]),
    ("Part IX — Input & Output Management", [
        (41, "Console Output with 'display'", "Printing values, auto-formatting, and newline handling.", "Display Statement", "Console Formatting"),
        (42, "Console Input Reading", "Reading user input from standard input stream.", "Input Prompting", "Type Conversion"),
        (43, "String Interpolation", "Embedding expressions inside text strings naturally.", "Interpolation Syntax", "Expression Evaluation"),
        (44, "Formatted Console Output", "Table formatting, column alignment, and colored output.", "Console Formatting", "CLI Layouts"),
        (45, "Structured Logging Engine", "log info, log warn, log error statements.", "Logging Levels", "Log Formatting"),
    ]),
    ("Part X — Decision Making & Branching", [
        (46, "If-Then Conditional Statements", "Single branch decision making with if statements.", "If Statements", "Boolean Guards"),
        (47, "If-Else Branching", "Two-way branching logic with if and else blocks.", "If-Else Control Flow", "Branch Execution"),
        (48, "Multi-Branch Else-If Logic", "Multi-way conditional evaluation chains.", "Else-If Chains", "Evaluation Order"),
        (49, "Structural Pattern Matching", "match statements, case branches, and default guards.", "Match Syntax", "Pattern Destructuring"),
        (50, "Guard Clause Patterns", "Early returns and guard assertions.", "Guard Assertions", "Early Return Rules"),
    ]),

    ("Part XI — Loops & Iterative Execution", [
        (51, "Repeat N Times Loop", "Fixed iteration loops without counter boilerplate.", "Repeat Statements", "Loop Bound Evaluation"),
        (52, "Foreach Collection Loops", "Iterating over lists, tuples, sets, and data streams.", "Foreach Syntax", "Element Binding"),
        (53, "Conditional While Loops", "Condition-driven while loops and termination criteria.", "While Loops", "Termination Conditions"),
        (54, "Do-While Loops", "Post-condition evaluated iterative loops.", "Do-While Syntax", "Execution Semantics"),
        (55, "Loop Control: Break & Continue", "Early loop termination and skipping iterations.", "Break Statement", "Continue Statement"),
    ]),

    ("Part XII — Functions & Modular Routines", [
        (56, "Function Declarations", "Declaring functions with parameters and return values.", "Function Syntax", "Return Statements"),
        (57, "Parameter Passing Rules", "Positional, named, and default parameter values.", "Parameter Passing", "Default Values"),
        (58, "Variadic Functions", "Accepting variable numbers of arguments.", "Variadic Parameters", "Argument Lists"),
        (59, "Recursion Principles", "Recursive function design, base cases, and stack depth.", "Recursive Calls", "Base Case Guards"),
        (60, "Function Scope & Closures", "Lexical environment capture and closed variable state.", "Closure State", "Lexical Scoping"),
    ]),

    ("Part XIII — Object-Oriented Programming (OOP)", [
        (61, "Classes & Blueprint Design", "Declaring classes, properties, and methods in EnLang.", "Class Syntax", "Property Binding"),
        (62, "Object Instantiation", "Creating instances of classes and managing lifecycles.", "Instantiation", "Instance State"),
        (63, "Constructors with 'init'", "Initialization constructors and parameter binding.", "Init Constructor", "State Assignment"),
        (64, "Destructors & Cleanup", "Object teardown, resource disposal, and finalizers.", "Destructor Hooks", "Resource Cleanup"),
        (65, "Method Invocation & 'this'", "Accessing instance properties via 'this' keyword.", "This Pointer", "Method Dispatch"),
    ]),

    ("Part XIV — OOP Inheritance & Encapsulation", [
        (66, "Single Inheritance", "Subclassing and deriving features with 'inherits'.", "Subclass Syntax", "Superclass Binding"),
        (67, "Multiple Inheritance", "Deriving behavior from multiple parent classes.", "Multiple Inheritance", "Diamond Problem Handling"),
        (68, "Method Overriding & 'super'", "Overriding parent methods and invoking 'super'.", "Method Overriding", "Super Calls"),
        (69, "Encapsulation Visibility", "private, protected, and public member access rules.", "Visibility Controls", "Encapsulation Guards"),
        (70, "Getters & Setters", "Property accessors and mutator methods.", "Getter Methods", "Setter Validation"),
    ]),

    ("Part XV — Polymorphism & Interfaces", [
        (71, "Polymorphism Principles", "Dynamic method dispatch and interface polymorphism.", "Dynamic Dispatch", "Polymorphic Call Trees"),
        (72, "Interface Contracts", "Declaring interface contracts and enforcing compliance.", "Interface Syntax", "Contract Verification"),
        (73, "Abstract Classes", "Partial implementations and abstract method requirements.", "Abstract Classes", "Abstract Methods"),
        (74, "Operator Overloading", "Customizing operator behaviors ('plus', 'times') for classes.", "Operator Overloading", "Custom Math Methods"),
        (75, "Composition vs Inheritance", "Designing modular systems using object composition.", "Object Composition", "Design Patterns"),
    ]),

    ("Part XVI — Functional Programming Paradigm", [
        (76, "Lambda Expressions", "Anonymous inline functions and lambda syntax.", "Lambda Functions", "Inline Expressions"),
        (77, "Higher-Order Functions", "Functions accepting or returning other functions.", "Higher-Order Functions", "Function Arguments"),
        (78, "Map Transformation", "Transforming collection elements using 'map'.", "Map Function", "Element Transformation"),
        (79, "Filter Predicates", "Filtering collections using boolean predicates.", "Filter Function", "Predicate Evaluation"),
        (80, "Reduce Aggregation", "Aggregating collection elements into single values.", "Reduce Function", "Accumulator State"),
    ]),

    ("Part XVII — Built-in Collections", [
        (81, "Arrays & Static Lists", "Fixed-size contiguous array memory layout.", "Array Allocation", "Indexed Access"),
        (82, "Dynamic Lists", "Resizable lists, append, insert, pop, and slice operations.", "List Operations", "Dynamic Resizing"),
        (83, "Immutable Tuples", "Fixed-size immutable element tuples.", "Tuple Allocation", "Immutability Rules"),
        (84, "Key-Value Dictionaries", "Hash map key-value lookup dictionaries.", "Dictionary Syntax", "Hash Table Lookup"),
        (85, "Unique Sets", "Unordered unique element sets and set algebra.", "Set Operations", "Set Union & Intersection"),
    ]),

    ("Part XVIII — Advanced Data Structures", [
        (86, "Stack Data Structure", "LIFO stack operations: push, pop, peek, and bounds.", "Stack Implementation", "LIFO Operations"),
        (87, "Queue & Deque", "FIFO queue operations: enqueue, dequeue, and double-ended queues.", "Queue Implementation", "FIFO Operations"),
        (88, "Binary Search Trees", "Tree nodes, recursive traversal, and search complexity.", "Tree Traversal", "BST Operations"),
        (89, "Min & Max Heaps", "Priority queue implementation via heap trees.", "Heap Array Layout", "Heapify Operations"),
        (90, "Adjacency Graphs", "Graph representations, nodes, edges, and path traversal.", "Graph Nodes & Edges", "Pathfinding Algorithms"),
    ]),

    ("Part XIX — Error & Exception Handling", [
        (91, "Error Categories", "Compile-time syntax errors, link errors, and runtime panics.", "Error Taxonomy", "Diagnostic Codes"),
        (92, "Try-Catch Blocks", "Intercepting exceptions gracefully using try and catch.", "Try-Catch Syntax", "Exception Interception"),
        (93, "Custom Exception Classes", "Defining domain-specific exception hierarchies.", "Custom Exceptions", "Exception Propagation"),
        (94, "Monadic Result Types", "Result<T, E> and Option<T> error handling patterns.", "Monadic Result", "Option Matching"),
        (95, "Unrecoverable Panics", "Panic assertions and stack trace dumps.", "Panic Statements", "Stack Trace Output"),
    ]),

    ("Part XX — Memory Management & Safety", [
        (96, "Stack Frame Allocation", "Automatic stack frame variable creation and destruction.", "Stack Frames", "Frame Pointer Cleanup"),
        (97, "Heap Dynamic Memory", "Allocating dynamic heap memory for complex objects.", "Heap Allocation", "Heap Pointer Management"),
        (98, "References & Borrowing", "Immutable and mutable references and borrow rules.", "Reference Borrowing", "Borrow Checker Rules"),
        (99, "Ownership & Move Semantics", "Scope-based ownership and resource drop rules.", "Ownership Transfer", "Automatic Drop Hooks"),
        (100, "Automatic Garbage Collection", "Reference counting and tracing garbage collector.", "ARC Garbage Collector", "Cycle Detection"),
    ]),

    ("Part XXI — Modules, Packages & Imports", [
        (101, "Module Design", "Organizing code into single-file modular units.", "Module Declaration", "Export Controls"),
        (102, "Import Statements", "Importing external modules via 'import module name'.", "Import Syntax", "Namespace Lookup"),
        (103, "Package Structure", "Multi-module package directory hierarchies.", "Package Directories", "Package Manifests"),
        (104, "Namespaces & Aliases", "Aliasing module imports and isolating global state.", "Namespace Isolation", "Import Aliases"),
        (105, "EPM Package Manager", "Installing and managing package dependencies via epm.json.", "EPM Registry", "Dependency Resolution"),
    ]),

    ("Part XXII — EnLang Standard Library Overview", [
        (106, "Standard Library Architecture", "Core module taxonomy and standard library organization.", "StdLib Overview", "Module Index"),
        (107, "String Utility Module", "Uppercase, lowercase, split, join, strip, and regex.", "String Utilities", "Text Processing"),
        (108, "Math & Statistics Module", "Trigonometric, logarithmic, and statistical functions.", "Math Functions", "Statistical Formulas"),
        (109, "Time & Date Module", "Timestamps, ISO date parsing, timezones, and stopwatches.", "Time Utilities", "Date Parsing"),
        (110, "Random & PRNG Module", "Random number generation, seeds, and distribution sampling.", "PRNG Generators", "Sampling Functions"),
    ]),

    ("Part XXIII — File System I/O & Formatting", [
        (111, "File Open & Close Semantics", "Opening file streams, modes, and automatic closure.", "File Stream Opening", "Stream Disposal"),
        (112, "Reading Text Files", "Reading full files, line-by-line streaming, and buffers.", "File Reading Verbs", "Line Iteration"),
        (113, "Writing Text Files", "Writing and appending text data to files.", "File Writing Verbs", "Append Modes"),
        (114, "JSON Parsing & Serialization", "Parsing JSON strings into dictionaries and serializing objects.", "JSON Parsing", "JSON Serialization"),
        (115, "CSV Data Stream Processing", "Parsing CSV files into structured rows and DataFrames.", "CSV Reader", "Header Mapping"),
    ]),

    ("Part XXIV — Networking Basics & Web Protocols", [
        (116, "Networking Concepts", "Sockets, TCP/IP, IP addresses, ports, and protocols.", "Networking Principles", "Socket Architecture"),
        (117, "HTTP GET & POST Requests", "Fetching remote REST endpoints via natural HTTP statements.", "HTTP Client Statements", "Status Code Handling"),
        (118, "Low-Level TCP Sockets", "Binding TCP listener sockets and stream data transmission.", "TCP Listeners", "Byte Stream Transmission"),
        (119, "UDP Datagram Streaming", "Sending and receiving low-latency UDP datagram packets.", "UDP Datagrams", "Packet Socket Binding"),
        (120, "Building REST Microservices", "Launching HTTP server endpoints with route handlers.", "REST Route Registration", "HTTP Server Engines"),
    ]),

    ("Part XXV — Concurrency, Threads & Async", [
        (121, "Concurrency Concepts", "Parallelism vs concurrency, OS threads, and event loops.", "Thread Principles", "Concurrency Models"),
        (122, "Spawning OS Threads", "Creating worker threads and executing parallel functions.", "Thread Spawning", "Worker Thread Pools"),
        (123, "Asynchronous Async & Await", "Non-blocking event loop execution via async and await.", "Async Functions", "Await Resolution"),
        (124, "Locks & Critical Sections", "Mutex locks and synchronization guards for shared state.", "Mutex Locks", "Critical Section Guards"),
        (125, "Thread Channels", "Safe inter-thread message passing channels.", "Channel Transmission", "Message Queue Buffers"),
    ]),

    ("Part XXVI — Automated Unit Testing & BDD", [
        (126, "Software Testing Principles", "Unit tests, integration tests, assertions, and test suites.", "Testing Frameworks", "Assertion Rules"),
        (127, "BDD Test Blocks in EnLang", "Writing BDD natural English test blocks and assertions.", "Natural Test Blocks", "Assertion Evaluation"),
        (128, "Running Test Suites", "Executing test runners via enlang check and test CLI.", "Test Runner CLI", "Test Output Reports"),
        (129, "Benchmarking Performance", "Profiling execution speed and memory allocations.", "Performance Benchmarking", "Timing Measurements"),
        (130, "Code Coverage & Diagnostics", "Measuring test coverage percentage across source files.", "Code Coverage Tools", "Coverage Reports"),
    ]),

    ("Part XXVII — Best Practices & Security", [
        (131, "Coding Style & Standards", "Official EnLang style guidelines, formatting, and indentation.", "Style Guidelines", "Formatting Engine"),
        (132, "Naming Conventions", "Variable, function, class, and package naming standards.", "Naming Standards", "Identifier Style"),
        (133, "Project Directory Layout", "Organizing multi-file commercial applications cleanly.", "Directory Structure", "Modular Design"),
        (134, "Security & Input Sanitization", "Preventing SQL injection, XSS, and unvalidated input.", "Security Auditing", "Input Sanitization"),
        (135, "Performance Optimization", "Optimizing loop bounds, memory caching, and vectorization.", "Optimization Techniques", "Vectorized Math"),
    ]),

    ("Part XXVIII — Step-by-Step Hands-on Tutorials", [
        (136, "Tutorial 1: Building a Student Grade Calculator", "Step-by-step tutorial building a grade calculation program.", "Grade Calculator Code", "Tutorial Walkthrough"),
        (137, "Tutorial 2: Building a Task Manager CLI App", "Building an interactive command-line todo task manager.", "Task Manager Code", "Interactive CLI"),
        (138, "Tutorial 3: Building a File Compression Utility", "Creating a system utility that compresses files into ZIP format.", "Compression Code", "System Utilities"),
        (139, "Tutorial 4: Building an HTTP Web API Service", "Creating a REST API service that serves JSON endpoints.", "REST API Code", "Web Server Demo"),
        (140, "Tutorial 5: Building a Multi-Threaded Worker Queue", "Designing a parallel task worker queue using thread channels.", "Worker Queue Code", "Concurrent Execution"),
    ]),

    ("Part XXIX — Language Reference & Specifications", [
        (141, "Keywords & Syntax Quick Sheet", "Comprehensive reference table of all language keywords.", "Keyword Table", "Syntax Matrix"),
        (142, "Operators & Symbol Reference", "Complete reference matrix of operators and natural equivalents.", "Operator Matrix", "Symbol Reference"),
        (143, "Standard Library API Index", "Alphabetical index of built-in functions and standard modules.", "StdLib Index", "API Function Signatures"),
        (144, "CLI Flags & Compiler Options", "Command line options, environment switches, and debug flags.", "CLI Flag Index", "Compiler Flags"),
        (145, "Compiler Error Codes Index", "Exhaustive table of error codes and resolution steps.", "Error Code Index", "Troubleshooting Guide"),
    ]),

    ("Part XXX — Appendices & Master Index", [
        (146, "Reserved Words Appendix", "Alphabetical list of reserved keywords.", "Reserved Words", "Keyword Appendix"),
        (147, "Version History & Changelog", "Changelog from v1.0.0 through v1.1.2.", "Version History", "Changelog Table"),
        (148, "Frequently Asked Questions (FAQ)", "Answers to 50 common questions about EnLang development.", "FAQ Database", "Troubleshooting FAQ"),
        (149, "Glossary of Technical Terms", "Definitions of language, compiler, and software engineering terms.", "Glossary A-Z", "Technical Dictionary"),
        (150, "Master Subject Index", "Complete alphabetical subject index covering all 150 chapters.", "Master Index", "150 Chapters Indexed"),
    ])
]

print(f"[INFO] PARTS_DATA loaded with {len(PARTS_DATA)} parts and 150 chapters.")
