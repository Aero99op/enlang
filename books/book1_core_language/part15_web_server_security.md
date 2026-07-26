# Part 15: Web Server, Cryptography & HTTP Networking

EnLang includes built-in commands for starting web servers, making HTTP network requests, and performing cryptographic hashing.

## 1. Zero-Config HTTP Web Server

You can start a lightweight web server directly from `.enlg` code:

```enlg
start web server on port 8000
```

### Transpiled Target Output:
```python
from enlang_core.web_server import start_enlang_server
start_enlang_server(8000)
```

## 2. HTTP Networking (`fetch url`)

Fetch external data over HTTP/HTTPS:

```enlg
fetch url "https://api.github.com/users/spandan" and store in response
display response
```

### Transpiled Target Output:
```python
import urllib.request
response = urllib.request.urlopen("https://api.github.com/users/spandan").read().decode('utf-8')
print(response)
```

## 3. Cryptographic Hashing (`hash`)

Perform secure cryptographic hashing (SHA256, MD5, SHA512) natively:

```enlg
define text secret as "MyPassword123"
hash secret with sha256 and store in hashed_password

display "Hashed Password: " + hashed_password
```

### Transpiled Target Output:
```python
secret = "MyPassword123"
import hashlib
hashed_password = hashlib.sha256(secret.encode('utf-8')).hexdigest()
print("Hashed Password: " + str(hashed_password))
```
