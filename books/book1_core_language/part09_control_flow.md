# Part 9: Control Flow, Conditional Logic & Pattern Matching

Control flow structures dictate the order in which statements are executed in an EnLang program.

## 1. Conditional Logic (`if` / `else`)

EnLang uses natural `if ... then:` statements.

### Syntax:
```enlg
if <condition> then:
    <statements>
otherwise if <condition> then:
    <statements>
otherwise:
    <statements>
```

### Real Example:
```enlg
define number user_age as 20

if user_age is greater than 18 then:
    display "Access Granted: Adult"
otherwise if user_age is equal to 18 then:
    display "Access Granted: Newly Adult"
otherwise:
    display "Access Denied: Minor"
```

### Native Python Target Output:
```python
user_age = 20
if user_age > 18:
    print("Access Granted: Adult")
elif user_age == 18:
    print("Access Granted: Newly Adult")
else:
    print("Access Denied: Minor")
```

## 2. Pattern Matching (`match` / `case`)

EnLang features a powerful pattern matching syntax (`match`, `case`, `default`, `end match`):

```enlg
define text status_code as "200"

match status_code:
case "200":
    display "Success OK"
case "404":
    display "Error: Resource Not Found"
case "500":
    display "Error: Internal Server Error"
default:
    display "Unknown Status Code"
end match
```

### Match with Multiple Values & Expressions:
```enlg
define number score as 85

match score:
case is greater than or equal to 90:
    display "Grade A"
case is greater than or equal to 80:
    display "Grade B"
default:
    display "Grade C"
end match
```

## 3. Increment & Decrement Shortcuts

EnLang provides natural English syntax for updating numerical variables:

```enlg
define number score as 10
increment score by 5      # Transpiles to: score += 5
decrement score by 2      # Transpiles to: score -= 2
```
