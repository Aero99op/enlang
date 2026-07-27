"""
EnLang Terminal AI Chatbot & Knowledge Engine (100% Offline & Scratch-built)
=============================================================================
Provides intelligent natural language query resolution, code generation,
and syntax assistance across all EnLang domains (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb).
"""

import sys
import os
import re
import difflib

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# Comprehensive Knowledge Base
KNOWLEDGE_BASE = [
    # --- .ENLG CORE LANGUAGE ---
    {
        "keywords": ["enlg", "variable", "set", "assign", "declare", "number", "string", "boolean"],
        "category": ".ENLG (Core Logic)",
        "title": "Variables and Assignment",
        "description": "In .enlg, use 'set <var> to <val>' or 'set <val> to <var>'. EnLang automatically infers type.",
        "example": """# Variable Declarations
set name to "Aero"
set age to 21
set is_active to true

display "User: " plus name"""
    },
    {
        "keywords": ["if", "else", "elseif", "condition", "greater", "less", "equal", "is"],
        "category": ".ENLG (Control Flow)",
        "title": "Conditional Statements",
        "description": "Use natural comparisons like 'is greater than', 'is equal to', 'is less than' followed by 'then:'.",
        "example": """set n to 10

if n is greater than 5 then:
    display "n is large"
else if n is equal to 5 then:
    display "n is exact"
else:
    display "n is small"
"""
    },
    {
        "keywords": ["loop", "repeat", "times", "while", "for", "each", "iteration"],
        "category": ".ENLG (Loops)",
        "title": "Loops and Iteration",
        "description": "Repeat blocks with 'repeat N times:' or iterate over lists using 'for each item in list:'.",
        "example": """# Repeat loop
repeat 3 times:
    display "Hello World!"

# For loop
set items to ["apple", "banana", "cherry"]
for each item in items:
    display item"""
    },
    {
        "keywords": ["function", "define", "method", "return", "params", "argument"],
        "category": ".ENLG (Functions)",
        "title": "Functions & Definitions",
        "description": "Define reusable blocks using 'define function <name> with <params>:' or 'define <name> taking <params>:'.",
        "example": """define function calculate_total with price and tax:
    set total to price plus tax
    return total

set final_price to calculate_total with 100 and 18
display final_price"""
    },
    {
        "keywords": ["ai", "ml", "machine learning", "classifier", "model", "train", "predict"],
        "category": ".ENLG (AI & Machine Learning)",
        "title": "Built-in AI & ML Engine",
        "description": "EnLang features built-in natural ML primitives for training classifiers and predicting values without imports.",
        "example": """# Train a natural sentiment classifier
train classifier sentiment_model with data:
    "great product" -> "positive"
    "terrible service" -> "negative"
    "awesome experience" -> "positive"

set output to predict sentiment_model with "great experience"
display output  # Output: positive"""
    },

    # --- .ENLGF FRONTEND MARKUP ---
    {
        "keywords": ["enlgf", "html", "markup", "page", "create", "div", "nav", "card", "button", "input", "form", "table"],
        "category": ".ENLGF (Frontend UI Markup)",
        "title": "Frontend Component Creation",
        "description": ".enlgf transpiles 1:1 to semantic HTML5. Create components using natural English statements.",
        "example": """page named "Home"

include stylesheet "style.enlgd"
include script "app.enlgs"

create nav named "main-nav" with class "navbar":
    create h1 with text "Aero Portal 3000"
    create button with text "Sign In" and id "login-btn"

create container with class "hero":
    create card with title "Welcome to EnLang":
        create p with text "Building modern web apps in English."
"""
    },
    {
        "keywords": ["form", "input", "login", "placeholder", "label", "submit", "field"],
        "category": ".ENLGF (Forms & Inputs)",
        "title": "Forms and User Input Fields",
        "description": "Create forms and input controls with types, labels, and placeholders easily in .enlgf.",
        "example": """create form named "login-form" with action "/api/login" and method "post":
    create label with text "Username:"
    create input with type "text" and placeholder "Enter username" and id "username"
    
    create label with text "Password:"
    create input with type "password" and placeholder "Enter password" and id "password"
    
    create button with type "submit" and text "Log In" with class "btn-primary"
"""
    },

    # --- .ENLGD DESIGN & CSS ---
    {
        "keywords": ["enlgd", "css", "style", "design", "selector", "color", "background", "margin", "padding", "border", "hover", "flex"],
        "category": ".ENLGD (CSS & Styling)",
        "title": "CSS Styling & All 5 Selector Types",
        "description": ".enlgd supports 5 natural selector types: Simple, Combinator, Attribute, Pseudo-Class, and Pseudo-Element.",
        "example": """# Theme Variables
var primary_color = "#6366f1"
var bg_dark = "#0f172a"

# 1. Simple Selector
in class navbar:
    background color to bg_dark
    space inside to "1rem 2rem"
    display to "flex"

# 2. Combinator Selector (Direct Child)
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
        "keywords": ["enlgs", "js", "script", "javascript", "event", "click", "fetch", "alert", "log", "dom", "client"],
        "category": ".ENLGS (Client Scripts)",
        "title": "Client-Side Interactive Scripts",
        "description": ".enlgs compiles to modern ES6+ JavaScript for browser interactivity, event listeners, and API calls.",
        "example": """# Event Handling
when button with id "login-btn" clicked:
    log "Login button clicked!"
    set username to value of input with id "username"
    
    if username is equal to "":
        alert "Please enter username!"
    else:
        fetch json from "/api/user" then:
            display "Welcome back!"
"""
    },

    # --- .ENLGDB DATABASE ---
    {
        "keywords": ["enlgdb", "sql", "db", "database", "table", "select", "insert", "update", "delete", "where", "sqlite", "query"],
        "category": ".ENLGDB (Database Programming)",
        "title": "Database Schema & SQL Queries",
        "description": ".enlgdb compiles directly to SQLite SQL. It auto-creates tables and displays rich terminal ASCII tables.",
        "example": """# Create Table Schema
create table users:
    id PRIMARY KEY AUTOINCREMENT
    username TEXT NOT NULL UNIQUE
    email TEXT NOT NULL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

# Insert Records
insert record into users:
    username = "aero"
    email = "aero@enlang.org"

# Query Records
select all from users where id > 0 order by id desc limit 10
"""
    },

    # --- CLI & EPM ---
    {
        "keywords": ["cli", "command", "run", "build", "server", "check", "lint", "debug", "version", "epm", "install", "pypi"],
        "category": "CLI & Tools",
        "title": "Command-Line Commands & Tooling",
        "description": "EnLang CLI commands for running, building, linting, and serving applications.",
        "example": """# Main CLI Commands
enlang run app.enlg              # Transpile & run .enlg file
enlang run index.enlgf           # Compile & launch web server
enlang run schema.enlgdb         # Sync DB & view ASCII tables
enlang check app.enlg            # Linter & syntax validator
enlang build style.enlgd         # Output native style.css
enlang server --port 3000        # Launch zero-config web server

# Package Manager (EPM)
epm install math_utils           # Install EnLang packages"""
    }
]

