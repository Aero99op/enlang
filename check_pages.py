import re
with open("enlangbookv2release.pdf", "rb") as f:
    data = f.read()
pages = len(re.findall(b"/Type /Page[^s]", data))
print(f"Approximate page count: {pages}")
print(f"File size: {len(data):,} bytes ({len(data)//1024} KB)")
