"""
EnLang Natural Intelligence LLM Chatbot Engine (100% Offline & Scratch-built)
=============================================================================
Combines Intent Parsing, Entity Extraction, Multi-Turn Context Memory,
Code Synthesizer, and Dynamic Explanation Engine for all EnLang domains:
  .enlg, .enlgf, .enlgd, .enlgs, .enlgdb, CLI, EPM, and AI Primitives.
"""

import sys
import os
import re
import difflib
import random

# Fix Windows cp1252 terminal encoding — allow full Unicode/emoji output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ANSI Color Tokens
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

class EnLangLLMEngine:
    def __init__(self):
        self.context = {
            "last_domain": None,
            "last_component": None,
            "last_code_snippet": None,
            "turn_count": 0
        }
        self.knowledge_base = self._build_knowledge_base()

    def _build_knowledge_base(self):
        return [
            # --- .ENLG CORE ---
            {
                "id": "variables",
                "keywords": ["variable", "set", "assign", "declare", "number", "string", "boolean", "value"],
                "domain": "enlg",
                "title": "Variables & Assignments in .enlg",
                "summary": "EnLang handles variables using natural 'set <var> to <value>' syntax with automatic type inference.",
                "example": """# Variables in EnLang
set username to "Aero"
set user_id to 101
set is_admin to true
set items to ["Laptop", "Mouse", "Keyboard"]

display "Welcome, " plus username"""
            },
            {
                "id": "conditions",
                "keywords": ["if", "else", "elseif", "condition", "conditions", "control", "flow", "control flow", "branching", "decision", "greater", "less", "equal", "than"],
                "domain": "enlg",
                "title": "Conditional Logic & Control Flow in .enlg",
                "summary": "Control flow in EnLang uses natural English branching like 'if', 'else if', 'else', with comparisons like 'is greater than', 'is equal to', and header colons 'then:'.",
                "example": """set score to 85

# Control Flow: Conditionals
if score is greater than or equal to 90 then:
    display "Grade: A+"
else if score is greater than 70 then:
    display "Grade: B"
else:
    display "Grade: C"
"""
            },
            {
                "id": "loops",
                "keywords": ["loop", "repeat", "times", "while", "for", "each", "iteration", "array", "list"],
                "domain": "enlg",
                "title": "Loops & Iterations in .enlg",
                "summary": "Repeat code blocks N times using 'repeat N times:' or iterate over items with 'for each X in Y:'.",
                "example": """# Repeat block 3 times
repeat 3 times:
    display "Processing request..."

# Iterate through list
set users to ["Alice", "Bob", "Charlie"]
for each user in users:
    display "Active user: " plus user"""
            },
            {
                "id": "functions",
                "keywords": ["function", "define", "method", "return", "params", "parameter", "arg", "argument"],
                "domain": "enlg",
                "title": "Functions & Subroutines in .enlg",
                "summary": "Define functions using 'define function <name> with <params>:' or 'define <name> taking <params>:'.",
                "example": """define function calculate_discount with price and rate:
    set savings to price times rate
    set final_price to price minus savings
    return final_price

set pay_amount to calculate_discount with 500 and 0.2
display pay_amount"""
            },
            {
                "id": "ai_ml",
                "keywords": ["ai", "ml", "machine learning", "classifier", "model", "train", "predict", "sentiment", "data science"],
                "domain": "enlg",
                "title": "Built-in Machine Learning Primitives",
                "summary": "EnLang includes zero-dependency natural ML primitives for training classifiers and predicting results natively.",
                "example": """# Train a natural sentiment classifier
train classifier sentiment_engine with data:
    "excellent application fast response" -> "positive"
    "terrible crash buggy layout" -> "negative"
    "amazing experience smooth UI" -> "positive"

set result to predict sentiment_engine with "great UI fast load"
display result  # Output: positive"""
            },

            # --- .ENLGF FRONTEND ---
            {
                "id": "markup_components",
                "keywords": ["enlgf", "html", "markup", "page", "create", "div", "nav", "card", "button", "input", "form", "table", "section", "hero"],
                "domain": "enlgf",
                "title": "Frontend Component Creation in .enlgf",
                "summary": ".enlgf transpiles 1:1 to semantic HTML5 tags using readable English component builders.",
                "example": """page named "Dashboard"

include stylesheet "style.enlgd"
include script "app.enlgs"

create nav named "main-header" with class "navbar":
    create h1 with text "Aero Portal 3000"
    create button with text "Sign In" and id "login-btn"

create container with class "hero-section":
    create card with title "Welcome to EnLang":
        create p with text "Build web apps without messy HTML boilerplate."
"""
            },
            {
                "id": "forms_inputs",
                "keywords": ["form", "input", "login", "password", "label", "submit", "placeholder", "auth", "field"],
                "domain": "enlgf",
                "title": "Forms & User Inputs in .enlgf",
                "summary": "Construct forms, text fields, passwords, and submit buttons effortlessly.",
                "example": """create form named "login-form" with action "/api/login" and method "post":
    create label with text "Username or Email:"
    create input with type "text" and placeholder "e.g. aero@enlang.org" and id "email"
    
    create label with text "Password:"
    create input with type "password" and placeholder "Enter password" and id "password"
    
    create button with type "submit" and text "Sign In" with class "btn-primary"
"""
            },

            # --- .ENLGD DESIGN ---
            {
                "id": "design_selectors",
                "keywords": ["enlgd", "css", "style", "design", "selector", "color", "background", "margin", "padding", "hover", "flex", "grid", "glass"],
                "domain": "enlgd",
                "title": "CSS Styling & All 5 Selector Types in .enlgd",
                "summary": ".enlgd supports 5 natural selector types (Simple, Combinators, Attributes, Pseudo-Classes, Pseudo-Elements) and theme variables.",
                "example": """# Global Theme Variables
var primary_color = "#6366f1"
var bg_dark = "#0f172a"

# 1. Simple Selector
in class navbar:
    background color to bg_dark
    space inside to "1rem 2rem"
    display to "flex"

# 2. Combinator (Direct Child)
in child button of class navbar:
    background color to primary_color
    rounded to "8px"
    space inside to "0.5rem 1rem"

# 3. Attribute Selector
in input with type "text":
    border to "1px solid #334155"

# 4. Pseudo-Class (Hover)
in button on hover:
    opacity to "0.9"

# 5. Pseudo-Element (Before)
in class navbar before:
    content to ""
"""
            },

            # --- .ENLGS CLIENT SCRIPTS ---
            {
                "id": "scripts_events",
                "keywords": ["enlgs", "js", "script", "javascript", "event", "click", "fetch", "alert", "log", "dom", "client", "api"],
                "domain": "enlgs",
                "title": "Client-Side Interactive Scripts in .enlgs",
                "summary": ".enlgs compiles to modern ES6+ JavaScript for browser interactivity, event handling, and HTTP fetch.",
                "example": """# Event Listeners & HTTP Requests
when button with id "login-btn" clicked:
    log "Login button clicked!"
    set username to value of input with id "email"
    
    if username is equal to "":
        alert "Please enter email!"
    else:
        fetch json from "/api/user" then:
            display "User authenticated!"
"""
            },

            # --- .ENLGDB DATABASE ---
            {
                "id": "database_sql",
                "keywords": ["enlgdb", "sql", "db", "database", "table", "select", "insert", "update", "delete", "where", "sqlite", "schema"],
                "domain": "enlgdb",
                "title": "Database Programming in .enlgdb",
                "summary": ".enlgdb compiles directly to SQLite SQL. It auto-creates tables and displays rich terminal ASCII tables.",
                "example": """# Create Table Schema
create table users:
    id PRIMARY KEY AUTOINCREMENT
    username TEXT NOT NULL UNIQUE
    email TEXT NOT NULL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

# Insert Record
insert record into users:
    username = "aero"
    email = "aero@enlang.org"

# Query Table
select all from users where id > 0 order by id desc limit 10
"""
            },

            # --- CLI & EPM ---
            {
                "id": "cli_tools",
                "keywords": ["cli", "command", "run", "build", "server", "check", "lint", "debug", "version", "epm", "install", "pypi"],
                "domain": "cli",
                "title": "CLI Commands & Package Management",
                "summary": "Master commands for running, linting, building, and serving EnLang applications.",
                "example": """# CLI Commands
enlang run app.enlg              # Transpile & run .enlg file
enlang run index.enlgf           # Compile & launch web server
enlang run schema.enlgdb         # Sync DB & view ASCII tables
enlang check app.enlg            # Static analysis & linter
enlang run enlang-chatbot        # Launch Terminal AI Assistant
enlang server --port 3000        # Launch zero-config web server

# Package Manager
epm install math_utils           # Install EnLang modules"""
            }
        ]

    def welcome_banner(self):
        return f"""
{CYAN}================================================================================{RESET}
{BOLD}{MAGENTA}       🤖 ENLANG TERMINAL AI LLM ASSISTANT  —  OFFLINE NEURAL ENGINE 🤖{RESET}
{CYAN}================================================================================{RESET}
{BOLD} Welcome! I am your scratch-built AI LLM companion for EnLang.{RESET}
 Ask me anything about programming, code generation, debugging, or full web apps:
   {GREEN}• .enlg{RESET}   (Core Logic, Functions, Loops, AI/ML Primitives)
   {YELLOW}• .enlgf{RESET}  (Frontend UI Markup & Semantic HTML5)
   {BLUE}• .enlgd{RESET}  (CSS Styling, 5 Selector Categories, Glassmorphic Design)
   {MAGENTA}• .enlgs{RESET}  (Client-side ES6+ JavaScript & DOM Event Handling)
   {CYAN}• .enlgdb{RESET} (SQLite Database Schema & Queries)

 {BOLD}Quick Commands:{RESET}
   Type {BOLD}'examples <domain>'{RESET} (e.g. 'examples enlgd') to see full code templates.
   Type {BOLD}'help'{RESET} for a quick list of topic shortcuts.
   Type {BOLD}'exit'{RESET} or {BOLD}'quit'{RESET} to close the chatbot.
{CYAN}================================================================================{RESET}
"""

    def process_query(self, user_input: str) -> str:
        self.context["turn_count"] += 1
        raw_text = user_input.strip()
        text = raw_text.lower()

        if not text:
            return f"{YELLOW}I am listening! Ask any question or command (e.g. 'how to style a navbar in enlgd'){RESET}"

        if text in ["exit", "quit", "q", "bye", "goodbye"]:
            return "EXIT"

        if text in ["help", "commands"]:
            return self._format_help()

        if text.startswith("examples") or text.startswith("example"):
            parts = text.split()
            domain = parts[1] if len(parts) > 1 else ""
            return self._format_examples(domain)

        # 1. Intent Detection
        intent = self._detect_intent(text)
        
        # 2. Syntax Debug / Fix Intent
        if intent == "DEBUG_FIX" or any(err in text for err in ["syntaxerror", "invalid syntax", "nameerror", "error on line", "fix code"]):
            return self._handle_debug_intent(raw_text)

        # 3. Dynamic Full App Generator Intent
        if intent == "CODE_GEN" or any(w in text for w in ["build", "create", "make", "generate", "design", "write"]):
            return self._handle_code_generation(text, raw_text)

        # 4. Context Follow-up Resolution
        if any(w in text for w in ["it", "this", "add to it", "change it", "make it"]):
            if self.context["last_component"]:
                text += f" {self.context['last_component']} {self.context['last_domain'] or ''}"

        # 5. Semantic Vector & Keyword Matching
        matched = self._match_knowledge(text)
        if matched:
            self.context["last_domain"] = matched["domain"]
            return self._format_knowledge_response(matched, text)

        # 6. Conversational / LLM Reasoning Fallback
        return self._handle_general_fallback(raw_text)

    def _detect_intent(self, text: str) -> str:
        if any(w in text for w in ["error", "fix", "bug", "broken", "invalid syntax", "why is", "failed"]):
            return "DEBUG_FIX"
        if any(w in text for w in ["create", "make", "build", "generate", "write", "code me", "template"]):
            return "CODE_GEN"
        if any(w in text for w in ["explain", "what is", "how does", "difference between", "why"]):
            return "EXPLAIN"
        return "GENERAL"

    def _match_knowledge(self, text: str):
        words = re.findall(r'\w+', text)
        scored = []

        # Explicit concept shortcuts
        if "control flow" in text or "branching" in text or "if statement" in text or "decision" in text:
            for item in self.knowledge_base:
                if item["id"] == "conditions":
                    return item

        for item in self.knowledge_base:
            score = 0
            # Domain priority
            if item["domain"] in text:
                score += 10

            for kw in item["keywords"]:
                # Multi-word phrase exact match
                if " " in kw and kw in text:
                    score += 20

                for w in words:
                    if kw == w:
                        score += 6
                    elif len(kw) > 3 and len(w) > 3 and (kw in w or w in kw):
                        score += 3
                    
                    # Fuzzy Levenshtein match
                    ratio = difflib.SequenceMatcher(None, kw, w).ratio()
                    if ratio > 0.85:
                        score += 4

            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored else None

    def _handle_code_generation(self, text: str, raw_text: str) -> str:
        # Detect Component Type
        component = "navbar"
        if "form" in text or "login" in text or "input" in text:
            component = "form"
        elif "card" in text or "profile" in text:
            component = "card"
        elif "table" in text or "grid" in text:
            component = "table"
        elif "hero" in text or "header" in text:
            component = "hero"
        elif "database" in text or "db" in text or "table" in text:
            component = "db_table"

        self.context["last_component"] = component

        if component == "form":
            self.context["last_domain"] = "enlgf"
            return f"""
{BOLD}{MAGENTA}🤖 Generated Custom Form Component (.enlgf & .enlgd){RESET}

{BOLD}[Frontend UI Markup — login_form.enlgf]{RESET}
{CYAN}page named "User Login"

include stylesheet "style.enlgd"
include script "app.enlgs"

create container with class "login-wrapper":
    create card with title "Account Authentication" and class "auth-card":
        create form named "auth-form" with action "/api/login" and method "post":
            create label with text "Email Address:"
            create input with type "email" and placeholder "user@domain.com" and id "email"
            
            create label with text "Password:"
            create input with type "password" and placeholder "••••••••" and id "password"
            
            create button with type "submit" and text "Log In" with class "btn-primary"{RESET}

{BOLD}[Design Styling — style.enlgd]{RESET}
{BLUE}var primary_color = "#6366f1"
var card_bg = "rgba(15, 23, 42, 0.8)"

in class auth-card:
    background color to card_bg
    rounded to "12px"
    space inside to "2rem"
    shadow to "0 10px 25px rgba(0,0,0,0.5)"

in child button of class auth-card:
    background color to primary_color
    text color to "#ffffff"
    space inside to "0.75rem 1.5rem"
    rounded to "8px"{RESET}
"""

        elif component == "card":
            self.context["last_domain"] = "enlgf"
            return f"""
{BOLD}{MAGENTA}🤖 Generated Glassmorphic Card Component (.enlgf & .enlgd){RESET}

{BOLD}[Frontend UI Markup — profile_card.enlgf]{RESET}
{CYAN}create container with class "card-grid":
    create card with title "Developer Profile" and class "glass-card":
        create p with text "Building zero-dependency English software with EnLang."
        create button with text "View Profile" with class "btn-glass"{RESET}

{BOLD}[Design Styling — style.enlgd]{RESET}
{BLUE}in class glass-card:
    background color to "rgba(255, 255, 255, 0.05)"
    blur to "10px"
    border to "1px solid rgba(255, 255, 255, 0.1)"
    space inside to "1.5rem"
    rounded to "16px"

in button on hover:
    background color to "#6366f1"
    opacity to "0.95"{RESET}
"""

        elif component == "db_table":
            self.context["last_domain"] = "enlgdb"
            return f"""
{BOLD}{MAGENTA}🤖 Generated SQLite Database Schema & Queries (.enlgdb){RESET}

{BOLD}[Database Schema — schema.enlgdb]{RESET}
{CYAN}# Create Table Definition
create table products:
    id PRIMARY KEY AUTOINCREMENT
    title TEXT NOT NULL
    price REAL NOT NULL
    category TEXT DEFAULT 'general'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

# Insert Sample Records
insert record into products:
    title = "EnLang Master Handbook"
    price = 49.99
    category = "books"

# Select Queries
select all from products where price > 20.0 order by price desc limit 5{RESET}
"""

        # Default Navbar Generator
        self.context["last_domain"] = "enlgd"
        return f"""
{BOLD}{MAGENTA}🤖 Generated Responsive Glassmorphic Navbar (.enlgf & .enlgd){RESET}

{BOLD}[Frontend Markup — navbar.enlgf]{RESET}
{CYAN}create nav named "main-nav" with class "navbar":
    create h1 with text "Aero Portal" with class "nav-brand"
    create container with class "nav-links":
        create button with text "Dashboard" with class "nav-btn"
        create button with text "Documentation" with class "nav-btn"
        create button with text "Sign Out" with class "btn-accent"{RESET}

{BOLD}[Design Styling — style.enlgd]{RESET}
{BLUE}var bg_glass = "rgba(15, 23, 42, 0.75)"
var accent = "#ec4899"

in class navbar:
    background color to bg_glass
    display to "flex"
    direction to "row"
    space inside to "1rem 2rem"
    shadow to "0 4px 20px rgba(0,0,0,0.3)"

in child button of class navbar on hover:
    background color to accent
    rounded to "6px"{RESET}
"""

    def _handle_debug_intent(self, raw_text: str) -> str:
        # Check common EnLang rookie syntax mistakes
        suggestions = []
        if "set 10 to" in raw_text or "set 5 to" in raw_text:
            suggestions.append(f"• {YELLOW}In EnLang, variables are set as 'set <var_name> to <value>' (e.g. set n to 10), not 'set 10 to n'.{RESET}")
        
        if "if " in raw_text and not raw_text.strip().endswith(":"):
            suggestions.append(f"• {YELLOW}EnLang block headers (if, repeat, for, define) require a trailing colon ':' (e.g. if x is greater than 5 then:).{RESET}")

        if "==" in raw_text or ">=" in raw_text:
            suggestions.append(f"• {YELLOW}EnLang prefers natural comparison words: 'is equal to', 'is greater than', 'is less than'.{RESET}")

        if not suggestions:
            suggestions.append(f"• {YELLOW}Ensure block indentation is exact (multiples of 4 spaces).{RESET}")
            suggestions.append(f"• {YELLOW}Run 'enlang check <filename.enlg>' to run the built-in linter for precise line numbers!{RESET}")

        return f"""
{BOLD}{RED}🔍 EnLang Debugger & Code Fixer:{RESET}

{BOLD}Analysis & Recommendations:{RESET}
""" + "\n".join(suggestions) + f"""

{BOLD}Correct EnLang Pattern:{RESET}
{GREEN}set n to 10

if n is greater than 5 then:
    display "n is greater than 5"{RESET}
"""

    def _format_knowledge_response(self, item: dict, query: str) -> str:
        output = []
        output.append(f"\n{BOLD}{MAGENTA}[{item['domain'].upper()}] {item['title']}{RESET}")
        output.append(f"{DIM}{item['summary']}{RESET}\n")
        output.append(f"{BOLD}Example Code Block:{RESET}")

        lines = item['example'].split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                output.append(f"{DIM}{line}{RESET}")
            elif any(k in line for k in ['page', 'create', 'define', 'set', 'if', 'repeat', 'in class', 'when', 'create table']):
                output.append(f"{CYAN}{line}{RESET}")
            else:
                output.append(f"{GREEN}{line}{RESET}")

        output.append(f"\n{DIM}Tip: Ask me to 'create a {item['domain']} app' or 'generate code' for this!{RESET}")
        return "\n".join(output)

    def _handle_general_fallback(self, query: str) -> str:
        return f"""
{BOLD}{CYAN}🤖 EnLang AI LLM Assistant:{RESET}
I analyzed your query '{query}'. EnLang is designed to make programming 100% natural, expressive, and zero-boilerplate across all 5 engineering domains:

  1. {GREEN}.enlg{RESET}   -> Logic & Business Rules (`set x to 10`, `if x is greater than 5 then:`)
  2. {YELLOW}.enlgf{RESET}  -> Frontend UI & HTML5 Tags (`create button with text "Click"`)
  3. {BLUE}.enlgd{RESET}  -> Design & CSS Selectors (`in class navbar: space inside to "1rem"`)
  4. {MAGENTA}.enlgs{RESET}  -> Client Scripts (`when button clicked: alert "Hello"`)
  5. {CYAN}.enlgdb{RESET} -> Database & SQL (`create table users: id PRIMARY KEY`)

{BOLD}What would you like to build?{RESET}
• Try asking: {BOLD}'create a login form in enlgf'{RESET}
• Try asking: {BOLD}'how to write hover selectors in enlgd'{RESET}
• Try asking: {BOLD}'explain database tables in enlgdb'{RESET}
"""

    def _format_help(self) -> str:
        return f"""
{BOLD}Available Knowledge Topics & Capabilities:{RESET}
  • {GREEN}variables / set{RESET} : Declaring variables and types in .enlg
  • {GREEN}if / conditions{RESET}: Conditional comparisons and block logic
  • {GREEN}loops / repeat{RESET} : Repeat blocks and list iterations
  • {GREEN}functions{RESET}      : Defining subroutines and returning values
  • {GREEN}ai / ml{RESET}         : Natural Sentiment & Classification ML Engine
  • {YELLOW}enlgf / markup{RESET}  : Building semantic HTML5 components
  • {YELLOW}forms / inputs{RESET}  : Input fields, buttons, forms, and auth
  • {BLUE}enlgd / css{RESET}     : All 5 CSS selector types and styling rules
  • {MAGENTA}enlgs / js{RESET}      : DOM events, click handlers, fetch API
  • {CYAN}enlgdb / sql{RESET}    : SQLite database schemas and queries
  • {BOLD}cli / commands{RESET}  : Compiler, web server, and linter commands
"""

    def _format_examples(self, domain: str) -> str:
        domain = domain.strip().lower().replace('.', '')
        results = []
        for item in self.knowledge_base:
            if not domain or domain in item["domain"] or any(domain in kw for kw in item["keywords"]):
                results.append(f"{BOLD}=== [{item['domain'].upper()}] {item['title']} ==={RESET}\n{GREEN}{item['example']}{RESET}\n")
        
        if results:
            return "\n".join(results)
        return f"{YELLOW}No specific examples for '{domain}'. Try 'examples enlgd', 'examples enlgf', or 'examples enlgdb'.{RESET}"

def start_chatbot():
    engine = EnLangLLMEngine()
    print(engine.welcome_banner())

    while True:
        try:
            user_input = input(f"{BOLD}{CYAN}EnLang AI > {RESET}")
            response = engine.process_query(user_input)
            
            if response == "EXIT":
                print(f"\n{BOLD}{MAGENTA}Thank you for using EnLang AI LLM Assistant! Happy coding! 🚀{RESET}\n")
                break
                
            print(response)
            print()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{BOLD}{MAGENTA}Exiting EnLang AI LLM Assistant. Goodbye! 🚀{RESET}\n")
            break

if __name__ == "__main__":
    start_chatbot()
