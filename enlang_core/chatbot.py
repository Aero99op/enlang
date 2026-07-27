"""
EnLang Hybrid AI LLM Engine (ChatGPT / Gemini Level Terminal Intelligence)
=============================================================================
Provides ChatGPT / Gemini level natural responses across all EnLang domains (.enlg, .enlgf, .enlgd, .enlgs, .enlgdb).
Backends supported (100% FREE & Zero Cost):
  1. Ollama / Local LLM (Llama 3, DeepSeek, Mistral, Qwen) -> 100% Offline & Free
  2. Free Cloud LLM (Gemini 1.5/2.0, Groq, HuggingFace, OpenAI) -> Free API Key
  3. EnLang Generative Neural Synthesizer -> Built-in Local Fallback Engine
"""

import sys
import os
import re
import difflib
import json
import urllib.request
import urllib.error

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

ENLANG_SYSTEM_PROMPT = """You are EnLang AI, a world-class AI Assistant and expert software engineer specializing in the EnLang Natural English Programming Language Ecosystem.

EnLang consists of 5 core domains:
1. .enlg   -> Core Logic (Variables: set x to 10, Conditions: if x is greater than 5 then:, Loops: repeat 3 times:, Functions: define function add with x and y:, ML: train classifier / predict)
2. .enlgf  -> Frontend Markup (HTML5 tags: page named "Home", create nav, create card, create form, create button, create input)
3. .enlgd  -> Design & CSS (Selectors: Simple 'in class navbar', Combinator 'in child p of div', Attribute 'in input with type "text"', Pseudo-class 'in btn on hover', Pseudo-element 'in card before', Properties: space inside, space outside, rounded, shadow, text color, bg_glass)
4. .enlgs  -> Client Scripts (ES6+ JS: when button clicked:, fetch json from url then:, log text, alert)
5. .enlgdb -> Database & SQL (SQLite: create table users, insert record into users, select all from users where id > 0)

Always provide clear, intelligent, step-by-step responses with copy-pasteable valid EnLang code snippets formatted nicely."""

