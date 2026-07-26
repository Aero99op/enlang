# Part 7: Primitive & Collection Data Types

EnLang supports a rich set of built-in primitive and collection data types.

## 1. Text (`text`)
Represents string literals.

```enlg
define text title as "EnLang Documentation"
define text message as 'Natural English Syntax'
```

## 2. Numbers (`number` & `decimal`)
- **`number`**: Whole integers.
- **`decimal`**: Floating-point numbers.

```enlg
define number total_items as 42
define decimal temperature as 98.6
```

## 3. Booleans (`boolean`)
Represents `true` or `false` truth values.

```enlg
define boolean is_logged_in as true
define boolean has_permission as false
```

## 4. Lists (`list` / `array`)
Ordered collections of items.

```enlg
define list fruits as ["Apple", "Banana", "Cherry"]
define list numbers as [10, 20, 30, 40]
```

## 5. Dictionaries (`dictionary` / `dict` / `map`)
Key-value mappings.

```enlg
define dictionary user as {"name": "Spandan", "role": "Author"}
```

## 6. Sets (`set`)
Unordered collections of unique elements.

```enlg
define set unique_ids
```

## Summary Table

| Data Type | Keyword | Natural Declaration Example | Default Value |
| :--- | :--- | :--- | :--- |
| String | `text` | `define text city as "Delhi"` | `""` |
| Integer | `number` | `define number age as 25` | `0` |
| Float | `decimal` | `define decimal price as 99.99` | `0.0` |
| Boolean | `boolean` | `define boolean is_admin as true` | `False` |
| List | `list` / `array` | `define list tags as ["ai", "web"]` | `[]` |
| Dictionary | `dictionary` / `map` | `define dictionary config` | `{}` |
| Set | `set` | `define set items` | `set()` |
