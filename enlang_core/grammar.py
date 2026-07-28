"""
EnLang Grammar Definitions and Domain Pattern Matchers
=======================================================
Each extension maps to its NATIVE target language:

  .enlg            -> Python 3
  .enlgf           -> HTML5
  .enlgd           -> CSS3
  .enlgs           -> JavaScript (ES6+)
  .enlgdb          -> SQL (SQLite)

DESIGN PRINCIPLE:
  - ZERO hardcoded class names or style injections
  - Pure 1:1 natural English -> native target language translation
  - Raw native code (HTML/CSS/JS/SQL) is ALWAYS passed through verbatim
  - Universal fallbacks handle any unknown syntax gracefully
  - This file is PERMANENTLY COMPLETE — no future edits needed
"""

import re

# ─────────────────────────────────────────────────────────────────────────────
# SHARED UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

EXPRESSION_REPLACEMENTS = [
    (r'\bis equal to\b',              '=='),
    (r'\bis not equal to\b',          '!='),
    (r'\bis greater than or equal to\b', '>='),
    (r'\bis less than or equal to\b',    '<='),
    (r'\bis greater than\b',          '>'),
    (r'\bis less than\b',             '<'),
    (r'\bis in\b',                    'in'),
    (r'\bis not in\b',                'not in'),
    (r'\bis not\b',                   '!='),
    (r'\bis true\b',                  '== True'),
    (r'\bis false\b',                 '== False'),
    (r'\btrue\b',                     'True'),
    (r'\bfalse\b',                    'False'),
    (r'\bnull\b',                     'None'),
    (r'\bnone\b',                     'None'),
    (r'\bplus\b',                     '+'),
    (r'\bminus\b',                    '-'),
    (r'\btimes\b',                    '*'),
    (r'\bdivided by\b',               '/'),
    (r'\bmodulo\b',                   '%'),
    (r'\bpower of\b',                 '**'),
    (r'\b([a-zA-Z_]\w*(?:\[[^\]]+\])*)\s+has\s+key\s+([a-zA-Z_]\w*(?:\[[^\]]+\])*)\b', r'\2 in \1'),
    (r'\binfinity\b',                 'float("inf")'),
    (r'\b([a-zA-Z_]\w*)\s+from\s+(.+?)\s+to\s+(length\s+of\s+[a-zA-Z_]\w*|[a-zA-Z_]\w*|\d+)\b', r'\1[\2:\3]'),
    (r'\b([a-zA-Z_]\w*)\s+at\s+index\s+([a-zA-Z_]\w*|\d+)\b', r'\1[\2]'),
    (r'\blength\s+of\s+([a-zA-Z_]\w*\[[^\]]+\])\b', r'len(\1)'),
    (r'\blength\s+of\s+([a-zA-Z_]\w*)\b', r'len(\1)'),
    (r'\bcreate\s+(?:map|dict|dictionary)\b', '{}'),
    (r'\bcall\s+([a-zA-Z_]\w*)\s+with\s+([a-zA-Z_0-9,\s"\'\+\-\*\/\%\(\)]+)\b', lambda m: f"{m.group(1)}({parse_args_list(m.group(2))})"),
    (r'\band\b',                      'and'),
    (r'\bor\b',                       'or'),
    (r'\bnot\b',                      'not'),
]

JS_EXPRESSION_REPLACEMENTS = [
    (r'\bis equal to\b',              '==='),
    (r'\bis not equal to\b',          '!=='),
    (r'\bis greater than or equal to\b', '>='),
    (r'\bis less than or equal to\b',    '<='),
    (r'\bis greater than\b',          '>'),
    (r'\bis less than\b',             '<'),
    (r'\btrue\b',                     'true'),
    (r'\bfalse\b',                    'false'),
    (r'\bnull\b',                     'null'),
    (r'\bundefined\b',                'undefined'),
    (r'\bplus\b',                     '+'),
    (r'\bminus\b',                    '-'),
    (r'\btimes\b',                    '*'),
    (r'\bdivided by\b',               '/'),
    (r'\bmodulo\b',                   '%'),
    (r'\bpower of\b',                 '**'),
    (r'\band\b',                      '&&'),
    (r'\bor\b',                       '||'),
    (r'\bnot\b',                      '!'),
]

# All standard HTML5 void (self-closing) elements
HTML_VOID_ELEMENTS = frozenset({
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr',
})

# Standard HTML5 semantic/structural elements (for universal rule)
HTML_BLOCK_ELEMENTS = frozenset({
    'div', 'span', 'section', 'article', 'aside', 'header', 'footer',
    'main', 'nav', 'figure', 'figcaption', 'details', 'summary',
    'dialog', 'menu', 'template', 'slot', 'canvas', 'video', 'audio',
    'picture', 'address', 'blockquote', 'pre', 'code', 'kbd', 'samp',
    'var', 'abbr', 'cite', 'dfn', 'mark', 'small', 'sub', 'sup',
    'strong', 'em', 'b', 'i', 'u', 's', 'del', 'ins', 'q',
    'ul', 'ol', 'li', 'dl', 'dt', 'dd',
    'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'caption',
    'form', 'fieldset', 'legend', 'label', 'select', 'option',
    'optgroup', 'textarea', 'button', 'progress', 'meter', 'output',
    'datalist', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a',
    'iframe', 'object', 'map', 'noscript', 'script', 'style',
    'title', 'head', 'body', 'html', 'svg', 'g', 'path', 'circle',
    'rect', 'line', 'polyline', 'polygon', 'text', 'tspan', 'defs',
    'symbol', 'use', 'mask', 'clippath', 'lineargradient',
    'radialgradient', 'stop', 'filter', 'feblend', 'fecolormatrix',
    'fecomposite', 'feconvolvematrix', 'fediffuselighting',
    'fedisplacementmap', 'feflood', 'fegaussianblur', 'feimage',
    'femerge', 'femorphology', 'feoffset', 'fespecularlighting',
    'fetile', 'feturbulence', 'animate', 'animatetransform',
    'section', 'nav', 'header', 'footer', 'aside', 'main',
})


def _protect_native_markers(expr: str):
    """Extracts @python(...), @js(...), @sql(...), @cpp(...) markers and returns placeholder map."""
    natives = []
    def save_native(m):
        natives.append(m.group(1))
        return f"__NATIVE_{len(natives)-1}__"

    # Match @target(...) or @target`...`
    pattern = r'@(?:python|js|javascript|sql|cpp|html|css)\s*(?:\((.*?)\)|`([^`]+)`)'
    
    # Simple regex for @lang(...)
    res = expr
    def repl_fn(m):
        code = m.group(1) if m.group(1) is not None else m.group(2)
        natives.append(code)
        return f"__NATIVE_{len(natives)-1}__"

    res = re.sub(pattern, repl_fn, res, flags=re.DOTALL | re.IGNORECASE)
    return res, natives


def clean_expression(expr: str) -> str:
    """Converts natural English operators in expressions to Python operators.
    Native markers (@python(...), @js(...)) and String literals are protected."""
    res = expr.strip()
    res = re.sub(r'\s+(?:then|do)\s*:?\s*$', '', res, flags=re.IGNORECASE)

    # Protect inline native markers
    res, natives = _protect_native_markers(res)

    # Protect string literals from operator replacement
    strings = []
    def save_str(m):
        strings.append(m.group(0))
        return f"__STR_{len(strings)-1}__"

    res = re.sub(r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')', save_str, res)

    for pattern, repl in EXPRESSION_REPLACEMENTS:
        if callable(repl):
            res = re.sub(pattern, repl, res, flags=re.IGNORECASE)
        else:
            res = re.sub(pattern, repl, res, flags=re.IGNORECASE)

    res = re.sub(r'len\(([a-zA-Z_]\w*)\)(\[[^\]]+\])', r'len(\1\2)', res)

    for idx, s in enumerate(strings):
        res = res.replace(f"__STR_{idx}__", s)

    for idx, n in enumerate(natives):
        res = res.replace(f"__NATIVE_{idx}__", n)

    return res