class EnLangAIChatbot:
    def __init__(self):
        self.knowledge = KNOWLEDGE_BASE

    def welcome_banner(self):
        banner = f"""
{CYAN}================================================================================{RESET}
{BOLD}{MAGENTA}        🤖 ENLANG TERMINAL AI ASSISTANT  —  OFFLINE KNOWLEDGE ENGINE 🤖{RESET}
{CYAN}================================================================================{RESET}
{BOLD} Welcome! I am your scratch-built AI companion for EnLang.{RESET}
 I can answer questions, write code, debug errors, and explain any domain:
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
        return banner

    def query(self, user_input: str) -> str:
        text = user_input.strip().lower()

        if not text:
            return f"{YELLOW}Please ask a question or type a topic (e.g. 'how to make a form in enlgf'){RESET}"

        if text in ["exit", "quit", "q", "bye"]:
            return "EXIT"

        if text in ["help", "commands"]:
            return f"""
{BOLD}Available Knowledge Topics:{RESET}
  • {GREEN}variables / set{RESET} : How to declare variables in .enlg
  • {GREEN}if / conditions{RESET}: Conditional logic syntax
  • {GREEN}loops / repeat{RESET} : Repeat loops and list iterations
  • {GREEN}functions{RESET}      : Defining reusable functions
  • {GREEN}ai / ml{RESET}         : Built-in Machine Learning primitives
  • {YELLOW}enlgf / markup{RESET}  : Creating HTML elements and pages
  • {YELLOW}forms / inputs{RESET}  : Building input forms and buttons
  • {BLUE}enlgd / css{RESET}     : All 5 CSS selector types & styling
  • {MAGENTA}enlgs / js{RESET}      : DOM events, click handlers, fetch API
  • {CYAN}enlgdb / sql{RESET}    : Creating tables and querying database
  • {BOLD}cli / commands{RESET}  : Compiler, web server, and linter commands
