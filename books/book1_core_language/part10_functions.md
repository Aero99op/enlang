# Part 10: Functions & Async Operations

Functions encapsulate reusable logic in EnLang.

## 1. Defining & Calling Functions

Functions are defined using the `function` keyword:

```enlg
function calculate_total(price, tax_rate):
    define decimal tax as price times tax_rate
    return price plus tax

define decimal final_price as calculate_total(100.0, 0.18)
display "Final Price: " + final_price
```

### Transpiled Target Output:
```python
def calculate_total(price, tax_rate):
    tax = price * tax_rate
    return price + tax

final_price = calculate_total(100.0, 0.18)
print("Final Price: " + str(final_price))
```

## 2. Asynchronous Functions (`async`)

EnLang natively supports asynchronous functions for non-blocking operations:

```enlg
async function fetch_user_data(user_id):
    display "Fetching data asynchronously for user: " + user_id
    fetch url "https://api.example.com/users/" + user_id and store in response
    return response
```

### Transpiled Target Output:
```python
async def fetch_user_data(user_id):
    print("Fetching data asynchronously for user: " + str(user_id))
    import urllib.request
    response = urllib.request.urlopen("https://api.example.com/users/" + str(user_id)).read().decode('utf-8')
    return response
```

## 3. Built-in Utility Functions

EnLang features built-in natural functions for math, strings, and system delays:

```enlg
sleep 2 seconds           # Pauses execution for 2 seconds
sleep 500 ms              # Pauses execution for 500 milliseconds

get current date and time and store in current_now
display "Current time: " + current_now
```