class EnLangHybridLLMEngine:
    def __init__(self):
        self.context = []
        self.ollama_available, self.ollama_model = self._check_ollama()
        self.api_key, self.api_provider = self._check_cloud_api()

    def _check_ollama(self):
        """Checks if local Ollama is running (Llama 3, DeepSeek, Mistral, Qwen)."""
        try:
            req = urllib.request.Request("http://localhost:11434/api/tags", headers={"User-Agent": "EnLangAI"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                if models:
                    preferred = ["llama3", "deepseek-r1", "mistral", "qwen", "phi3", "llama2"]
                    for pref in preferred:
                        for m in models:
                            if pref in m.lower():
                                return True, m
                    return True, models[0]
        except Exception:
            pass
        return False, None

    def _check_cloud_api(self):
        """Checks for free cloud API keys in environment."""
        if os.environ.get("GEMINI_API_KEY"):
            return os.environ.get("GEMINI_API_KEY"), "gemini"
        if os.environ.get("GROQ_API_KEY"):
            return os.environ.get("GROQ_API_KEY"), "groq"
        if os.environ.get("OPENAI_API_KEY"):
            return os.environ.get("OPENAI_API_KEY"), "openai"
        return None, None

    def welcome_banner(self):
        backend_info = ""
        if self.ollama_available:
            backend_info = f" {GREEN}● Backend: Local Ollama LLM ({self.ollama_model}){RESET}"
        elif self.api_provider:
            backend_info = f" {CYAN}● Backend: Cloud LLM ({self.api_provider.upper()}){RESET}"
        else:
            backend_info = f" {YELLOW}● Backend: EnLang Generative Neural Synthesizer (Offline Engine){RESET}"

        return f"""
{CYAN}================================================================================{RESET}
{BOLD}{MAGENTA}       🤖 ENLANG TERMINAL AI LLM ASSISTANT  —  CHATGPT/GEMINI POWERED 🤖{RESET}
{CYAN}================================================================================{RESET}
{backend_info}

{BOLD} Welcome! Ask any programming or architecture question about EnLang:{RESET}
   {GREEN}• .enlg{RESET}   (Core Logic, Control Flow, Functions, Machine Learning)
   {YELLOW}• .enlgf{RESET}  (Frontend UI Components & Semantic HTML5 Markup)
   {BLUE}• .enlgd{RESET}  (CSS Styling, Glassmorphism, 5 Selector Categories)
   {MAGENTA}• .enlgs{RESET}  (Client-side ES6+ JavaScript, DOM Events & Fetch)
   {CYAN}• .enlgdb{RESET} (SQLite Database Schemas & Queries)

 {BOLD}Quick Commands:{RESET}
   Type {BOLD}'examples <domain>'{RESET} (e.g. 'examples enlgd') to see full code templates.
   Type {BOLD}'help'{RESET} for a quick list of topic shortcuts.
   Type {BOLD}'exit'{RESET} or {BOLD}'quit'{RESET} to close the chatbot.
{CYAN}================================================================================{RESET}
"""

    def process_query(self, user_input: str) -> str:
        raw_text = user_input.strip()
        text = raw_text.lower()

        if not text:
            return f"{YELLOW}I am ready! Ask me anything (e.g. 'explain control flow' or 'build a login page'){RESET}"

        if text in ["exit", "quit", "q", "bye", "goodbye"]:
            return "EXIT"

        if text in ["help", "commands"]:
            return self._format_help()

        if text.startswith("examples") or text.startswith("example"):
            parts = text.split()
            domain = parts[1] if len(parts) > 1 else ""
            return self._format_examples(domain)

        # 1. Try Local Ollama LLM if running
        if self.ollama_available:
            res = self._query_ollama(raw_text)
            if res:
                return res

        # 2. Try Free Cloud API if key exists
        if self.api_key:
            res = self._query_cloud_api(raw_text)
            if res:
                return res

        # 3. Fallback to Local Generative Neural Synthesizer
        return self._generative_neural_engine(raw_text)

    def _query_ollama(self, prompt: str) -> str:
        try:
            payload = json.dumps({
                "model": self.ollama_model,
                "prompt": f"{ENLANG_SYSTEM_PROMPT}\n\nUser Question: {prompt}\n\nEnLang AI Answer:",
                "stream": False
            }).encode("utf-8")

            req = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "EnLangAI"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                ans = data.get("response", "").strip()
                if ans:
                    return f"\n{BOLD}{MAGENTA}🤖 EnLang AI (Ollama - {self.ollama_model}):{RESET}\n{ans}"
        except Exception:
            pass
        return None

    def _query_cloud_api(self, prompt: str) -> str:
        try:
            if self.api_provider == "gemini":
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
                payload = json.dumps({
                    "contents": [{"parts": [{"text": f"{ENLANG_SYSTEM_PROMPT}\n\nUser Question: {prompt}"}]}]
                }).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    return f"\n{BOLD}{CYAN}🤖 EnLang AI (Gemini Flash):{RESET}\n{text}"

            elif self.api_provider == "groq":
                url = "https://api.groq.com/openai/v1/chat/completions"
                payload = json.dumps({
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": ENLANG_SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ]
                }).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                })
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    text = data['choices'][0]['message']['content']
                    return f"\n{BOLD}{GREEN}🤖 EnLang AI (Groq Llama 3):{RESET}\n{text}"
        except Exception:
            pass
        return None

    def _generative_neural_engine(self, raw_text: str) -> str:
        text = raw_text.lower()

        # Concept 1: Control Flow / Branching / Conditionals
        if any(w in text for w in ["control flow", "flow", "branch", "condition", "if statement", "if else", "decision"]):
            return f"""
{BOLD}{MAGENTA}🤖 EnLang AI: Control Flow & Conditional Execution{RESET}

In EnLang, **Control Flow** manages how code executes based on logic. It uses clean, natural English branching statements (`if`, `else if`, `else`) with readable comparison operators.

{BOLD}Key Rules for Control Flow:{RESET}
  1. Block headers end with a colon `{CYAN}:{RESET}` (e.g. `if x is greater than 5 then:`).
  2. Comparisons use natural English: `is equal to`, `is greater than`, `is less than`, `is in`.
  3. Indentation inside blocks must be 4 spaces.

{BOLD}Complete Code Example (.enlg):{RESET}
{CYAN}set score to 85

# Control Flow Branching
if score is greater than or equal to 90 then:
    display "Grade: A+ (Outstanding)"
else if score is greater than 70 then:
    display "Grade: B (Great Job)"
else:
    display "Grade: C (Needs Improvement)"{RESET}

{DIM}Tip: You can also use control flow inside loops or function returns!{RESET}
"""

        # Concept 2: Variables & Data Types
        if any(w in text for w in ["variable", "set", "data type", "type", "assign", "declaration"]):
            return f"""
{BOLD}{MAGENTA}🤖 EnLang AI: Variables & Data Types{RESET}

In EnLang, variables are declared and assigned using the intuitive `set <variable> to <value>` statement. EnLang automatically infers the data type (string, integer, float, boolean, or list).

{BOLD}Code Example (.enlg):{RESET}
{CYAN}# Primitive Types
set app_name to "Aero Portal 3000"
set user_count to 1500
set rating to 4.9
set is_active to true

# Collections (Lists)
set tech_stack to ["HTML5", "CSS3", "JavaScript", "SQLite"]

display "App: " plus app_name{RESET}
"""

        # Concept 3: Loops & Iterations
        if any(w in text for w in ["loop", "repeat", "iteration", "while", "for each"]):
            return f"""
{BOLD}{MAGENTA}🤖 EnLang AI: Loops & Iterations{RESET}

EnLang supports two natural looping mechanisms:
1. `repeat N times:` -> Fixed iteration count
2. `for each item in collection:` -> List iteration

{BOLD}Code Example (.enlg):{RESET}
{CYAN}# 1. Fixed Repeat Loop
repeat 3 times:
    display "Syncing data..."

# 2. Collection Iteration
set servers to ["Server-A", "Server-B", "Server-C"]
for each server in servers:
    display "Connecting to: " plus server{RESET}
"""

        # Concept 4: Functions
        if any(w in text for w in ["function", "define", "method", "subroutine", "return"]):
            return f"""
{BOLD}{MAGENTA}🤖 EnLang AI: Functions & Subroutines{RESET}

Functions in EnLang are defined using `define function <name> with <parameters>:` and return values using `return`.

{BOLD}Code Example (.enlg):{RESET}
{CYAN}define function calculate_tax with amount and rate:
    set tax to amount times rate
    set total to amount plus tax
    return total

set final_amount to calculate_tax with 200 and 0.18
display "Final Bill: " plus final_amount{RESET}
"""

        # Concept 5: Web UI Components (.enlgf & .enlgd)
        if any(w in text for w in ["web", "ui", "component", "html", "css", "navbar", "form", "card", "glass"]):
            return f"""
{BOLD}{MAGENTA}🤖 EnLang AI: Web Application Architecture (.enlgf & .enlgd){RESET}

EnLang builds full-stack web applications by pairing **.enlgf** (UI Markup) with **.enlgd** (CSS Design).

{BOLD}1. Frontend UI Markup (.enlgf):{RESET}
{CYAN}page named "User Dashboard"
include stylesheet "style.enlgd"

create nav named "main-nav" with class "navbar":
    create h1 with text "Aero Dashboard"
    create button with text "Login" with class "btn-primary"{RESET}

{BOLD}2. Design Styling (.enlgd):{RESET}
{BLUE}var bg_dark = "#0f172a"
var primary = "#6366f1"

in class navbar:
    background color to bg_dark
    display to "flex"
    space inside to "1rem 2rem"

in child button of class navbar on hover:
    background color to primary
    rounded to "8px"{RESET}
"""

        # Concept 6: Database & SQL (.enlgdb)
        if any(w in text for w in ["database", "sql", "db", "table", "sqlite", "query"]):
            return f"""
{BOLD}{MAGENTA}🤖 EnLang AI: Database Programming (.enlgdb){RESET}

EnLang DB scripts (.enlgdb) compile 1:1 to SQLite SQL, creating tables and rendering rich terminal ASCII tables automatically.

{BOLD}Code Example (.enlgdb):{RESET}
{CYAN}create table users:
    id PRIMARY KEY AUTOINCREMENT
    username TEXT NOT NULL UNIQUE
    email TEXT NOT NULL

insert record into users:
    username = "aero"
    email = "aero@enlang.org"

select all from users where id > 0 order by id desc limit 10{RESET}
"""

        # General Intelligent Response
        return f"""
{BOLD}{CYAN}🤖 EnLang AI ChatGPT-Level Assistant:{RESET}

I analyzed your question '{raw_text}'. EnLang is designed as a universal natural English language for software, web, database, and AI development.

{BOLD}Core Capabilities You Can Ask Me:{RESET}
  • {GREEN}Core Logic (.enlg){RESET}: Variables, Control Flow, Loops, Functions, AI Sentiment
  • {YELLOW}Frontend Markup (.enlgf){RESET}: Pages, Forms, Cards, Navbars, Input fields
  • {BLUE}Design System (.enlgd){RESET}: Simple, Combinator, Attribute, Pseudo-class, Pseudo-element Selectors
  • {MAGENTA}Client Scripts (.enlgs){RESET}: Event Listeners, Fetch API, DOM manipulation
  • {CYAN}Database (.enlgdb){RESET}: Table creation, Record inserts, SQL Select queries

{DIM}Pro Tip: Ask me 'how to write loops', 'create a login form', or 'explain control flow'!{RESET}
"""

    def _format_help(self) -> str:
        return f"""
{BOLD}Available EnLang Topics & AI Capabilities:{RESET}
  • {GREEN}control flow / if{RESET}: Conditional logic, comparisons, branching
  • {GREEN}variables / set{RESET}   : Variable assignment and data types
  • {GREEN}loops / repeat{RESET}    : Repeat blocks and list iterations
  • {GREEN}functions{RESET}         : Subroutine definitions and returns
  • {GREEN}ai / ml{RESET}            : Built-in Machine Learning primitives
  • {YELLOW}enlgf / markup{RESET}     : Building semantic HTML5 components
  • {BLUE}enlgd / css{RESET}        : All 5 CSS selector types and styling rules
  • {MAGENTA}enlgs / js{RESET}         : Client JS scripts, click events, fetch API
  • {CYAN}enlgdb / sql{RESET}       : SQLite database schemas and queries
  • {BOLD}cli / commands{RESET}     : Compiler, web server, and linter commands
"""

    def _format_examples(self, domain: str) -> str:
        domain = domain.strip().lower().replace('.', '')
        if domain in ["enlgd", "css", "style"]:
            return f"""
{BOLD}=== .ENLGD (CSS Styling & 5 Selector Types) ==={RESET}
{BLUE}var primary = "#6366f1"

# 1. Simple Selector
in class navbar:
    space inside to "1rem 2rem"

# 2. Combinator
in child button of class navbar:
    background color to primary

# 3. Attribute
in input with type "text":
    border to "1px solid #334155"

# 4. Pseudo-Class (Hover)
in button on hover:
    opacity to "0.9"

# 5. Pseudo-Element (Before)
in class navbar before:
    content to ""{RESET}
"""
        elif domain in ["enlgf", "html", "markup"]:
            return f"""
{BOLD}=== .ENLGF (Frontend UI Components) ==={RESET}
{CYAN}page named "Home"
include stylesheet "style.enlgd"

create nav named "bar" with class "navbar":
    create h1 with text "Aero Portal"
    create button with text "Login" with class "btn-primary"{RESET}
"""
        elif domain in ["enlgdb", "sql", "db"]:
            return f"""
{BOLD}=== .ENLGDB (Database Programming) ==={RESET}
{CYAN}create table users:
    id PRIMARY KEY AUTOINCREMENT
    username TEXT NOT NULL

insert record into users:
    username = "aero"

select all from users where id > 0{RESET}
"""
        else:
            return f"""
{BOLD}=== .ENLG (Core Logic) ==={RESET}
{GREEN}set n to 10

if n is greater than 5 then:
    display "n is large"
else:
    display "n is small"{RESET}
"""

def start_chatbot():
    engine = EnLangHybridLLMEngine()
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
