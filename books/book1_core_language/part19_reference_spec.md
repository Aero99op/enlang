# Part 19: Complete Language Keyword Matrix & Specification

This reference chapter summarizes the core keywords, file extensions, and target transpilation mappings of the EnLang language suite.

## File Extension Matrix

| Extension | Domain | Target Language | CLI Compile Command |
| :--- | :--- | :--- | :--- |
| **`.enlg`** | Core Backend Logic & Algorithms | Python 3 | `enlang build main.enlg` |
| **`.enlgf`** | Structural Frontend Markup | HTML5 | `enlang build index.enlgf` |
| **`.enlgd`** | Styling & Design Systems | CSS3 | `enlang build style.enlgd` |
| **`.enlgs`** | Client Scripting & DOM Logic | JavaScript (ES6+) | `enlang build app.enlgs` |
| **`.enlgdb`** | Database Schemas & Queries | ANSI SQL / SQLite | `enlang build schema.enlgdb` |

## Keyword Transpilation Matrix

| Natural English Syntax | Domain | Transpiled Output |
| :--- | :--- | :--- |
| `define <type> <var> as <val>` | Logic | `<var> = <val>` |
| `set <var> to <val>` | Logic | `<var> = <val>` |
| `store <val> in <var>` | Logic | `<var> = <val>` |
| `display <expr>` | Logic | `print(<expr>)` |
| `ask <prompt> and store in <var>` | Logic | `<var> = input()` |
| `if <cond> then:` | Logic | `if <cond>:` |
| `otherwise if <cond> then:` | Logic | `elif <cond>:` |
| `otherwise:` | Logic | `else:` |
| `match <expr>:` | Logic | Pattern matching construct |
| `function <name>(<args>):` | Logic | `def <name>(<args>):` |
| `async function <name>(<args>):` | Logic | `async def <name>(<args>):` |
| `create class <name> extends <base>:` | Logic | `class <name>(<base>):` |
| `create interface <name>:` | Logic | `class <name>:` |
| `raise <Error> with message <msg>` | Logic | `raise <Error>(<msg>)` |
| `read file <path> into <var>` | File I/O | `with open(...) as _f: <var> = _f.read()` |
| `write <data> to file <path>` | File I/O | `with open(...) as _f: _f.write(<data>)` |
| `connect to database <db> as <var>`| DB | `sqlite3.connect(<db>)` |
| `define table <table> with columns ...`| DB | `CREATE TABLE <table> (...)` |
| `start web server on port <port>` | Server | `start_enlang_server(<port>)` |
| `hash <text> with <algo> and store in <v>`| Security | `hashlib.<algo>(...).hexdigest()` |
| `fetch url <url> and store in <var>`| Network | `urllib.request.urlopen(...)` |
| `analyze sentiment of <text> and store in <v>`| NLP | `analyze_sentiment(<text>)` |
| `extract keywords from <text> into <v>`| NLP | `extract_keywords(<text>)` |
| `calculate similarity between <t1> and <t2>`| NLP | `calculate_similarity(<t1>, <t2>)` |

---

**End of Book 1 — EnLang Core Language Reference**