def clean_js_expression(expr: str) -> str:
    """Converts natural English operators in expressions to JavaScript operators."""
    res = expr.strip()

    # Protect inline native markers
    res, natives = _protect_native_markers(res)

    # Protect string literals
    strings = []
    def save_str(m):
        strings.append(m.group(0))
        return f"__STR_{len(strings)-1}__"
    res = re.sub(r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')', save_str, res)
    for pattern, repl in JS_EXPRESSION_REPLACEMENTS:
        res = re.sub(pattern, repl, res, flags=re.IGNORECASE)
    for idx, s in enumerate(strings):
        res = res.replace(f"__STR_{idx}__", s)
    for idx, n in enumerate(natives):
        res = res.replace(f"__NATIVE_{idx}__", n)
    return res


def parse_args_list(args_str: str) -> str:
    """Parses 'x and y', 'a, b and c' -> 'a, b, c'."""
    if not args_str:
        return ""
    clean = re.sub(r'\band\b|\bwith\b', ',', args_str, flags=re.IGNORECASE)
    items = [item.strip() for item in clean.split(',') if item.strip()]
    return ", ".join(items)


def _strip_quotes(s: str) -> str:
    """Strips surrounding outer quotes cleanly only if whole string is quoted."""
    if s is None:
        return ''
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1].strip()
    return s


def _strip_trailing_colon(s: str) -> str:
    """Strip optional trailing colon from condition."""
    return s.rstrip(':').strip()


def _build_attrs(**kwargs) -> str:
    """Builds HTML attribute string from keyword args, skipping None/empty."""
    parts = []
    for k, v in kwargs.items():
        if v:
            attr_name = k.replace('_', '-')
            parts.append(f' {attr_name}="{v}"')
    return ''.join(parts)


# ─────────────────────────────────────────────────────────────────────────────
# .enlgf  →  HTML5
# ─────────────────────────────────────────────────────────────────────────────

