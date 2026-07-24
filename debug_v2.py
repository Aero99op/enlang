import sys
sys.path.insert(0, 'd:/enlangg')

from enlang_core.transpiler import EnLangTranspiler
t = EnLangTranspiler()

# Debug what each line transpiles to
lines = [
    ("define number age as 25", "main.enlg"),
    ('define text username as "Spandan"', "main.enlg"),
    ("define set unique_ids", "main.enlg"),
    ('define dictionary profile as {"name": "Spandan"}', "main.enlg"),
    ('define array tags as ["ai","nlp"]', "main.enlg"),
    ('match role:', "main.enlg"),
    ('case "admin":', "main.enlg"),
    ('default:', "main.enlg"),
    ('raise ValueError with message "Something broke"', "main.enlg"),
]

for line, ext in lines:
    result = t.transpile(line, ext)
    print(f"IN : {line}")
    print(f"OUT: {result}")
    print()
