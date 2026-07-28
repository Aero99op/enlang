# EnLang v2.0.0 Language Reference
==============================================================================

## 1. Introduction
EnLang is a universal natural English programming language designed to bridge human intent and native code execution across five domains: core backend logic (`.enlg`), frontend UI (`.enlgf`), styling (`.enlgd`), client scripting (`.enlgs`), and relational databases (`.enlgdb`).

## 2. Variables & Assignment
Variables are declared implicitly upon assignment:
```enlg
set x to 10
let name to "EnLang"
store { "key": "val" } in my_map
```

## 3. Data Types
- **Primitives**: `Number` (integers and floats), `String`, `Boolean` (`true`/`false`), `Null` (`null`/`none`).
- **Compounds**: `List` (indexed sequence), `Map` (associative dictionary).

## 4. Control Flow & Loops
```enlg
if x is greater than 10 then:
    display "High"
else:
    display "Low"

for each item in my_list:
    display item

repeat 5 times:
    display "Hello"
```

## 5. Functions & Scoping
Functions are first-class constructs:
```enlg
function add with a and b:
    return a + b

set result to call add with 5 and 10
```
Variables declared inside a function belong to the local scope. Outer scope symbols are accessible unless shadowed.
