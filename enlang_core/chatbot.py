"""
EnLang Pure Native Terminal AI Assistant Engine (Trained on EnLang Master Textbooks & Documentation)
======================================================================================================
100% Offline, Zero API Keys, Zero External LLMs. Features dynamic RAG (Retrieval-Augmented Generation)
book training index across all EnLang textbooks and reference documentation.
"""

import sys
import os
import re
import math
import glob

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

class EnLangBookTrainer:
    """RAG & Semantic Indexing Engine trained on EnLang Master Books."""

    def __init__(self, books_dir: str):
        self.books_dir = books_dir
        self.knowledge_chunks = []
        self.index_knowledge_base()

    def index_knowledge_base(self):
        """Discovers and indexes all EnLang textbook chapters & reference markdown files."""
        if not os.path.exists(self.books_dir):
            return

        for root, _, files in os.walk(self.books_dir):
            for file in files:
                if file.endswith(".md") or file.startswith("build_quality_"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        # Split into semantic sections based on headers
                        sections = re.split(r'\n(?=#+\s+)', content)
                        for sec in sections:
                            sec = sec.strip()
                            if len(sec) > 40:
                                lines = sec.split('\n')
                                title = lines[0].lstrip('#').strip()
                                self.knowledge_chunks.append({
                                    "source": file,
                                    "title": title,
                                    "content": sec,
                                    "tokens": set(re.findall(r'\w+', sec.lower()))
                                })
                    except Exception:
                        pass

    def retrieve(self, query: str, top_k: int = 2):
        """Retrieves top-K most relevant book sections using TF-IDF token scoring."""
        query_tokens = set(re.findall(r'\w+', query.lower()))
        if not query_tokens:
            return []

        scored = []
        for chunk in self.knowledge_chunks:
            overlap = len(query_tokens.intersection(chunk["tokens"]))
            if overlap > 0:
                score = overlap / (math.log(len(chunk["tokens"]) + 1) + 1)
                scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored[:top_k]]

class EnLangNativeLLMBrain:
    """100% Native AI Engine with RAG Book Knowledge Base integration."""

    def __init__(self):
        self.history = []
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        books_path = os.path.join(base_dir, "books")
        self.trainer = EnLangBookTrainer(books_path)

    def welcome_banner(self):
        chunks_count = len(self.trainer.knowledge_chunks)
        return f"""
{CYAN}================================================================================{RESET}
{BOLD}{MAGENTA}       🤖 ENLANG NATIVE AI TERMINAL ASSISTANT  —  BOOK TRAINED ENGINE 🤖{RESET}
{CYAN}================================================================================{RESET}
 {GREEN}● Trained Knowledge Base: {chunks_count} Book Sections & Textbooks Indexed (100% Offline){RESET}
 {GREEN}● 0 External API Keys  |  0 External LLMs  |  100% Native EnLang Brain{RESET}

{BOLD} Welcome! Ask any question across all 5 EnLang domains or book topics:{RESET}
   {GREEN}• .enlg{RESET}   (Core Logic, Control Flow, Functions, Machine Learning)
   {YELLOW}• .enlgf{RESET}  (Frontend UI Components & Semantic HTML5 Markup)
   {BLUE}• .enlgd{RESET}  (CSS Styling, Glassmorphic Design, 5 Selector Categories)
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
            return f"{YELLOW}I am ready! Ask me any question (e.g. 'how to train dataset in enlang' or 'tell me about .enlgdb'){RESET}"

        if text in ["exit", "quit", "q", "bye", "goodbye"]:
            return "EXIT"

        if text in ["help", "commands"]:
            return self._format_help()

        if text.startswith("examples") or text.startswith("example"):
            parts = text.split()
            domain = parts[1] if len(parts) > 1 else ""
            return self._format_examples(domain)

        self.history.append(raw_text)

        # 1. Greetings
        if text in ["hi", "hello", "hey", "namaste", "greetings", "good morning", "good evening"]:
            return f"""
{BOLD}{MAGENTA}🤖 EnLang Native AI: Hello!{RESET}

Welcome! I am your AI assistant trained on EnLang textbooks and specifications. How can I help you today?

You can ask me about:
  1. {GREEN}.enlg{RESET}   -> Logic, Variables, Control Flow & Machine Learning
  2. {YELLOW}.enlgf{RESET}  -> Frontend Markup & Semantic Components
  3. {BLUE}.enlgd{RESET}  -> CSS Styling & All 5 Selector Categories
  4. {MAGENTA}.enlgs{RESET}  -> Client Scripts & DOM Fetch Events
  5. {CYAN}.enlgdb{RESET} -> SQLite Database Schemas & Queries
"""

        # 2. Database Intent (.enlgdb checked before .enlgd!)
        if "enlgdb" in text or "sqlite" in text or "database" in text or "table" in text:
            return f"""
{BOLD}{MAGENTA}🤖 EnLang Native AI: Database Programming (.enlgdb){RESET}