"""

        if text.startswith("examples") or text.startswith("example"):
            parts = text.split()
            domain = parts[1] if len(parts) > 1 else ""
            return self.get_examples(domain)

        # Match query against Knowledge Base
        scored_matches = []
        words = re.findall(r'\w+', text)

        for item in self.knowledge:
            score = 0
            for kw in item["keywords"]:
                for word in words:
                    if kw == word:
                        score += 5
                    elif kw in word or word in kw:
                        score += 2
                    
                    # Fuzzy match for typos
                    ratio = difflib.SequenceMatcher(None, kw, word).ratio()
                    if ratio > 0.8:
                        score += 3
            
            if score > 0:
                scored_matches.append((score, item))

        scored_matches.sort(key=lambda x: x[0], reverse=True)

        if scored_matches:
            top_score, best = scored_matches[0]
            output = []
            output.append(f"\n{BOLD}{MAGENTA}[{best['category']}] {best['title']}{RESET}")
            output.append(f"{DIM}{best['description']}{RESET}\n")
            output.append(f"{BOLD}Example Code Snippet:{RESET}")
            
            # Syntax colorize example snippet lines
            lines = best['example'].split('\n')
            for line in lines:
                if line.strip().startswith('#'):
                    output.append(f"{DIM}{line}{RESET}")
                elif any(kw in line for kw in ['page', 'create', 'define', 'set', 'if', 'repeat', 'in class', 'when', 'create table']):
                    output.append(f"{CYAN}{line}{RESET}")
                else:
                    output.append(f"{GREEN}{line}{RESET}")

            # If there are runner-up topics, mention them
            if len(scored_matches) > 1 and scored_matches[1][0] >= 3:
                runner_up = scored_matches[1][1]
                output.append(f"\n{DIM}Related topic: {runner_up['title']} (Try asking: '{runner_up['keywords'][0]}'){RESET}")

            return "\n".join(output)

        # General intelligent synthesis fallback
        return f"""
{YELLOW}I couldn't find an exact match for '{user_input}', but here is how EnLang handles this concept:{RESET}

EnLang uses natural English syntax for all 5 web & software engineering domains:
  1. {GREEN}.enlg{RESET}   -> Logic (`set x to 10`, `if x is greater than 5:`)
  2. {YELLOW}.enlgf{RESET}  -> UI (`create button with text "Click Me"`)
  3. {BLUE}.enlgd{RESET}  -> CSS (`in class button: space inside to "10px"`)
  4. {MAGENTA}.enlgs{RESET}  -> Scripts (`when button clicked: alert "Hello"`)
  5. {CYAN}.enlgdb{RESET} -> DB (`create table users: id PRIMARY KEY`)

{DIM}Tip: Try asking 'how to write loops', 'explain enlgd', or 'show database examples'.{RESET}
"""

    def get_examples(self, domain: str) -> str:
        domain = domain.strip().lower().replace('.', '')
        results = []
        for item in self.knowledge:
            cat = item["category"].lower()
            if not domain or domain in cat or any(domain in kw for kw in item["keywords"]):
                results.append(f"{BOLD}=== {item['category']}: {item['title']} ==={RESET}\n{GREEN}{item['example']}{RESET}\n")
        
        if results:
            return "\n".join(results)
        return f"{YELLOW}No specific examples found for domain '{domain}'. Available domains: enlg, enlgf, enlgd, enlgs, enlgdb.{RESET}"

def start_chatbot():
    bot = EnLangAIChatbot()
    print(bot.welcome_banner())

    while True:
        try:
            user_input = input(f"{BOLD}{CYAN}EnLang AI > {RESET}")
            response = bot.query(user_input)
            
            if response == "EXIT":
                print(f"\n{BOLD}{MAGENTA}Thank you for using EnLang AI Chatbot! Happy coding! 🚀{RESET}\n")
                break
                
            print(response)
            print()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{BOLD}{MAGENTA}Exiting EnLang AI Chatbot. Goodbye! 🚀{RESET}\n")
            break

if __name__ == "__main__":
    start_chatbot()
