"""
EnLang Hybrid AI Terminal Assistant Engine (Groq Llama 3.3 70B / Multi-Provider Powered)
=======================================================================================
Secure API Key Management: Loads keys from Environment Variables (GROQ_API_KEY, GEMINI_API_KEY),
local .env files, or ~/.enlang/keys.json with automatic RAG Book Knowledge fallback.
"""

import sys
import os
import re
import math
import glob
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

ENLANG_SYSTEM_PROMPT = """You are EnLang AI, the official AI assistant and language engine for EnLang — the Universal Natural English Programming Language Ecosystem.

### STRICT RULES FOR ZERO HALLUCINATION (MUST FOLLOW 100%):
1. **NO DOMAIN MIXING**:
   - In `.enlg` (Core Logic) scripts: NEVER put UI/HTML commands like `page named ...`, `create nav`, or HTML tags. Logic scripts start DIRECTLY with variables (`set`), conditions (`if`), loops (`while`/`repeat`/`for each`), or output (`display`).
   - `page named "..."` belongs ONLY in `.enlgf` (Frontend Markup) files.

2. **NUMERIC COMPARISONS & INPUT**:
   - `ask "..."` returns a string. When taking numeric input for comparisons (e.g. attendance percentage, age, score), ALWAYS convert it to integer/decimal first:
     ```enlg
     set score to ask "Enter score: "
     convert score to integer
     if score is greater than 90 then:
         display "Passed"
     ```

3. **CORE LOGIC SYNTAX (.enlg)**:
   - Output: ALWAYS use `display <expr>`. NEVER use `print` or `log text:`.
   - Variables: ALWAYS use `set <var> to <val>`.
   - Functions: ALWAYS use `function <name> with <arg1> and <arg2>:`.
   - Invocations: ALWAYS use `call <name> with <arg>`.
   - Counter Loops: ALWAYS use `repeat <N> times:`.
   - Collection Loops: ALWAYS use `for each <item> in <list>:`.
   - Conditional Loops: ALWAYS use `while <condition> then:`.

4. **FRONTEND MARKUP SYNTAX (.enlgf)**:
   - Page: `page named "Home"`
   - UI Elements: `create div with text "Hello"`, `create button with text "Submit"`

5. **DESIGN SYNTAX (.enlgd)**:
   - Selectors: `in class navbar`, `in btn on hover`
   - Properties: `background color: #1e1e2e`, `padding: 20px`

6. **CLIENT SCRIPT SYNTAX (.enlgs)**:
   - `when button clicked:`, `log text: "Clicked"`, `alert "Saved"`

### GOLDEN VERIFIED ENLANG CODE EXAMPLE (.enlg):
```enlg
set attendees to []
set attendeeName to ask "Enter student name: "
set attendancePercentage to ask "Enter attendance percentage (0-100): "
convert attendancePercentage to integer

if attendancePercentage is greater than or equal to 90 then:
    set feedback to "High - Excellent attendance!"
else if attendancePercentage is greater than or equal to 80 then:
    set feedback to "Medium - Good attendance."
else:
    set feedback to "Low - Need more attendance."

set attendee to attendeeName plus " - " plus attendancePercentage plus "% - " plus feedback
add attendee to attendees

display "Attendance Record: "
for each record in attendees:
    display record
```

Always double check the reference context below and enforce 100% exact syntax matching."""

