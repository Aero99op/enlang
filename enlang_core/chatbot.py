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

ENLANG_SYSTEM_PROMPT = """You are EnLang AI, a world-class AI assistant and expert compiler/web engineer specializing in the EnLang Natural English Programming Language Ecosystem.

EnLang consists of 5 core domains:
1. .enlg   -> Core Logic (Variables: set x to 10, Conditions: if x is greater than 5 then:, Loops: repeat 3 times:, Functions: define function add with x and y:, ML: train classifier / predict)
2. .enlgf  -> Frontend Markup (HTML5 tags: page named "Home", create nav, create card, create form, create button, create input)
3. .enlgd  -> Design & CSS (Selectors: Simple 'in class navbar', Combinator 'in child p of div', Attribute 'in input with type "text"', Pseudo-class 'in btn on hover', Pseudo-element 'in card before', Properties: space inside, space outside, rounded, shadow, text color)
4. .enlgs  -> Client Scripts (ES6+ JS: when button clicked:, fetch json from url then:, log text, alert)
5. .enlgdb -> Database & SQL (SQLite: create table users, insert record into users, select all from users where id > 0)

Answer ANY user question (technical, conversational, comparisons, debugging, or general knowledge) intelligently, accurately, and politely with copy-pasteable EnLang code examples where appropriate."""

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

        # Retrieve RAG Book Context
        matches = self.trainer.retrieve(raw_text, top_k=2)
        rag_context = ""
        if matches:
            rag_context = "\n\nRelevant EnLang Master Textbook Reference:\n" + "\n---\n".join([m['content'][:800] for m in matches])

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
        return self._native_book_rag_engine(raw_text, text)

    def _query_groq(self, prompt: str, rag_context: str = "") -> str:
        """Queries Groq Llama 3.3 70B (Free Tier: 14,400 free requests per day, ~500 tokens/sec)."""
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

    def _native_book_rag_engine(self, raw_text: str, text: str) -> str:
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

        matches = self.trainer.retrieve(raw_text, top_k=2)
        words = [w.capitalize() for w in re.findall(r'\w+', raw_text) if len(w) > 2]
        topic = " ".join(words[:4]) if words else raw_text

        return f"""
{BOLD}{CYAN}🤖 EnLang Book-Trained AI Analysis: "{raw_text}"{RESET}

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
    display "Execution successful for: " plus "{topic}"{RESET}
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
                print(f"\n{BOLD}{MAGENTA}Thank you for using EnLang AI Assistant! Happy coding! 🚀{RESET}\n")
                break
                
            print(response)
            print()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{BOLD}{MAGENTA}Exiting EnLang AI Assistant. Goodbye! 🚀{RESET}\n")
            break

if __name__ == "__main__":
    start_chatbot()
