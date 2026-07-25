"""
EnLang Universal Web Server
============================
Serves any EnLang application over HTTP.
PERMANENTLY COMPLETE — handles static assets, MIME types, error pages.

File routing:
  *.enlgf  ->  HTML  (body content)
  *.enlgd  ->  CSS   (style block)
  *.enlgs  ->  JS    (script block)
  Static assets (images, fonts, etc.) are served directly.
"""

import sys
import http.server
import socketserver
import os
import glob
import re
import mimetypes

# Ensure all common MIME types are registered
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('font/woff', '.woff')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('font/ttf', '.ttf')
mimetypes.add_type('font/otf', '.otf')


def _run_enlg_file(file_path: str) -> str:
    """Runs any EnLang file through the interpreter, returns captured stdout."""
    try:
        from .interpreter import EnLangInterpreter
        interp = EnLangInterpreter()
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        _, stdout, _, _ = interp.run_code(code, file_path=file_path)
        return stdout.strip()
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        return f"<!-- EnLang render error in {os.path.basename(file_path)}: {e}\n{tb} -->"


def _build_error_page(title: str, message: str, code: int = 500) -> str:
    """Returns a clean HTML error page."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EnLang {code} — {title}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #0f172a; color: #f8fafc; font-family: 'Courier New', monospace;
            display: flex; align-items: center; justify-content: center;
            min-height: 100vh; flex-direction: column; gap: 1rem; padding: 2rem; }}
    h1 {{ font-size: 4rem; color: #ef4444; }}
    h2 {{ font-size: 1.5rem; color: #94a3b8; }}
    pre {{ background: #1e293b; padding: 1.5rem; border-radius: 12px; font-size: 0.85rem;
           color: #fb923c; max-width: 90vw; overflow-x: auto; white-space: pre-wrap; }}
    .badge {{ background: #ef4444; color: white; padding: 0.3rem 0.8rem;
              border-radius: 9999px; font-size: 0.8rem; font-weight: bold; }}
  </style>
</head>
<body>
  <span class="badge">EnLang Error</span>
  <h1>{code}</h1>
  <h2>{title}</h2>
  <pre>{message}</pre>
</body>
</html>"""


def start_enlang_server(port=8000, directory="."):
    port = int(port)
    if directory and os.path.exists(directory):
        os.chdir(directory)

    class EnLangHTTPHandler(http.server.SimpleHTTPRequestHandler):

        def log_message(self, format, *args):
            # Only log errors, suppress routine access logs
            if args and str(args[1]) not in ('200', '304'):
                super().log_message(format, *args)

        def do_GET(self):
            try:
                # Serve root → assembled EnLang page
                if self.path in ('/', '/index.html'):
                    html_page = self._build_page()
                    encoded = html_page.encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(encoded)))
                    self.send_header('Cache-Control', 'no-cache')
                    self.end_headers()
                    self.wfile.write(encoded)

                # Serve static files from cwd
                elif self._is_static_file(self.path):
                    self._serve_static(self.path)

                # 404 for unknown routes
                else:
                    err = _build_error_page('Not Found', f'Route not found: {self.path}', 404)
                    encoded = err.encode('utf-8')
                    self.send_response(404)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(encoded)))
                    self.end_headers()
                    self.wfile.write(encoded)

            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                err = _build_error_page('Server Error', f'{type(e).__name__}: {e}\n\n{tb}', 500)
                encoded = err.encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

        def _is_static_file(self, path: str) -> bool:
            """Check if the request is for a static asset that exists on disk."""
            clean_path = path.split('?')[0].lstrip('/')
            full_path = os.path.join(os.getcwd(), clean_path)
            return os.path.isfile(full_path)

        def _serve_static(self, path: str):
            """Serve a static file with proper MIME type."""
            clean_path = path.split('?')[0].lstrip('/')
            full_path = os.path.join(os.getcwd(), clean_path)
            mime_type, _ = mimetypes.guess_type(full_path)
            if not mime_type:
                mime_type = 'application/octet-stream'
            try:
                with open(full_path, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', mime_type)
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.end_headers()
                self.wfile.write(data)
            except PermissionError:
                err = _build_error_page('Forbidden', f'Access denied: {path}', 403)
                encoded = err.encode('utf-8')
                self.send_response(403)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

        def _build_page(self) -> str:
            cwd = os.getcwd()
            html_body = ""
            css_output = ""
            js_output = ""
            page_title = "EnLang Application"
            page_meta = []

            # 1. CSS from *.enlgd files (sorted alphabetically for determinism)
            for f in sorted(glob.glob(os.path.join(cwd, "*.enlgd"))):
                result = _run_enlg_file(f)
                css_output += result + "\n"

            # 2. HTML from *.enlgf files
            for f in sorted(glob.glob(os.path.join(cwd, "*.enlgf"))):
                out = _run_enlg_file(f)
                for line in out.splitlines():
                    stripped = line.strip()
                    if not stripped or stripped.startswith('#'):
                        continue
                    # Extract <title>
                    if stripped.startswith('<title>') and stripped.endswith('</title>'):
                        m = re.search(r'<title>(.*?)</title>', stripped, re.IGNORECASE)
                        if m:
                            page_title = m.group(1)
                        continue
                    # Extract <meta> tags for <head>
                    if stripped.startswith('<meta ') or stripped == '<meta>':
                        page_meta.append(stripped)
                        continue
                    # Extract <link rel="stylesheet"> for <head>
                    if stripped.startswith('<link '):
                        page_meta.append(stripped)
                        continue
                    html_body += line + "\n"

            # 3. JS from *.enlgs files
            for f in sorted(glob.glob(os.path.join(cwd, "*.enlgs"))):
                result = _run_enlg_file(f)
                js_output += result + "\n"

            if not html_body.strip():
                html_body = (
                    '<div style="font-family:sans-serif;text-align:center;padding:50px">'
                    '<h1>EnLang App Running</h1>'
                    '<p>Create a <code>.enlgf</code> file to add HTML content.</p>'
                    '</div>'
                )

            # Inject additional meta/link tags
            extra_head = "\n    ".join(page_meta)
            if extra_head:
                extra_head = f"\n    {extra_head}"

            # Pure assembly — ZERO injected styles
            return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">{extra_head}
    <title>{page_title}</title>
    <style>
{css_output}
    </style>
</head>
<body>
{html_body}
<script>
{js_output}
</script>
</body>
</html>"""

    print(f"[OK] EnLang Web Server running -> http://localhost:{port}/")
    print(f"[OK] Serving from: {os.getcwd()}")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), EnLangHTTPHandler) as httpd:
        httpd.serve_forever()