def _load_key_from_env_or_config(key_name: str) -> str:
    """Safely retrieves API key from environment, local .env, or ~/.enlang/keys.json."""
    val = os.environ.get(key_name)
    if val:
        return val.strip()

    # Try local .env file
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(f"{key_name}="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass

    # Try home directory keys.json
    home_key_file = os.path.expanduser(os.path.join("~", ".enlang", "keys.json"))
    if os.path.exists(home_key_file):
        try:
            with open(home_key_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if key_name in data:
                    return data[key_name].strip()
        except Exception:
            pass

    return None

class EnLangBookTrainer:
    """RAG & Semantic Indexing Engine trained on EnLang Master Books."""

    def __init__(self, books_dir: str):
        self.books_dir = books_dir
        self.knowledge_chunks = []
        self.index_knowledge_base()

    def index_knowledge_base(self):
        """Discovers and indexes all EnLang textbook chapters & core grammar/transpiler code files."""
        # 1. Index Books
        if os.path.exists(self.books_dir):
            for root, _, files in os.walk(self.books_dir):
                for file in files:
                    if file.endswith(".md") or file.startswith("build_quality_"):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()

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

        # 2. Index Core Grammar & Transpiler Source Code for 100% Exact Syntax Matching
        core_dir = os.path.dirname(os.path.abspath(__file__))
        core_files = ["grammar.py", "transpiler.py", "interpreter.py", "checker.py"]
        for fname in core_files:
            fpath = os.path.join(core_dir, fname)
            if os.path.exists(fpath):
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    sections = content.split("\n\n")
                    for sec in sections:
                        sec = sec.strip()
                        if len(sec) > 50:
                            self.knowledge_chunks.append({
                                "source": fname,
                                "title": f"EnLang Core Engine ({fname})",
                                "content": sec[:1500],
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
    """Hybrid AI Assistant Engine with Secure API Key Management & RAG Book Fallback."""

    def __init__(self):
        self.history = []
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        books_path = os.path.join(base_dir, "books")
        self.trainer = EnLangBookTrainer(books_path)

        self.groq_key = _load_key_from_env_or_config("GROQ_API_KEY")
        self.gemini_key = _load_key_from_env_or_config("GEMINI_API_KEY")
        self.openrouter_key = _load_key_from_env_or_config("OPENROUTER_API_KEY")
        self.ollama_available, self.ollama_model = self._check_ollama()

    def _check_ollama(self):
        try:
            req = urllib.request.Request("http://localhost:11434/api/tags", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=1.2) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                if models:
                    return True, models[0]
        except Exception:
            pass
        return False, None

    def welcome_banner(self):
        chunks_count = len(self.trainer.knowledge_chunks)
        active_backend = ""

        if self.groq_key:
            active_backend = f" {GREEN}● Engine: Groq Llama 3.3 70B (Ultra-Fast 500+ tok/sec | Secure Cloud API Key){RESET}"
        elif self.gemini_key:
            active_backend = f" {CYAN}● Engine: Google Gemini 2.0 Flash (Cloud Key Active){RESET}"
        elif self.openrouter_key:
            active_backend = f" {MAGENTA}● Engine: OpenRouter Free Models Aggregator{RESET}"
        elif self.ollama_available:
            active_backend = f" {BLUE}● Engine: Local Ollama Neural Model ({self.ollama_model}){RESET}"
        else:
            active_backend = f" {YELLOW}● Engine: Book-Trained RAG Engine ({chunks_count} Sections Indexed | 100% Offline){RESET}"

        return f"""
{CYAN}================================================================================{RESET}
{BOLD}{MAGENTA}       🤖 ENLANG TERMINAL AI ASSISTANT  —  HYBRID NEURAL & RAG BRAIN 🤖{RESET}
{CYAN}================================================================================{RESET}
{active_backend}

{BOLD} Welcome! Ask me ANY question (coding, architecture, comparisons, debugging):{RESET}
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
            return f"{YELLOW}I am ready! Ask me any question (e.g. 'write a login form in enlangf' or 'explain control flow'){RESET}"

        if text in ["exit", "quit", "q", "bye", "goodbye"]:
            return "EXIT"

        if text in ["help", "commands"]:
            return self._format_help()

        if text.startswith("examples") or text.startswith("example"):
            parts = text.split()
            domain = parts[1] if len(parts) > 1 else ""
            return self._format_examples(domain)

        self.history.append(raw_text)

        # Domain Detection for RAG Focus
        detected_domain = ""
        for dom in ["enlgf", "enlgd", "enlgs", "enlgdb", "enlg"]:
            if dom in text:
                detected_domain = dom
                break
        if not detected_domain:
            if any(w in text for w in ["css", "style", "color", "design", "selector"]):
                detected_domain = "enlgd"
            elif any(w in text for w in ["html", "markup", "page", "card", "button", "frontend"]):
                detected_domain = "enlgf"
            elif any(w in text for w in ["js", "javascript", "fetch", "event", "click", "script"]):
                detected_domain = "enlgs"
            elif any(w in text for w in ["sql", "database", "table", "query", "db"]):
                detected_domain = "enlgdb"
            elif any(w in text for w in ["logic", "variable", "if", "loop", "function"]):
                detected_domain = "enlg"

        # Retrieve RAG Book Context
        search_query = f"{detected_domain} {raw_text}" if detected_domain else raw_text
        matches = self.trainer.retrieve(search_query, top_k=4)
        rag_context = ""
        if matches:
            rag_context = f"\n\nOfficial EnLang Book & Codebase References (Focus: {detected_domain or 'General'}):\n" + "\n---\n".join([f"[{m['source']} - {m['title']}]\n{m['content']}" for m in matches])

        # 1. Try Free High-Speed Cloud LLM APIs (Groq -> Gemini -> OpenRouter -> Ollama)
        if self.groq_key:
            res = self._query_groq(raw_text, rag_context)
            if res:
                return res

        if self.gemini_key:
            res = self._query_gemini(raw_text, rag_context)
            if res:
                return res

        if self.openrouter_key:
            res = self._query_openrouter(raw_text, rag_context)
            if res:
                return res

        if self.ollama_available:
            res = self._query_ollama(raw_text, rag_context)
            if res:
                return res

        # 2. Native Book-Trained RAG Fallback Engine
        return self._native_book_rag_engine(raw_text, text, detected_domain)

    def _query_groq(self, prompt: str, rag_context: str = "") -> str:
        """Queries Groq Llama 3.3 70B."""
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            system_prompt = ENLANG_SYSTEM_PROMPT + rag_context
            payload = json.dumps({
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.groq_key}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data['choices'][0]['message']['content']
                return f"\n{BOLD}{GREEN}🤖 EnLang AI (Groq Llama 3.3 70B):{RESET}\n{text}"
        except Exception:
            pass
        return None

    def _query_gemini(self, prompt: str, rag_context: str = "") -> str:
        """Queries Google Gemini 2.0 Flash."""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_key}"
            system_prompt = ENLANG_SYSTEM_PROMPT + rag_context
            payload = json.dumps({
                "contents": [{"parts": [{"text": f"{system_prompt}\n\nUser Question: {prompt}"}]}]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data['candidates'][0]['content']['parts'][0]['text']
                return f"\n{BOLD}{CYAN}🤖 EnLang AI (Google Gemini 2.0 Flash):{RESET}\n{text}"
        except Exception:
            pass
        return None

    def _query_openrouter(self, prompt: str, rag_context: str = "") -> str:
        """Queries OpenRouter Free Tier Models."""
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            system_prompt = ENLANG_SYSTEM_PROMPT + rag_context
            payload = json.dumps({
                "model": "meta-llama/llama-3.2-11b-vision-instruct:free",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openrouter_key}",
                "User-Agent": "Mozilla/5.0"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data['choices'][0]['message']['content']
                return f"\n{BOLD}{MAGENTA}🤖 EnLang AI (OpenRouter Free API):{RESET}\n{text}"
        except Exception:
            pass
        return None

    def _query_ollama(self, prompt: str, rag_context: str = "") -> str:
        """Queries Local Ollama Instance."""
        try:
            system_prompt = ENLANG_SYSTEM_PROMPT + rag_context
            payload = json.dumps({
                "model": self.ollama_model,
                "prompt": f"{system_prompt}\n\nUser Question: {prompt}\n\nEnLang AI Answer:",
                "stream": False
            }).encode("utf-8")
            req = urllib.request.Request("http://localhost:11434/api/generate", data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data.get("response", "").strip()
                if text:
                    return f"\n{BOLD}{BLUE}🤖 EnLang AI (Local Ollama - {self.ollama_model}):{RESET}\n{text}"
        except Exception:
            pass
        return None

    def _native_book_rag_engine(self, raw_text: str, text: str, domain: str = "") -> str:
        if text in ["hi", "hello", "hey", "namaste", "greetings", "good morning", "good evening"]:
            return f"""
{BOLD}{MAGENTA}🤖 EnLang Native AI: Hello!{RESET}

Welcome! I am your AI assistant trained on EnLang textbooks and specifications. How can I help you today?
"""

        matches = self.trainer.retrieve(raw_text, top_k=3)
        retrieved_text = ""
        if matches:
            retrieved_text = "\n\n" + "\n---\n".join([f"[{m['title']}]\n{m['content']}" for m in matches])

        return f"""
{BOLD}{CYAN}🤖 EnLang Book-Trained AI Analysis for "{raw_text}":{RESET}
{retrieved_text if retrieved_text else "No direct book match found, refer to domain guidelines."}
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
        d = domain.lower().replace(".", "")
        if d == "enlgf":
            return f"""
{BOLD}=== .ENLGF (Frontend Markup Template) ==={RESET}
{YELLOW}page named "Dashboard"

create nav with id "navbar":
    create div with text "Logo"
    create button with text "Logout"

create section with class "hero":
    create h1 with text "Welcome Back!"
    create p with text "Here is your system overview."

create form with action "/api/save":
    create input with type "text" and placeholder "Enter name"
    create button with type "submit" and text "Save"{RESET}
"""
        elif d == "enlgd":
            return f"""
{BOLD}=== .ENLGD (Design & CSS System Template - 5 Selectors) ==={RESET}
{BLUE}# 1. Simple Class Selector
in class hero:
    space inside: 40px
    background color: #1e1e2e
    rounded: 12px

# 2. Combinator Selector
in child p of div:
    text color: #a6adc8
    font size: 16px

# 3. Attribute Selector
in input with type "text":
    border: 1px solid #45475a
    padding: 10px

# 4. Pseudo-class Selector
in btn on hover:
    background color: #89b4fa
    cursor: pointer

# 5. Pseudo-element Selector
in card before:
    content: ""
    display: block{RESET}
"""
        elif d == "enlgs":
            return f"""
{BOLD}=== .ENLGS (Client Script Template) ==={RESET}
{MAGENTA}when button with id "btn-fetch" clicked:
    log text: "Fetching data from server..."
    fetch json from url "https://api.example.com/data" then:
        display json.result
        alert "Data loaded successfully!"{RESET}
"""
        elif d == "enlgdb":
            return f"""
{BOLD}=== .ENLGDB (Database Schema & Queries Template) ==={RESET}
{CYAN}connect to database "app.db" as db

create table users with columns id integer primary key, name text, email text

insert record into users with values 1, "Spandan", "spandan@example.com"

execute query "SELECT * FROM users WHERE id = 1" on db and store in user_record
display user_record{RESET}
"""
        else:
            return f"""
{BOLD}=== .ENLG (Core Logic Template) ==={RESET}
{GREEN}set users to ["Alice", "Bob", "Charlie"]

function greetUser with name:
    display "Hello, " plus name

for each user in users:
    call greetUser with user

repeat 3 times:
    display "Loop iteration active"{RESET}
"""

def start_chatbot():
    engine = EnLangNativeLLMBrain()
    print(engine.welcome_banner())

    while True:
        try:
            user_input = input(f"{BOLD}{CYAN}EnLang AI > {RESET}")
            response = engine.process_query(user_input)
            
            if response == "EXIT":
                print(f"\n{BOLD}{MAGENTA}Thank you for using EnLang AI Assistant! Happy coding! 🚀{RESET}\n")
                break
                
            print(response)
            print()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{BOLD}{MAGENTA}Exiting EnLang AI Assistant. Goodbye! 🚀{RESET}\n")
            break

if __name__ == "__main__":
    start_chatbot()