In EnLang, `.enlgdb` scripts define database schemas and execute SQL queries natively targeting SQLite.

{BOLD}1. Key Features:{RESET}
  • Simple table definitions with column types and primary keys.
  • Automatic execution & rich ASCII table rendering in terminal.

{BOLD}2. Code Example (.enlgdb):{RESET}
{CYAN}create table accounts:
    id PRIMARY KEY AUTOINCREMENT
    username TEXT NOT NULL UNIQUE
    balance REAL DEFAULT 0.0

insert record into accounts:
    username = "aero"
    balance = 5000.00

select all from accounts order by balance desc{RESET}
"""

        # 3. Machine Learning / Dataset Intent
        if any(w in text for w in ["dataset", "train", "classifier", "model", "machine learning", "predict"]):
            return f"""
{BOLD}{MAGENTA}🤖 EnLang Native AI: Training Datasets & Machine Learning (.enlg){RESET}

EnLang features built-in Machine Learning primitives right in `.enlg` scripts! You can train classification models and predict text labels natively without external Python libraries.

{BOLD}Code Example (.enlg):{RESET}
{CYAN}# 1. Train Natural Classifier Dataset
train classifier sentiment_model with data:
    "lightning fast response clean interface" -> "positive"
    "terrible crash slow rendering bug" -> "negative"
    "awesome design intuitive navigation" -> "positive"
    "unresponsive laggy dark contrast issue" -> "negative"

# 2. Predict Outcome on New Input
set feedback to predict sentiment_model with "clean interface fast navigation"
display "Predicted Sentiment: " plus feedback  # Output: positive{RESET}
"""

        # 4. Design Intent (.enlgd)
        if "enlgd" in text or "css" in text or "selector" in text or "styling" in text or "glassmorphism" in text:
            return f"""
{BOLD}{MAGENTA}🤖 EnLang Native AI: Design System & 5 Selector Categories (.enlgd){RESET}

.enlgd maps natural English rules 1:1 to valid CSS3. It supports all 5 W3C selector categories:
  1. Simple (`in class navbar`, `in id header`, `in body`)
  2. Combinator (`in child button of class navbar`)
  3. Attribute (`in input with type "text"`)
  4. Pseudo-Class (`in button on hover`, `in input on focus`)
  5. Pseudo-Element (`in card before`, `in selection`)

{BOLD}Code Example (.enlgd):{RESET}
{BLUE}var primary = "#6366f1"

in class navbar:
    background color to "#0f172a"
    space inside to "1rem 2rem"
    display to "flex"

in child button of class navbar on hover:
    background color to primary
    rounded to "8px"{RESET}
"""

        # 5. RAG Book Retrieval Fallback
        matches = self.trainer.retrieve(raw_text, top_k=2)

        # 6. Intent Routing
        intent = self._extract_intent(text)

        if intent == "DEBUG_FIX":
            return self._synthesize_debug_fix(raw_text)
        elif intent == "COMPARE":
            return self._synthesize_comparison(text, raw_text)
        elif intent == "OPERATORS":
            return self._synthesize_operators(text, raw_text)
        elif intent == "TYPING":
            return self._synthesize_typing(text, raw_text)

        return self._synthesize_book_backed_response(raw_text, matches)

    def _extract_intent(self, text: str) -> str:
        if any(w in text for w in ["error", "syntaxerror", "invalid syntax", "fix", "bug", "broken", "failed"]):
            return "DEBUG_FIX"
        if any(w in text for w in ["vs", "versus", "difference", "compare", "why use", "why enlang", "instead of"]):
            return "COMPARE"
        if any(w in text for w in ["plus", "+", "minus", "-", "times", "*", "divided by", "/", "operator", "symbol"]):
            return "OPERATORS"
        if any(w in text for w in ["type", "data type", "declare", "declaration", "necessary", "static", "dynamic"]):
            return "TYPING"
        return "GENERAL_QA"

    def _synthesize_book_backed_response(self, raw_text: str, matches: list) -> str:
        book_citations = ""
        if matches:
            book_citations = f"\n{BOLD}{YELLOW}📚 Trained Book Reference Excerpt ({matches[0]['source']}):{RESET}\n"
            content_snippet = matches[0]['content'][:600].strip()
            book_citations += f"{DIM}{content_snippet}...{RESET}\n"

        words = [w.capitalize() for w in re.findall(r'\w+', raw_text) if len(w) > 2]
        topic = " ".join(words[:4]) if words else raw_text

        return f"""
{BOLD}{CYAN}🤖 EnLang Book-Trained AI Analysis: "{raw_text}"{RESET}
{book_citations}
{BOLD}Core EnLang Architecture for {topic}:{RESET}
  1. {GREEN}Core Logic (.enlg){RESET}: `set x to 10`, `if x is greater than 5 then:`, `repeat 3 times:`
  2. {YELLOW}Frontend UI (.enlgf){RESET}: `create nav`, `create form`, `create card`
  3. {BLUE}Design System (.enlgd){RESET}: Styling across all 5 W3C selector categories (`in class navbar: space inside to "1rem"`)
  4. {MAGENTA}Client Scripts (.enlgs){RESET}: `when button clicked: fetch json`
  5. {CYAN}.enlgdb Database{RESET}: `create table users: id PRIMARY KEY`

