# Part 8: Operators & Expression Cleaners

In EnLang, expressions use natural English operators instead of standard programming symbols.

## Comparison Operators

| EnLang Natural Operator | Native Python Equivalent | Example |
| :--- | :--- | :--- |
| `is equal to` | `==` | `if score is equal to 100 then:` |
| `is not equal to` | `!=` | `if status is not equal to "active" then:` |
| `is greater than` | `>` | `if age is greater than 18 then:` |
| `is less than` | `<` | `if price is less than 50 then:` |
| `is greater than or equal to` | `>=` | `if score is greater than or equal to 80 then:` |
| `is less than or equal to` | `<=` | `if count is less than or equal to 5 then:` |
| `is in` | `in` | `if "admin" is in roles then:` |
| `is not in` | `not in` | `if item is not in cart then:` |

## Arithmetic Operators

| EnLang Natural Operator | Native Python Equivalent | Example |
| :--- | :--- | :--- |
| `plus` | `+` | `set total to price plus tax` |
| `minus` | `-` | `set balance to total minus discount` |
| `times` | `*` | `set area to width times height` |
| `divided by` | `/` | `set average to sum divided by count` |
| `modulo` | `%` | `set remainder to number modulo 2` |
| `power of` | `**` | `set result to 2 power of 8` |

## Logical Operators

| EnLang Natural Operator | Native Python Equivalent | Example |
| :--- | :--- | :--- |
| `and` | `and` | `if age > 18 and is_active is true then:` |
| `or` | `or` | `if role == "admin" or role == "editor" then:` |
| `not` | `not` | `if not is_disabled then:` |

## Natural Expression Examples

```enlg
define number a as 10
define number b as 20

if a plus b is equal to 30 then:
    display "Math is correct!"
```

Transpiles directly to:
```python
a = 10
b = 20
if a + b == 30:
    print("Math is correct!")
```
