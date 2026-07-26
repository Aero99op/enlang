# Part 14: File I/O & Storage Operations

EnLang provides natural English syntax for reading from and writing to disk files.

## 1. Reading Files (`read file`)

To read the full contents of a file into a variable:

```enlg
read file "config.json" into config_data
display "Config loaded: " + config_data
```

### Transpiled Target Output:
```python
with open("config.json", 'r', encoding='utf-8') as _f:
    config_data = _f.read()
print("Config loaded: " + str(config_data))
```

## 2. Writing to Files (`write ... to file`)

To write text or variable data to a file:

```enlg
define text log_entry as "User logged in at 10:00 AM"
write log_entry to file "app.log"
```

### Transpiled Target Output:
```python
log_entry = "User logged in at 10:00 AM"
with open("app.log", 'w', encoding='utf-8') as _f:
    _f.write(str(log_entry))
```