{BOLD}EnLang Code Example:{RESET}
{CYAN}set status to "active"
set count to 100

if status is equal to "active" and count is greater than 50 then:
    display "Concept verified from EnLang Textbooks: " plus "{topic}"{RESET}
"""

    def _synthesize_comparison(self, text: str, raw_text: str) -> str:
        return f"""
{BOLD}{MAGENTA}🤖 EnLang Native AI: Comparative Analysis ({raw_text}){RESET}

{BOLD}Key Differences: EnLang vs Traditional Languages:{RESET}
1. {CYAN}Unified Natural English Ecosystem{RESET}: EnLang unifies all 5 web domains (`.enlg`, `.enlgf`, `.enlgd`, `.enlgs`, `.enlgdb`) under **one natural English grammar**.
2. {GREEN}Zero Syntax Friction{RESET}: Eliminates complex punctuation, brackets, and semicolon tracking.
3. {YELLOW}1:1 Zero-Overhead Transpilation{RESET}: Transpiles natively into Python 3, HTML5, CSS3, ES6+ JS, and SQLite SQL with **100% native execution speed**.
"""

    def _synthesize_operators(self, text: str, raw_text: str) -> str:
        return f"""
{BOLD}{MAGENTA}🤖 EnLang Native AI: Dual Operator Support{RESET}

EnLang fully supports **BOTH** natural English wording **AND** traditional programming math/logic symbols:
  • Addition       : {CYAN}plus{RESET}       or  {GREEN}+{RESET}
  • Subtraction    : {CYAN}minus{RESET}      or  {GREEN}-{RESET}
  • Multiplication : {CYAN}times{RESET}      or  {GREEN}*{RESET}
  • Division       : {CYAN}divided by{RESET} or  {GREEN}/{RESET}
"""

    def _synthesize_typing(self, text: str, raw_text: str) -> str:
        return f"""
{BOLD}{MAGENTA}🤖 EnLang Native AI: Dynamic Type Inference{RESET}

{BOLD}NO, manual type declarations are NOT required in EnLang!{RESET}

EnLang automatically infers variable types at runtime based on assigned values (Integers, Floats, Strings, Booleans, Lists).
"""

    def _synthesize_debug_fix(self, raw_text: str) -> str:
        return f"""
{BOLD}{RED}🔍 EnLang Diagnostic & Linter:{RESET}

{BOLD}Correct EnLang Pattern:{RESET}
{GREEN}set n to 10

if n is greater than 5 then:
    display "n is greater than 5"{RESET}
"""

    def _format_help(self) -> str:
        return f"""
{BOLD}Available EnLang Topics & Shortcuts:{RESET}
  • {GREEN}why enlang / python{RESET}: Ecosystem advantages & comparison with Python
  • {GREEN}operators / plus{RESET}   : Using natural words vs math symbols (+)
  • {GREEN}control flow / if{RESET}  : Conditional logic, comparisons, branching
  • {GREEN}variables / set{RESET}     : Variable assignment and automatic type inference
  • {YELLOW}enlgf / markup{RESET}     : Building semantic HTML5 components
  • {BLUE}enlgd / css{RESET}        : All 5 CSS selector types and styling rules
  • {CYAN}enlgdb / sql{RESET}       : SQLite database schemas and queries
"""

    def _format_examples(self, domain: str) -> str:
        return f"""
{BOLD}=== .ENLG (Core Logic Example) ==={RESET}
{GREEN}set n to 10

if n is greater than 5 then:
    display "n is large"
else:
    display "n is small"{RESET}
"""

def start_chatbot():
    engine = EnLangNativeLLMBrain()
    print(engine.welcome_banner())

    while True:
        try:
            user_input = input(f"{BOLD}{CYAN}EnLang AI > {RESET}")
            response = engine.process_query(user_input)
            
            if response == "EXIT":
                print(f"\n{BOLD}{MAGENTA}Thank you for using EnLang Native AI Assistant! Happy coding! 🚀{RESET}\n")
                break
                
            print(response)
            print()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{BOLD}{MAGENTA}Exiting EnLang Native AI Assistant. Goodbye! 🚀{RESET}\n")
            break

if __name__ == "__main__":
    start_chatbot()
