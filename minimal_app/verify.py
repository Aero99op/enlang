import os
import sys
sys.path.insert(0, r'd:\enlangg')

from enlang_core.web_server import _run_enlg_file

os.chdir(r'd:\enlangg\minimal_app')
html_out = _run_enlg_file('index.enlgf')
css_out = _run_enlg_file('style.enlgd')
js_out = _run_enlg_file('script.enlgs')

print(f"HTML output length: {len(html_out)}")
print(f"CSS output length:  {len(css_out)}")
print(f"JS output length:   {len(js_out)}")

print("\n--- SAMPLE RENDERED HTML ---")
print(html_out[:400])

print("\n--- SAMPLE RENDERED CSS ---")
print(css_out[:300])

print("\n--- SAMPLE RENDERED JS ---")
print(js_out[:300])
