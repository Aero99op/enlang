import urllib.request

try:
    resp = urllib.request.urlopen("http://localhost:8099/").read().decode("utf-8")
    print("HTTP 200 OK — RENDERED HTML LENGTH:", len(resp))
    print("TOP 300 CHARS OF RENDERED HTML:")
    print(resp[:300])
except Exception as e:
    print("FETCH ERROR:", e)
