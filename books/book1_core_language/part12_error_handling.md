# Part 12: Error Handling & Exception Management

Robust applications must handle errors gracefully without unexpected crashes. EnLang provides natural English keywords for throwing, catching, and handling exceptions.

## 1. Raising Exceptions (`raise` / `throw`)

You can throw exceptions using natural syntax:

```enlg
define number age as -5

if age is less than 0 then:
    raise ValueError with message "Age cannot be negative"
```

Or using `throw error`:

```enlg
if connection_failed is true then:
    throw error "Database Connection Timeout"
```

### Transpiled Target Output:
```python
if age < 0:
    raise ValueError("Age cannot be negative")

if connection_failed == True:
    raise Exception("Database Connection Timeout")
```

## 2. Catching Exceptions (`try` / `except` / `finally`)

EnLang supports standard try-except exception blocks:

```enlg
try:
    read file "data.txt" into content
    display content
except FileNotFoundError:
    display "Warning: data.txt was not found!"
finally:
    display "Cleanup completed."
```

### Transpiled Target Output:
```python
try:
    with open("data.txt", 'r', encoding='utf-8') as _f: content = _f.read()
    print(content)
except FileNotFoundError:
    print("Warning: data.txt was not found!")
finally:
    print("Cleanup completed.")
```

## Zero Error Philosophy

EnLang emphasizes catching errors at static compile time using `enlang check main.enlg`. This prevents cryptic runtime 500 server crashes in production!