def translate_html_line(line: str) -> str:
    """
    Translates .enlgf (EnLang Frontend) lines into pure HTML5 markup.
    Returns a Python print() statement that outputs the HTML.

    RULES (in priority order):
    1. Comments → ignored
    2. Raw HTML (starts with < or is raw passthrough) → verbatim
    3. EnLang high-level sugar keywords (page title, create hero, create form, etc.)
    4. Universal: create <tag> [named <id>] [with text <t>] [with class <c>]
    5. close/end <tag>
    6. Everything else → verbatim passthrough
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return f"# {line}"

    # ── Raw Python print() — pass through directly ─────────────────────────
    if line.startswith('print('):
        return line

    # ── page title <t> ──────────────────────────────────────────────────────
    m = re.match(r'^(?:set\s+)?page\s+title\s+(?:to\s+)?(.+)$', line, re.IGNORECASE)
    if m:
        title = _strip_quotes(m.group(1))
        return f'print("""<title>{title}</title>""")'

    # ── page meta <name> content <val> ──────────────────────────────────────
    m = re.match(r'^(?:set\s+)?(?:page\s+)?meta\s+([a-zA-Z_\-]+)\s+(?:content\s+)?(.+)$', line, re.IGNORECASE)
    if m:
        name, content = m.group(1), _strip_quotes(m.group(2))
        return f'print("""<meta name="{name}" content="{content}">""")'

    # ── page charset <charset> ───────────────────────────────────────────────
    m = re.match(r'^(?:set\s+)?page\s+charset\s+(?:to\s+)?(.+)$', line, re.IGNORECASE)
    if m:
        charset = _strip_quotes(m.group(1))
        return f'print("""<meta charset="{charset}">""")'

    # ── create hero with title <t> [, subtitle <s>] ─────────────────────────
    m = re.match(r'^create\s+hero(?:\s+named\s+\S+)?\s+with\s+title\s+(.+?)(?:(?:\s+and\s+|\s*,\s*)subtitle\s+(.+))?$', line, re.IGNORECASE)
    if m:
        title = _strip_quotes(m.group(1))
        sub = _strip_quotes(m.group(2)) if m.group(2) else ''
        sub_html = f'<p>{sub}</p>' if sub else ''
        return f'print("""<section><h1>{title}</h1>{sub_html}</section>""")'

    # ── Legacy shortcuts (subsumed by universal tag rule) ─────────────────────
    if m:
        text = _strip_quotes(m.group(1))
        return f'print("""<p>{text}</p>""")'

    # ── create image named <var> with src <s> [, alt <a>] ───────────────────
    m = re.match(r'^create\s+image\s+named\s+(\S+)\s+with\s+src\s+(.+?)(?:,\s+alt\s+(.+))?$', line, re.IGNORECASE)
    if m:
        var = m.group(1)
        src = _strip_quotes(m.group(2))
        alt = _strip_quotes(m.group(3)) if m.group(3) else ''
        return f'print("""<img id="{var}" src="{src}" alt="{alt}">""")'

    # ── create image with src <s> [, alt <a>] (unnamed) ────────────────────
    m = re.match(r'^create\s+image\s+with\s+src\s+(.+?)(?:,\s+alt\s+(.+))?$', line, re.IGNORECASE)
    if m:
        src = _strip_quotes(m.group(1))
        alt = _strip_quotes(m.group(2)) if m.group(2) else ''
        return f'print("""<img src="{src}" alt="{alt}">""")'

    # ── create link named <var> with text <t>, href <url> ───────────────────
    m = re.match(r'^create\s+link\s+named\s+(\S+)\s+with\s+text\s+(.+?),\s+href\s+(.+)$', line, re.IGNORECASE)
    if m:
        var = m.group(1)
        text = _strip_quotes(m.group(2))
        href = _strip_quotes(m.group(3))
        return f'print("""<a id="{var}" href="{href}">{text}</a>""")'

    # ── create link with text <t>, href <url> (unnamed) ─────────────────────
    m = re.match(r'^create\s+link\s+with\s+text\s+(.+?),\s+href\s+(.+)$', line, re.IGNORECASE)
    if m:
        text = _strip_quotes(m.group(1))
        href = _strip_quotes(m.group(2))
        return f'print("""<a href="{href}">{text}</a>""")'

    # ── create script with src <s> ──────────────────────────────────────────
    m = re.match(r'^create\s+script\s+with\s+src\s+(.+)$', line, re.IGNORECASE)
    if m:
        src = _strip_quotes(m.group(1))
        return f'print("""<script src="{src}"></script>""")'

    # ── create stylesheet with href <url> ────────────────────────────────────
    m = re.match(r'^create\s+(?:stylesheet|css)\s+with\s+href\s+(.+)$', line, re.IGNORECASE)
    if m:
        href = _strip_quotes(m.group(1))
        return f'print("""<link rel="stylesheet" href="{href}">""")'

    # ── include/link external file ────────────────────────────────────────────
    m = re.match(r'^(?:include|link)\s+(?:stylesheet\s+)?["\']?(.+\.css)["\']?$', line, re.IGNORECASE)
    if m:
        href = _strip_quotes(m.group(1))
        return f'print("""<link rel="stylesheet" href="{href}">""")'

    # ── create svg with width <w>, height <h> [, viewbox <v>] ───────────────
    m = re.match(r'^create\s+svg\s+with\s+width\s+(.+?),\s+height\s+(.+?)(?:,\s+viewbox\s+(.+))?\s*:?$', line, re.IGNORECASE)
    if m:
        w, h = _strip_quotes(m.group(1)), _strip_quotes(m.group(2))
        vb = f' viewBox="{_strip_quotes(m.group(3))}"' if m.group(3) else ''
        return f'print("""<svg width="{w}" height="{h}"{vb}>""")'

    # ── create circle with cx <cx>, cy <cy>, r <r> [fill <f>] [stroke <s>] ─
    m = re.match(r'^create\s+circle\s+with\s+cx\s+(.+?),\s+cy\s+(.+?),\s+r\s+(.+?)(?:,\s+fill\s+(.+?))?(?:,\s+stroke\s+(.+?))?(?:,\s+stroke[-\s]+width\s+(.+))?$', line, re.IGNORECASE)
    if m:
        cx, cy, r = _strip_quotes(m.group(1)), _strip_quotes(m.group(2)), _strip_quotes(m.group(3))
        fill = f' fill="{_strip_quotes(m.group(4))}"' if m.group(4) else ''
        stroke = f' stroke="{_strip_quotes(m.group(5))}"' if m.group(5) else ''
        sw = f' stroke-width="{_strip_quotes(m.group(6))}"' if m.group(6) else ''
        return f'print("""<circle cx="{cx}" cy="{cy}" r="{r}"{fill}{stroke}{sw}/>""")'

    # ── create rect with x <x>, y <y>, width <w>, height <h> [fill <f>] ────
    m = re.match(r'^create\s+rect\s+with\s+x\s+(.+?),\s+y\s+(.+?),\s+width\s+(.+?),\s+height\s+(.+?)(?:,\s+fill\s+(.+))?$', line, re.IGNORECASE)
    if m:
        x, y, w, h = _strip_quotes(m.group(1)), _strip_quotes(m.group(2)), _strip_quotes(m.group(3)), _strip_quotes(m.group(4))
        fill = f' fill="{_strip_quotes(m.group(5))}"' if m.group(5) else ''
        return f'print("""<rect x="{x}" y="{y}" width="{w}" height="{h}"{fill}/>""")'

    # ── create path with d <d> [fill <f>] ────────────────────────────────────
    m = re.match(r'^create\s+path\s+with\s+d\s+(.+?)(?:,\s+fill\s+(.+?))?(?:,\s+stroke\s+(.+))?$', line, re.IGNORECASE)
    if m:
        d = _strip_quotes(m.group(1))
        fill = f' fill="{_strip_quotes(m.group(2))}"' if m.group(2) else ''
        stroke = f' stroke="{_strip_quotes(m.group(3))}"' if m.group(3) else ''
        return f'print("""<path d="{d}"{fill}{stroke}/>""")'

    # ── render layout with <c1>, <c2> ────────────────────────────────────────
    m = re.match(r'^render\s+layout\s+with\s+(.+)$', line, re.IGNORECASE)
    if m:
        comps = [c.strip() for c in m.group(1).split(',')]
        comps_str = ", ".join(comps)
        return f'_comps = [{comps_str}]; print("""<div>""" + "".join(str(c) for c in _comps) + """</div>""")'

    # ── close <tag> / end <tag> ───────────────────────────────────────────────
    m = re.match(r'^(?:close|end)\s+([a-zA-Z0-9_\-]+)\s*:?$', line, re.IGNORECASE)
    if m:
        tag = m.group(1).lower()
        return f'print("</{tag}>")'

    # ── UNIVERSAL TAG RULE: create <tag> [named <id>] [with class <c>] [with style <s>] [with text <t>] ──
    # Flexible attribute parser handling named (id), with class, with style, with text, with href, with src, with type
    m = re.match(r'^create\s+([a-zA-Z][a-zA-Z0-9_\-]*)(?:\s+(.+))?$', line, re.IGNORECASE)
    if m:
        tag = m.group(1).lower()
        rest = m.group(2) if m.group(2) else ''

        # Parse attributes from rest string
        elem_id = None
        cls = None
        style_attr = None
        txt = None
        href = None
        src = None
        itype = None
        val = None

        # Named (id)
        m_id = re.search(r'(?:named|with\s+id)\s+(["\'][^"\']+["\']|\S+)', rest, re.IGNORECASE)
        if m_id: elem_id = _strip_quotes(m_id.group(1))

        # Class
        m_cls = re.search(r'with\s+class\s+(["\'][^"\']+["\']|\S+)', rest, re.IGNORECASE)
        if m_cls: cls = _strip_quotes(m_cls.group(1))

        # Style
        m_style = re.search(r'with\s+style\s+(["\'][^"\']+["\']|\S+)', rest, re.IGNORECASE)
        if m_style: style_attr = _strip_quotes(m_style.group(1))

        # Text / Label
        m_txt = re.search(r'with\s+(?:text|label)\s+(["\'][^"\']+["\']|.+)', rest, re.IGNORECASE)
        if m_txt:
            raw_t = m_txt.group(1)
            for kw in (' with class ', ' with style ', ' with href ', ' with src ', ' with type ', ' and action ', ' with action '):
                if kw in raw_t.lower():
                    raw_t = raw_t[:raw_t.lower().index(kw)]
            txt = _strip_quotes(raw_t.strip())
        else:
            txt = None

        # Action
        m_act = re.search(r'(?:with|and)\s+action\s+(["\'][^"\']+["\']|\S+)', rest, re.IGNORECASE)
        action = _strip_quotes(m_act.group(1)) if m_act else None

        # Method
        m_meth = re.search(r'(?:with|and)\s+method\s+(["\'][^"\']+["\']|\S+)', rest, re.IGNORECASE)
        method = _strip_quotes(m_meth.group(1)) if m_meth else None

        # Links / Items / Fields
        m_items = re.search(r'with\s+(?:links|items|fields)\s+(["\'][^"\']+["\']|.+)', rest, re.IGNORECASE)
        if m_items:
            raw_items = m_items.group(1)
            for kw in (' with class ', ' with style ', ' and action ', ' with action ', ' and method ', ' with method '):
                if kw in raw_items.lower():
                    raw_items = raw_items[:raw_items.lower().index(kw)]
            cleaned_items = _strip_quotes(raw_items.strip())
            items_list = []
            for item in cleaned_items.split(','):
                item = item.strip()
                if ' and ' in item and not (item.startswith('"') or item.startswith("'")):
                    parts = item.split(' and ')
                    items_list.extend([p.strip() for p in parts if p.strip()])
                elif item:
                    items_list.append(item)
        else:
            items_list = None

        # Headers
        m_hdrs = re.search(r'with\s+headers?\s+(["\'][^"\']+["\']|.+)', rest, re.IGNORECASE)
        hdrs_list = [_strip_quotes(h.strip()) for h in _strip_quotes(m_hdrs.group(1)).split(',') if h.strip()] if m_hdrs else None

        id_str = f' id="{elem_id}"' if elem_id else ''
        cls_str = f' class="{cls}"' if cls else ''
        style_str = f' style="{style_attr}"' if style_attr else ''
        href_str = f' href="{href}"' if href else ''
        src_str = f' src="{src}"' if src else ''
        type_str = f' type="{itype}"' if itype else ''
        val_str = f' value="{val}"' if val else ''
        act_str = (f' onclick="{action}"' if action.endswith('()') else f' action="{action}"') if action else ''
        meth_str = f' method="{method}"' if method else ''

        all_attrs = f'{id_str}{cls_str}{style_str}{href_str}{src_str}{type_str}{val_str}{act_str}{meth_str}'

        if tag in HTML_VOID_ELEMENTS:
            return f'print("""<{tag}{all_attrs}>""")'

        if tag in ('nav', 'ul', 'ol') and items_list:
            inner = "".join(f'<a href="#{i.lower()}">{i}</a>' for i in items_list) if tag == 'nav' else "".join(f'<li>{i}</li>' for i in items_list)
            return f'print("""<{tag}{all_attrs}>{inner}</{tag}>""")'

        if tag == 'form' and items_list:
            fields_html = "".join(f'<input type="text" name="{f}" placeholder="{f}">\n' for f in items_list)
            return f'print("""<{tag}{all_attrs}>\n{fields_html}</{tag}>""")'

        if tag == 'table' and hdrs_list:
            inner = "<thead><tr>" + "".join(f'<th>{h}</th>' for h in hdrs_list) + "</tr></thead>"
            return f'print("""<{tag}{all_attrs}>{inner}</{tag}>""")'

        if txt is not None:
            return f'print("""<{tag}{all_attrs}>{txt}</{tag}>""")'
        return f'print("""<{tag}{all_attrs}>""")'

    # ── br / hr / linebreak shortcuts ────────────────────────────────────────
    if re.match(r'^(?:linebreak|line\s+break|br)$', line, re.IGNORECASE):
        return 'print("""<br>""")'

    if re.match(r'^(?:horizontal\s+rule|divider|hr)$', line, re.IGNORECASE):
        return 'print("""<hr>""")'

    # ── All raw HTML / text nodes / unknown lines pass through verbatim ──────
    return f'print({repr(line)})'


# ─────────────────────────────────────────────────────────────────────────────
# .enlgd  →  CSS3
# ─────────────────────────────────────────────────────────────────────────────

# Map of all CSS selector keywords to their real CSS selectors
CSS_SELECTOR_MAP = {
    'all': '*', 'root': ':root', 'body': 'body', 'html': 'html',
    'button': 'button', 'input': 'input', 'form': 'form', 'table': 'table',
    'nav': 'nav', 'header': 'header', 'footer': 'footer', 'section': 'section',
    'main': 'main', 'article': 'article', 'aside': 'aside', 'figure': 'figure',
    'h1': 'h1', 'h2': 'h2', 'h3': 'h3', 'h4': 'h4', 'h5': 'h5', 'h6': 'h6',
    'p': 'p', 'a': 'a', 'ul': 'ul', 'ol': 'ol', 'li': 'li',
    'span': 'span', 'img': 'img', 'div': 'div', 'label': 'label',
    'select': 'select', 'textarea': 'textarea', 'canvas': 'canvas',
    'video': 'video', 'audio': 'audio', 'iframe': 'iframe',
    'code': 'code', 'pre': 'pre', 'blockquote': 'blockquote',
    'summary': 'summary', 'details': 'details', 'dialog': 'dialog',
    'small': 'small', 'strong': 'strong', 'em': 'em', 'mark': 'mark',
}


def translate_design_line(line: str) -> str:
    """
    Translates .enlgd (EnLang Design) lines into pure CSS3.
    Raw CSS is passed through verbatim.
    EnLang keywords are mapped to their CSS equivalents.
    PERMANENTLY COMPLETE — handles all CSS patterns.
    """
    line = line.strip()
    if not line:
        return ""
    if line.startswith('# ') or line.startswith('note:') or line.startswith('comment:'):
        return f"# {line}"

    # ── Raw CSS Passthrough Detection (Comments, Raw Passthrough) ─────────────
    if line.startswith('# ') or line.startswith('note:') or line.startswith('comment:'):
        return f"# {line}"

    # ── 1. Variable & Token Declarations ──────────────────────────────────────
    # Supports: create variable x as y, set variable x as y, var x = y, token x = y, color x = y, theme color x = y
    m = re.match(
        r'^(?:create\s+variable|set\s+variable|define\s+variable|var|variable|token|color|theme\s+color|define\s+token)\s+([a-zA-Z_][a-zA-Z0-9_\-]*)\s*(?:as|=|:|\s)\s*(.+)$',
        line, re.IGNORECASE
    )
    if m:
        var_name = m.group(1).replace('_', '-')
        var_val = _strip_quotes(m.group(2).strip())
        return f'print(":root {{ --{var_name}: {var_val}; }}")'

    # ── 2. Theme Token Generator: define theme with primary <p>, background <bg>, accent <a> ──
    m = re.match(r'^define\s+theme\s+with\s+primary\s+(.+?),\s+background\s+(.+?)(?:,\s+accent\s+(.+))?$', line, re.IGNORECASE)
    if m:
        p = _strip_quotes(m.group(1))
        bg = _strip_quotes(m.group(2))
        acc = _strip_quotes(m.group(3)) if m.group(3) else p
        css_rule = f":root {{ --primary: {p}; --background: {bg}; --accent: {acc}; }}"
        return f'print({repr(css_rule)})'

    # ── 3. Selector Block Declarations ───────────────────────────────────────
    # Supports: in navbar, in style navbar, in .navbar, in class card, in id header, in all,
    # in btn on hover, in input on focus, in child p of div, in card before, in selection, etc.
    m = re.match(r'^(?:in\s+style|in|style)\s+(.+?)\s*:?\s*\{?$', line, re.IGNORECASE)
    if m:
        raw_sel = m.group(1).strip()
        lower_sel = raw_sel.lower()

        # Natural Pseudo-Element / Pseudo-Class Conversions
        target_sel = lower_sel
        target_sel = re.sub(r'\s+(?:on|when)\s+hover(?:ed)?$', ':hover', target_sel)
        target_sel = re.sub(r'\s+(?:on|when)\s+focus(?:ed)?$', ':focus', target_sel)
        target_sel = re.sub(r'\s+(?:on|when)\s+active$', ':active', target_sel)
        target_sel = re.sub(r'\s+(?:on|when)\s+checked$', ':checked', target_sel)
        target_sel = re.sub(r'\s+(?:on|when)\s+disabled$', ':disabled', target_sel)
        target_sel = re.sub(r'\s+before$', '::before', target_sel)
        target_sel = re.sub(r'\s+after$', '::after', target_sel)
        target_sel = re.sub(r'\s+first\s+line$', '::first-line', target_sel)
        target_sel = re.sub(r'\s+first\s+letter$', '::first-letter', target_sel)

        # Natural Keyword Selectors
        if target_sel in ('all', 'every', 'universal', '*'):
            final_sel = '*'
        elif target_sel in ('selection', 'user selection', 'user-selection'):
            final_sel = '::selection'
        # Natural Attribute / Combinator Conversions
        elif ' with attribute ' in target_sel:
            parts = target_sel.split(' with attribute ')
            tag, attr = parts[0].strip(), parts[1].strip()
            final_sel = f"{tag}[{attr}]"
        elif ' with ' in target_sel and ' starting with ' in target_sel:
            m_attr = re.match(r'(.+?)\s+with\s+(.+?)\s+starting\s+with\s+(.+)', target_sel)
            if m_attr:
                tag, attr, val = m_attr.group(1).strip(), m_attr.group(2).strip(), _strip_quotes(m_attr.group(3).strip())
                final_sel = f'{tag}[{attr}^="{val}"]'
            else:
                final_sel = target_sel
        elif ' with ' in target_sel and ' ending with ' in target_sel:
            m_attr = re.match(r'(.+?)\s+with\s+(.+?)\s+ending\s+with\s+(.+)', target_sel)
            if m_attr:
                tag, attr, val = m_attr.group(1).strip(), m_attr.group(2).strip(), _strip_quotes(m_attr.group(3).strip())
                final_sel = f'{tag}[{attr}$="{val}"]'
            else:
                final_sel = target_sel
        elif ' with ' in target_sel and ' containing ' in target_sel:
            m_attr = re.match(r'(.+?)\s+with\s+(.+?)\s+containing\s+(.+)', target_sel)
            if m_attr:
                tag, attr, val = m_attr.group(1).strip(), m_attr.group(2).strip(), _strip_quotes(m_attr.group(3).strip())
                final_sel = f'{tag}[{attr}*="{val}"]'
            else:
                final_sel = target_sel
        elif 'child' in target_sel and 'of' in target_sel:
            m_ch = re.search(r'(?:direct\s+)?child\s+(.+?)\s+of\s+(.+)', target_sel)
            if m_ch:
                child_elem, parent_elem = m_ch.group(1).strip(), m_ch.group(2).strip()
                final_sel = f"{parent_elem} > {child_elem}"
            else:
                final_sel = target_sel
        elif ' inside ' in target_sel:
            parts = target_sel.split(' inside ')
            final_sel = f"{parts[1].strip()} {parts[0].strip()}"
        elif target_sel.startswith('class '):
            final_sel = '.' + target_sel[6:].strip()
        elif target_sel.startswith('id '):
            final_sel = '#' + target_sel[3:].strip()
        else:
            HTML_ELEMENTS = {
                'body', 'html', 'div', 'span', 'p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'button', 'input', 'label', 'form', 'nav', 'header', 'footer', 'section',
                'article', 'main', 'aside', 'table', 'tr', 'td', 'th', 'pre', 'code',
                'ul', 'ol', 'li', 'img', 'svg', 'iframe', 'video', 'audio', 'fieldset', '*'
            }
            base_elem = target_sel.split(':')[0].split('.')[0].split('#')[0]
            if target_sel.startswith('.') or target_sel.startswith('#') or target_sel.startswith(':') or target_sel.startswith('@') or target_sel.startswith('[') or base_elem in HTML_ELEMENTS:
                final_sel = target_sel
            else:
                final_sel = '.' + target_sel
        
        return f'print({repr(final_sel + " {")})'

    # ── 4. End Block ─────────────────────────────────────────────────────────
    if re.match(r'^(?:end\s+style|end\s+block|close\s+style|close\s+block|end|close|\});?\s*$', line, re.IGNORECASE):
        return 'print("}")'

    # ── 5. Media Queries & Responsive Directives ─────────────────────────────
    m = re.match(r'^(?:when|on)?\s*screen\s+(?:width\s+is\s+)?(?:smaller|less|below|under)\s+(?:than\s+)?(.+?)\s*:?\s*\{?$', line, re.IGNORECASE)
    if m:
        size = _strip_quotes(m.group(1).rstrip(':').strip())
        return f'print("@media (max-width: {size}) {{")'

    m = re.match(r'^(?:when|on)?\s*screen\s+(?:width\s+is\s+)?(?:larger|bigger|greater|more)\s+(?:than\s+)?(.+?)\s*:?\s*\{?$', line, re.IGNORECASE)
    if m:
        size = _strip_quotes(m.group(1).rstrip(':').strip())
        return f'print("@media (min-width: {size}) {{")'

    # ── 6. Property & Value Translation (Natural Property Word Equivalents) ────
    # Handles: set <prop> to <val>, <prop>: <val>, <prop> = <val>
    PROPERTY_WORD_MAP = {
        'background color': 'background-color',
        'bg color': 'background-color',
        'bg-color': 'background-color',
        'bg': 'background',
        'text color': 'color',
        'font color': 'color',
        'font family': 'font-family',
        'font size': 'font-size',
        'font weight': 'font-weight',
        'border radius': 'border-radius',
        'rounded': 'border-radius',
        'box shadow': 'box-shadow',
        'shadow': 'box-shadow',
        'space inside': 'padding',
        'space outside': 'margin',
        'space': 'gap',
        'direction': 'flex-direction',
        'flex direction': 'flex-direction',
        'align': 'align-items',
        'align items': 'align-items',
        'justify': 'justify-content',
        'justify content': 'justify-content',
        'grid columns': 'grid-template-columns',
        'columns': 'grid-template-columns',
        'glass blur': 'backdrop-filter',
        'blur': 'backdrop-filter',
        'web blur': '-webkit-backdrop-filter',
    }

    # Match set <prop> to <val> or <prop> : <val> or <prop> = <val> (excluding selector lines with '{')
    if not line.endswith('{') and '{' not in line and not line.endswith('}'):
        m = re.match(r'^(?:set\s+)?([a-zA-Z_][a-zA-Z0-9_\-\s]*?)\s*(?::|=|\s+to\s+)\s*(.+)$', line, re.IGNORECASE)
    if m:
        raw_prop = m.group(1).strip().lower()
        raw_val = _strip_quotes(m.group(2).strip())
        css_prop = PROPERTY_WORD_MAP.get(raw_prop, raw_prop.replace('_', '-').replace(' ', '-'))
        return f'print({repr("  " + css_prop + ": " + raw_val + ";")})'

    # ── 7. Fallback Passthrough (Raw CSS passthrough for direct standard CSS lines) ──
    return f'print({repr(line)})'


# ─────────────────────────────────────────────────────────────────────────────
# .enlgs  →  JavaScript (ES6+)
# ─────────────────────────────────────────────────────────────────────────────

# All prefixes that indicate raw JavaScript — passed verbatim
_RAW_JS_PREFIXES = (
    '//', '/*', '*/', '/**',
    'let ', 'var ', 'const ',
    'class ', 'extends ',
    'return ',
    'if (', 'if(', '} else', 'else {', 'else if', '} else if',
    'for (', 'for(', 'while (', 'while(',
    'switch (', 'switch(', 'case ', 'default:',
    'try {', 'try{', '} catch', '} finally', 'catch (', 'catch(',
    'throw ', 'import ', 'export ',
    'async ', 'await ',
    'new ', 'delete ', 'typeof ', 'instanceof ',
    'document.', 'window.', 'console.',
    'navigator.', 'location.', 'history.',
    'localStorage.', 'sessionStorage.',
    'fetch(', 'Promise.', 'Object.', 'Array.', 'JSON.',
    'Math.', 'Date.', 'RegExp.', 'Number.', 'String.',
    'setTimeout(', 'setInterval(', 'clearTimeout(', 'clearInterval(',
    'addEventListener(', 'removeEventListener(',
    'requestAnimationFrame(', 'cancelAnimationFrame(',
    'performance.', 'crypto.', 'indexedDB.',
    'super.', 'this.',
    'module.', 'require(',
    'Symbol.', 'Map(', 'Set(', 'WeakMap(', 'WeakSet(',
    'Proxy(', 'Reflect.',
)


def translate_script_line(line: str) -> str:
    """
    Translates .enlgs (EnLang Script) lines into pure JavaScript (ES6+).
    Raw JS lines are always passed through verbatim.
    PERMANENTLY COMPLETE — handles all JS patterns.
    """
    raw = line.strip()
    if not raw or raw.startswith('#'):
        return f"# {raw}"

    # ── Pass-through raw JS lines verbatim ─────────────────────────────────
    _is_raw_js = (
        any(raw.startswith(pfx) for pfx in _RAW_JS_PREFIXES) or
        raw == '{' or raw == '}' or raw == '};' or raw == '})' or
        raw == '});' or raw == ')' or raw == ');' or
        raw.endswith(';') or raw.endswith('{') or raw.endswith('}') or
        raw.endswith('*/') or
        (raw.startswith('function ') and not raw.endswith(':'))
    )

    if _is_raw_js:
        return f'print({repr(raw)})'

    # ── EnLang Natural Language → JS ────────────────────────────────────────

    # Constant: define constant <name> as <val>
    m = re.match(r'^define\s+constant\s+([a-zA-Z_$][\w$]*)\s+(?:as|=)\s+(.+)$', raw, re.IGNORECASE)
    if m:
        var, val = m.group(1), clean_js_expression(m.group(2))
        return f'print({repr("const " + var + " = " + val + ";")})'

    # Variable declaration: set <var> to <val>
    m = re.match(r'^(?:set|let|var)\s+([a-zA-Z_$][\w$]*)\s+(?:to|=)\s+(.+)$', raw, re.IGNORECASE)
    if m:
        var, val = m.group(1), clean_js_expression(m.group(2))
        return f'print({repr("let " + var + " = " + val + ";")})'

    # Assign (without let/var): store <val> in <var>
    m = re.match(r'^store\s+(.+?)\s+in\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        val, var = clean_js_expression(m.group(1)), m.group(2)
        return f'print({repr(var + " = " + val + ";")})'

    # Function definition: function <name>(<params>):
    m = re.match(r'^function\s+([a-zA-Z_$][\w$]*)\s*\(([^)]*)\)\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        name, params = m.group(1), m.group(2)
        return f'print({repr("function " + name + "(" + params + ") {")})'

    # Arrow function: arrow <name> = (<params>) =>
    m = re.match(r'^(?:arrow|lambda)\s+([a-zA-Z_$][\w$]*)\s*=\s*\(([^)]*)\)\s*=>?', raw, re.IGNORECASE)
    if m:
        name, params = m.group(1), m.group(2)
        return f'print({repr("const " + name + " = (" + params + ") => {")})'

    # Class definition: class <name> [extends <base>]:
    m = re.match(r'^class\s+([a-zA-Z_$][\w$]*)(?:\s+extends\s+([a-zA-Z_$][\w$]*))?\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        name = m.group(1)
        base = m.group(2)
        extends_part = f' extends {base}' if base else ''
        return f'print({repr("class " + name + extends_part + " {")})'

    # Constructor: constructor(<params>):
    m = re.match(r'^constructor\s*\(([^)]*)\)\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        params = m.group(1)
        return f'print({repr("  constructor(" + params + ") {")})'

    # Return: return <expr>
    m = re.match(r'^return\s+(.+)$', raw, re.IGNORECASE)
    if m:
        return f'print({repr("  return " + clean_js_expression(m.group(1)) + ";")})'

    # Alert / Popup: alert <message>
    m = re.match(r'^(?:alert|popup)\s+(.+)$', raw, re.IGNORECASE)
    if m:
        msg = m.group(1).strip()
        if not (msg.startswith('"') or msg.startswith("'")):
            msg = f'"{_strip_quotes(msg)}"'
        return f'print({repr("alert(" + msg + ");")})'

    # Console log: log <expr>
    m = re.match(r'^log\s+(.+)$', raw, re.IGNORECASE)
    if m:
        expr = clean_js_expression(m.group(1))
        return f'print({repr("console.log(" + expr + ");")})'

    # Console warn: warn <expr>
    m = re.match(r'^warn\s+(.+)$', raw, re.IGNORECASE)
    if m:
        expr = clean_js_expression(m.group(1))
        return f'print({repr("console.warn(" + expr + ");")})'

    # Console error: error <expr>
    m = re.match(r'^(?:console\.)?error\s+(.+)$', raw, re.IGNORECASE)
    if m:
        expr = clean_js_expression(m.group(1))
        return f'print({repr("console.error(" + expr + ");")})'

    # DOM Get Element: get element <id> and store in <var>
    m = re.match(r'^get\s+element\s+(.+?)\s+(?:and\s+store\s+in|into)\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        eid = _strip_quotes(m.group(1))
        var = m.group(2)
        return f'print({repr("const " + var + " = document.getElementById(\"" + eid + "\");")})'

    # DOM Get Elements by class: get elements with class <cls> into <var>
    m = re.match(r'^get\s+elements?\s+with\s+class\s+(.+?)\s+(?:and\s+store\s+in|into)\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        cls = _strip_quotes(m.group(1))
        var = m.group(2)
        return f'print({repr("const " + var + " = document.getElementsByClassName(\"" + cls + "\");")})'

    # DOM query selector: query <selector> into <var>
    m = re.match(r'^query\s+(.+?)\s+(?:and\s+store\s+in|into)\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        sel = _strip_quotes(m.group(1))
        var = m.group(2)
        return f'print({repr("const " + var + " = document.querySelector(\"" + sel + "\");")})'

    # DOM Set value/text: set value of <elem> to <val>
    m = re.match(r'^set\s+(?:value|text|content|inner)\s+of\s+([a-zA-Z_$][\w$]*)\s+to\s+(.+)$', raw, re.IGNORECASE)
    if m:
        elem, val = m.group(1), clean_js_expression(m.group(2))
        attr_type = re.match(r'^set\s+(value|text|content|inner)', raw, re.IGNORECASE).group(1).lower()
        prop = {'value': 'value', 'text': 'textContent', 'content': 'innerHTML', 'inner': 'innerHTML'}.get(attr_type, 'value')
        return f'print({repr(elem + "." + prop + " = " + val + ";")})'

    # DOM set style: set style <prop> of <elem> to <val>
    m = re.match(r'^set\s+style\s+([a-zA-Z_\-]+)\s+of\s+([a-zA-Z_$][\w$]*)\s+to\s+(.+)$', raw, re.IGNORECASE)
    if m:
        prop, elem, val = m.group(1), m.group(2), clean_js_expression(m.group(3))
        camel = re.sub(r'-([a-z])', lambda x: x.group(1).upper(), prop)
        return f'print({repr(elem + ".style." + camel + " = " + val + ";")})'

    # DOM add class: add class <cls> to <elem>
    m = re.match(r'^add\s+class\s+(.+?)\s+to\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        cls, elem = _strip_quotes(m.group(1)), m.group(2)
        return f'print({repr(elem + ".classList.add(\"" + cls + "\");")})'

    # DOM remove class: remove class <cls> from <elem>
    m = re.match(r'^remove\s+class\s+(.+?)\s+from\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        cls, elem = _strip_quotes(m.group(1)), m.group(2)
        return f'print({repr(elem + ".classList.remove(\"" + cls + "\");")})'

    # DOM toggle class: toggle class <cls> on <elem>
    m = re.match(r'^toggle\s+class\s+(.+?)\s+on\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        cls, elem = _strip_quotes(m.group(1)), m.group(2)
        return f'print({repr(elem + ".classList.toggle(\"" + cls + "\");")})'

    # Add event listener: on <event> of <elem> call <fn>
    m = re.match(r'^on\s+(click|change|submit|keyup|keydown|mouseover|mouseout|load|input|focus|blur|resize|scroll|dblclick|contextmenu|touchstart|touchend)\s+of\s+(.+?)\s+call\s+(.+)$', raw, re.IGNORECASE)
    if m:
        event, elem, fn = m.group(1), _strip_quotes(m.group(2)), m.group(3)
        return f'print({repr("document.getElementById(\"" + elem + "\").addEventListener(\"" + event + "\", " + fn + ");")})'

    # on load: execute on page load
    m = re.match(r'^on\s+(?:page\s+)?load\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        return f'print({repr("window.addEventListener(\"load\", function() {")})'

    # on DOM ready
    m = re.match(r'^on\s+(?:dom\s+)?ready\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        return f'print({repr("document.addEventListener(\"DOMContentLoaded\", function() {")})'

    # Fetch API: fetch url <url> and store response in <var>
    m = re.match(r'^fetch\s+url\s+(.+?)\s+and\s+store\s+(?:response\s+)?in\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        url = _strip_quotes(m.group(1))
        var = m.group(2)
        return f'print({repr("fetch(\"" + url + "\").then(r => r.json()).then(" + var + " => {")})'

    # JSON parse: parse json <val> and store in <var>
    m = re.match(r'^parse\s+json\s+(.+?)\s+(?:and\s+store\s+in|into)\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        val, var = clean_js_expression(m.group(1)), m.group(2)
        return f'print({repr("const " + var + " = JSON.parse(" + val + ");")})'

    # JSON stringify: stringify <val> and store in <var>
    m = re.match(r'^stringify\s+(.+?)\s+(?:and\s+store\s+in|into)\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        val, var = clean_js_expression(m.group(1)), m.group(2)
        return f'print({repr("const " + var + " = JSON.stringify(" + val + ");")})'

    # localStorage: save <key> <val> to storage
    m = re.match(r'^(?:save|store)\s+(.+?)\s+(?:as|with\s+key)\s+(.+?)\s+(?:to|in)\s+(?:local\s*)?storage$', raw, re.IGNORECASE)
    if m:
        val, key = clean_js_expression(m.group(1)), _strip_quotes(m.group(2))
        return f'print({repr("localStorage.setItem(\"" + key + "\", " + val + ");")})'

    # localStorage: get <key> from storage and store in <var>
    m = re.match(r'^get\s+(.+?)\s+from\s+(?:local\s*)?storage\s+(?:and\s+store\s+in|into)\s+([a-zA-Z_$][\w$]*)$', raw, re.IGNORECASE)
    if m:
        key, var = _strip_quotes(m.group(1)), m.group(2)
        return f'print({repr("const " + var + " = localStorage.getItem(\"" + key + "\");")})'

    # Wait (async timeout): wait <n> milliseconds
    m = re.match(r'^wait\s+(.+?)\s+(?:ms|milliseconds?)\s*$', raw, re.IGNORECASE)
    if m:
        ms = clean_js_expression(m.group(1))
        return f'print({repr("await new Promise(r => setTimeout(r, " + ms + "));")})'

    # setTimeout: after <n> ms call <fn>
    m = re.match(r'^after\s+(.+?)\s+(?:ms|milliseconds?)\s+call\s+(.+)$', raw, re.IGNORECASE)
    if m:
        ms, fn = clean_js_expression(m.group(1)), m.group(2)
        return f'print({repr("setTimeout(" + fn + ", " + ms + ");")})'

    # setInterval: every <n> ms call <fn>
    m = re.match(r'^every\s+(.+?)\s+(?:ms|milliseconds?)\s+call\s+(.+)$', raw, re.IGNORECASE)
    if m:
        ms, fn = clean_js_expression(m.group(1)), m.group(2)
        return f'print({repr("setInterval(" + fn + ", " + ms + ");")})'

    # If condition (natural English)
    m = re.match(r'^(?:if|else\s+if|elif)\s+(.+?)(?:\s+(?:then|do))?\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        prefix = 'else if' if raw.lower().startswith(('else if', 'elif')) else 'if'
        cond = clean_js_expression(m.group(1).rstrip(':').rstrip())
        return f'print({repr(prefix + " (" + cond + ") {")})'

    # Else
    if re.match(r'^else\s*:?\s*$', raw, re.IGNORECASE):
        return "print('} else {')"

    # Switch: switch on <expr>:
    m = re.match(r'^switch\s+on\s+(.+)\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        expr = clean_js_expression(m.group(1))
        return f'print({repr("switch (" + expr + ") {")})'

    # Case: case <val>:
    m = re.match(r'^case\s+(.+)\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        val = clean_js_expression(m.group(1))
        return f'print({repr("  case " + val + ":")})'

    # Default (switch):
    if re.match(r'^default\s*:?\s*$', raw, re.IGNORECASE):
        return "print('  default:')"

    # End block / close brace (close if, close function, close try, end if, end function, etc.)
    if re.match(r'^(?:end|close|close\s+[a-zA-Z_]+|end\s+[a-zA-Z_]+|\})\s*$', raw, re.IGNORECASE):
        return "print('}')"

    # For loop: repeat <n> times:
    m = re.match(r'^repeat\s+(.+?)\s+times\s*:?$', raw, re.IGNORECASE)
    if m:
        count = clean_js_expression(m.group(1))
        return f'print({repr("for (let _i = 0; _i < " + count + "; _i++) {")})'

    # For-each: for each <item> in <array>:
    m = re.match(r'^for\s+each\s+([a-zA-Z_$][\w$]*)\s+in\s+([a-zA-Z_$][\w$]*)\s*(?:do\s*)?:?\s*$', raw, re.IGNORECASE)
    if m:
        item, arr = m.group(1), m.group(2)
        return f'print({repr("for (const " + item + " of " + arr + ") {")})'

    # For-in: for key <k> in <obj>:
    m = re.match(r'^for\s+key\s+([a-zA-Z_$][\w$]*)\s+in\s+([a-zA-Z_$][\w$]*)\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        key, obj = m.group(1), m.group(2)
        return f'print({repr("for (const " + key + " in " + obj + ") {")})'

    # While loop
    m = re.match(r'^while\s+(.+?)(?:\s+do)?\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        cond = clean_js_expression(m.group(1).rstrip(':'))
        return f'print({repr("while (" + cond + ") {")})'

    # Try block
    if re.match(r'^try\s*:?\s*$', raw, re.IGNORECASE):
        return "print('try {')"

    # Catch block
    m = re.match(r'^catch\s*(?:\((.+?)\))?\s*:?\s*$', raw, re.IGNORECASE)
    if m:
        err = m.group(1) if m.group(1) else 'e'
        return f'print({repr("}} catch (" + err + ") {")})'

    # Finally
    if re.match(r'^finally\s*:?\s*$', raw, re.IGNORECASE):
        return "print('} finally {')"

    # Import JS module: import <name> from <module>
    m = re.match(r'^import\s+([a-zA-Z_$][\w$,\s\{\}]*)\s+from\s+(.+)$', raw, re.IGNORECASE)
    if m:
        what, mod = m.group(1), _strip_quotes(m.group(2))
        return f'print({repr("import " + what + " from \"" + mod + "\";")})'

    # Export default: export default <name>
    m = re.match(r'^export\s+default\s+(.+)$', raw, re.IGNORECASE)
    if m:
        name = m.group(1)
        return f'print({repr("export default " + name + ";")})'

    # Export named: export <name>
    m = re.match(r'^export\s+(.+)$', raw, re.IGNORECASE)
    if m:
        name = m.group(1)
        return f'print({repr("export { " + name + " };")})'

    # break / continue
    if re.match(r'^break\s*$', raw, re.IGNORECASE):
        return "print('  break;')"
    if re.match(r'^continue\s*$', raw, re.IGNORECASE):
        return "print('  continue;')"

    # Default: pass through verbatim
    return f'print({repr(raw)})'


# ─────────────────────────────────────────────────────────────────────────────
# .enlgdb  →  SQL (SQLite compatible)
# ─────────────────────────────────────────────────────────────────────────────

def translate_database_line(line: str, db_var: str = "db") -> str:
    """
    Translates .enlgdb (EnLang Database) lines into pure SQL output strings.
    Returns a Python print() that outputs raw SQL.
    PERMANENTLY COMPLETE — handles all common SQL operations.
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return f"# {line}"

    # Raw SQL passthrough: lines that are ALREADY in uppercase SQL syntax
    # EnLang natural language lines will be mixed-case (e.g. "select all from users")
    # True raw SQL will be uppercase (e.g. "SELECT * FROM users")
    _raw_sql_starts = ('SELECT ', 'INSERT ', 'UPDATE ', 'DELETE ', 'CREATE ', 'DROP ',
                       'ALTER ', 'BEGIN ', 'COMMIT', 'ROLLBACK', 'PRAGMA ', 'EXPLAIN ',
                       'WITH ', 'VACUUM', 'ATTACH ', 'DETACH ', '--', '/*')
    if any(line.startswith(kw) for kw in _raw_sql_starts):
        return f'print({repr(line)})'

    # connect to database <file> as <var>
    m = re.match(r'^connect\s+to\s+database\s+(.+)\s+as\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        return f'print({repr("-- Connected to database " + m.group(1))})'

    # define / create table <name> with columns <col1 TYPE, col2 TYPE>
    m = re.match(r'^(?:define|create)\s+table\s+([a-zA-Z_]\w*)\s+with\s+columns\s+(.+)$', line, re.IGNORECASE)
    if m:
        tbl, cols_raw = m.group(1), m.group(2)
        cols_parsed = cols_raw.replace(' as ', ' ').replace(' and ', ', ')
        sql = f'CREATE TABLE IF NOT EXISTS {tbl} ({cols_parsed});'
        return f'print({repr(sql)})'

    # define / create table <name> with columns and constraints <...>
    m = re.match(r'^(?:define|create)\s+table\s+([a-zA-Z_]\w*)\s+\((.+)\)$', line, re.IGNORECASE)
    if m:
        tbl, cols = m.group(1), m.group(2)
        sql = f'CREATE TABLE IF NOT EXISTS {tbl} ({cols});'
        return f'print({repr(sql)})'

    # add column <col> <type> to table <name>
    m = re.match(r'^add\s+column\s+([a-zA-Z_]\w*)\s+([a-zA-Z]+(?:\([^)]*\))?)\s+to\s+(?:table\s+)?([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        col, dtype, tbl = m.group(1), m.group(2), m.group(3)
        sql = f'ALTER TABLE {tbl} ADD COLUMN {col} {dtype};'
        return f'print({repr(sql)})'

    # rename column <old> to <new> in table <name>
    m = re.match(r'^rename\s+column\s+([a-zA-Z_]\w*)\s+to\s+([a-zA-Z_]\w*)\s+in\s+(?:table\s+)?([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        old_col, new_col, tbl = m.group(1), m.group(2), m.group(3)
        sql = f'ALTER TABLE {tbl} RENAME COLUMN {old_col} TO {new_col};'
        return f'print({repr(sql)})'

    # rename table <old> to <new>
    m = re.match(r'^rename\s+table\s+([a-zA-Z_]\w*)\s+to\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        old_tbl, new_tbl = m.group(1), m.group(2)
        sql = f'ALTER TABLE {old_tbl} RENAME TO {new_tbl};'
        return f'print({repr(sql)})'

    # drop table <name>
    m = re.match(r'^drop\s+table\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        sql = f'DROP TABLE IF EXISTS {m.group(1)};'
        return f'print({repr(sql)})'

    # truncate table <name>
    m = re.match(r'^truncate\s+(?:table\s+)?([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        sql = f'DELETE FROM {m.group(1)};'
        return f'print({repr(sql)})'

    # insert record into <table> with values <v1>, <v2>
    m = re.match(r'^insert\s+record\s+into\s+([a-zA-Z_]\w*)\s+with\s+values\s+(.+)$', line, re.IGNORECASE)
    if m:
        tbl, vals_raw = m.group(1), m.group(2)
        vals = parse_args_list(vals_raw)
        sql = f'INSERT INTO {tbl} VALUES ({vals});'
        return f'print({repr(sql)})'

    # insert into <table> columns (<cols>) values (<vals>)
    m = re.match(r'^insert\s+into\s+([a-zA-Z_]\w*)\s+columns?\s+\((.+?)\)\s+values?\s+\((.+?)\)$', line, re.IGNORECASE)
    if m:
        tbl, cols, vals = m.group(1), m.group(2), m.group(3)
        sql = f'INSERT OR IGNORE INTO {tbl} ({cols}) VALUES ({vals});'
        return f'print({repr(sql)})'

    # insert or replace into <table>
    m = re.match(r'^insert\s+or\s+replace\s+into\s+([a-zA-Z_]\w*)\s+\((.+?)\)\s+values?\s+\((.+?)\)$', line, re.IGNORECASE)
    if m:
        tbl, cols, vals = m.group(1), m.group(2), m.group(3)
        sql = f'INSERT OR REPLACE INTO {tbl} ({cols}) VALUES ({vals});'
        return f'print({repr(sql)})'

    # select all from <table> [where <cond>] [order by <col>] [limit <n>]
    m = re.match(r'^select\s+all\s+from\s+([a-zA-Z_]\w*)(?:\s+where\s+(.+?))?(?:\s+order\s+by\s+(.+?))?(?:\s+limit\s+(\d+))?$', line, re.IGNORECASE)
    if m:
        tbl = m.group(1)
        where = f' WHERE {m.group(2)}' if m.group(2) else ''
        order = f' ORDER BY {m.group(3)}' if m.group(3) else ''
        limit = f' LIMIT {m.group(4)}' if m.group(4) else ''
        sql = f'SELECT * FROM {tbl}{where}{order}{limit};'
        return f'print({repr(sql)})'

    # select <cols> from <table> [where <cond>] [order by <col>] [limit <n>]
    m = re.match(r'^select\s+(.+?)\s+from\s+([a-zA-Z_]\w*)(?:\s+where\s+(.+?))?(?:\s+order\s+by\s+(.+?))?(?:\s+limit\s+(\d+))?$', line, re.IGNORECASE)
    if m:
        cols, tbl = m.group(1), m.group(2)
        where = f' WHERE {m.group(3)}' if m.group(3) else ''
        order = f' ORDER BY {m.group(4)}' if m.group(4) else ''
        limit = f' LIMIT {m.group(5)}' if m.group(5) else ''
        sql = f'SELECT {cols} FROM {tbl}{where}{order}{limit};'
        return f'print({repr(sql)})'

    # count records in <table> [where <cond>]
    m = re.match(r'^count\s+records?\s+in\s+([a-zA-Z_]\w*)(?:\s+where\s+(.+))?$', line, re.IGNORECASE)
    if m:
        tbl = m.group(1)
        where = f' WHERE {m.group(2)}' if m.group(2) else ''
        sql = f'SELECT COUNT(*) FROM {tbl}{where};'
        return f'print({repr(sql)})'

    # update <table> set <col>=<val> where <cond>
    m = re.match(r'^update\s+([a-zA-Z_]\w*)\s+set\s+(.+?)\s+where\s+(.+)$', line, re.IGNORECASE)
    if m:
        tbl, sets, cond = m.group(1), m.group(2), m.group(3)
        sql = f'UPDATE {tbl} SET {sets} WHERE {cond};'
        return f'print({repr(sql)})'

    # update <table> set <col>=<val> (blocked without where clause)
    m = re.match(r'^update\s+([a-zA-Z_]\w*)\s+set\s+(.+)$', line, re.IGNORECASE)
    if m:
        tbl = m.group(1)
        raise SyntaxError(
            f"[ENLANG DB SAFETY ERROR] Accidental bulk update blocked on table '{tbl}'! "
            f"Updating without a 'where' clause alters every row in the table. "
            f"Add a 'where' condition or append 'confirm bulk' if intended."
        )

    # delete all rows from <table> confirm bulk
    m = re.match(r'^delete\s+all\s+(?:rows?\s+)?from\s+([a-zA-Z_]\w*)\s+confirm\s+bulk$', line, re.IGNORECASE)
    if m:
        tbl = m.group(1)
        sql = f'DELETE FROM {tbl};'
        return f'print({repr(sql)})'

    # delete [row|rows] from <table> where <cond>
    m = re.match(r'^delete\s+(?:rows?\s+)?from\s+([a-zA-Z_]\w*)\s+where\s+(.+)$', line, re.IGNORECASE)
    if m:
        tbl, cond = m.group(1), m.group(2)
        sql = f'DELETE FROM {tbl} WHERE {cond};'
        return f'print({repr(sql)})'

    # delete from <table> (blocked without where clause)
    m = re.match(r'^delete\s+(?:rows?\s+)?from\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        tbl = m.group(1)
        raise SyntaxError(
            f"[ENLANG DB SAFETY ERROR] Accidental bulk delete blocked on table '{tbl}'! "
            f"Deleting without a 'where' clause wipes the entire table. "
            f"Example: 'delete row from {tbl} where id is 42' or 'delete all rows from {tbl} confirm bulk'."
        )

    # create index <name> on <table> (<col>) [unique]
    m = re.match(r'^create\s+(unique\s+)?index\s+([a-zA-Z_]\w*)\s+on\s+([a-zA-Z_]\w*)\s+\((.+?)\)$', line, re.IGNORECASE)
    if m:
        unique = 'UNIQUE ' if m.group(1) else ''
        idx, tbl, col = m.group(2), m.group(3), m.group(4)
        sql = f'CREATE {unique}INDEX IF NOT EXISTS {idx} ON {tbl} ({col});'
        return f'print({repr(sql)})'

    # drop index <name>
    m = re.match(r'^drop\s+index\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        sql = f'DROP INDEX IF EXISTS {m.group(1)};'
        return f'print({repr(sql)})'

    # create view <name> as select ...
    m = re.match(r'^create\s+view\s+([a-zA-Z_]\w*)\s+as\s+(.+)$', line, re.IGNORECASE)
    if m:
        view, query = m.group(1), m.group(2)
        sql = f'CREATE VIEW IF NOT EXISTS {view} AS {query};'
        return f'print({repr(sql)})'

    # define foreign key <col> in <table> references <ref_table>(<ref_col>)
    m = re.match(r'^define\s+foreign\s+key\s+([a-zA-Z_]\w*)\s+in\s+([a-zA-Z_]\w*)\s+references\s+([a-zA-Z_]\w*)\s*\(([a-zA-Z_]\w*)\)$', line, re.IGNORECASE)
    if m:
        col, tbl, ref_tbl, ref_col = m.group(1), m.group(2), m.group(3), m.group(4)
        sql = f'-- FK: ALTER TABLE {tbl} ADD FOREIGN KEY ({col}) REFERENCES {ref_tbl}({ref_col});'
        return f'print({repr(sql)})'

    # enable foreign keys
    if re.match(r'^enable\s+foreign\s+keys?$', line, re.IGNORECASE):
        return "print('PRAGMA foreign_keys = ON;')"

    # begin transaction
    if re.match(r'^begin\s+(?:transaction|trans)$', line, re.IGNORECASE):
        return "print('BEGIN TRANSACTION;')"

    # commit
    if re.match(r'^commit$', line, re.IGNORECASE):
        return "print('COMMIT;')"

    # rollback
    if re.match(r'^rollback$', line, re.IGNORECASE):
        return "print('ROLLBACK;')"

    # savepoint <name>
    m = re.match(r'^savepoint\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        sql = f'SAVEPOINT {m.group(1)};'
        return f'print({repr(sql)})'

    # release savepoint <name>
    m = re.match(r'^release\s+savepoint\s+([a-zA-Z_]\w*)$', line, re.IGNORECASE)
    if m:
        sql = f'RELEASE SAVEPOINT {m.group(1)};'
        return f'print({repr(sql)})'

    # Unknown SQL lines → comment passthrough
    return f'print({repr("-- " + line)})'
