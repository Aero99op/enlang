# Part 17: Database Integration (`.enlg` & `.enlgdb`)

EnLang provides built-in database support directly from `.enlg` scripts, as well as standalone `.enlgdb` schema files.

## 1. Connecting to SQLite Database (`connect to database`)

```enlg
connect to database "app.db" as db
```

### Transpiled Target Output:
```python
import sqlite3
db = sqlite3.connect("app.db")
```

## 2. Defining Tables (`define table`)

Define database tables using natural English column declarations:

```enlg
define table users with columns id as INTEGER PRIMARY KEY AUTOINCREMENT, username as TEXT NOT NULL, email as TEXT NOT NULL
```

### Transpiled Target Output:
```python
_cur = db.cursor()
_cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL)')
db.commit()
```

## 3. Inserting Records (`insert record`)

```enlg
insert record into users with values NULL, 'Spandan', 'spandan@enlang.org'
```

### Transpiled Target Output:
```python
_cur = db.cursor()
_cur.execute(f'INSERT INTO users VALUES (NULL, \'Spandan\', \'spandan@enlang.org\')')
db.commit()
```

## 4. Executing Custom SQL Queries (`execute query`)

Execute queries and store results directly into EnLang variables:

```enlg
execute query "SELECT * FROM users" on database db and store in all_users

display all_users
```

### Transpiled Target Output:
```python
_cur = db.cursor()
_cur.execute("SELECT * FROM users")
all_users = _cur.fetchall()
db.commit()
print(all_users)
```
