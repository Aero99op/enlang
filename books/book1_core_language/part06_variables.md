# Part 6: Variables & Value Assignment

Variables in EnLang allow you to store and manipulate data using plain English syntax.

## Variable Declaration Syntax

You can declare typed variables using `define`, `let`, or `var`:

### Format:
```enlg
define <type> <name> as <value>
# OR
set <name> to <value>
# OR
store <value> in <name>
```

### Examples:
```enlg
define text user_name as "Spandan"
define number user_age as 25
define decimal account_balance as 1500.50
define boolean is_verified as true
```

## Default Initializations

If you declare a typed variable without specifying an initial value, EnLang automatically initializes it to a safe default:

```enlg
define number score        # Defaults to 0
define decimal rate        # Defaults to 0.0
define text title          # Defaults to ""
define boolean active      # Defaults to false
define list items          # Defaults to []
define dictionary config   # Defaults to {}
```

## Reassigning Values

You can update the value of an existing variable using natural English phrasing:

```enlg
set score to 100
store "Spandan Prayas Patra" in user_name
set is_verified to false
```

## Transpilation Mapping

| EnLang Natural Syntax | Transpiled Native Python Target |
| :--- | :--- |
| `define text name as "Spandan"` | `name = "Spandan"` |
| `define number count as 10` | `count = 10` |
| `set count to 20` | `count = 20` |
| `store 50 in count` | `count = 50` |
| `define list users` | `users = []` |
| `define dictionary settings` | `settings = {}` |
