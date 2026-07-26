# Part 11: Object-Oriented Programming (OOP) & Interfaces

EnLang supports full Object-Oriented Programming, including Classes, Inheritance, and Interfaces.

## 1. Creating Interfaces (`interface`)

Interfaces define blueprints for classes:

```enlg
create interface Authenticatable:
    function login(username, password):
    function logout():
end interface
```

### Transpiled Target Output:
```python
class Authenticatable:
    pass
# end class/interface
```

## 2. Classes & Inheritance (`create class` / `extends` / `implements`)

Classes are created using `create class` with optional `extends` (for inheritance) and `implements`:

```enlg
create class BaseUser:
    function get_role():
        return "Standard User"

create class User extends BaseUser:
    function __init__(self, username, email):
        set self.username to username
        set self.email to email

    function get_info(self):
        return self.username + " (" + self.email + ")"
```

### Transpiled Target Output:
```python
class BaseUser:
    def get_role(self):
        return "Standard User"

class User(BaseUser):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_info(self):
        return self.username + " (" + str(self.email) + ")"
```

## 3. Instantiating Objects

Objects are instantiated naturally:

```enlg
define user1 as User("Spandan", "spandan@enlang.org")
display user1.get_info()
```
