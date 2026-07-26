# Part 13: Modules, Packages & File Linking

Organizing code into modular files and importing third-party libraries is essential for large-scale applications.

## 1. Importing Modules (`import module`)

To import external or standard library modules in EnLang:

```enlg
import module math as m
import module datetime

define number root as m.sqrt(16)
display "Square root of 16 is: " + root
```

### Transpiled Target Output:
```python
import math as m
import datetime

root = m.sqrt(16)
print("Square root of 16 is: " + str(root))
```

## 2. Selective Imports (`from ... import`)

You can import specific functions or classes from a module:

```enlg
from math import sqrt, floor

define number result as floor(sqrt(20))
display "Floor of sqrt(20): " + result
```

## 3. Linking & Including Other EnLang Files (`include`)

EnLang allows linking other `.enlg`, `.enlgf`, `.enlgd`, `.enlgs`, or `.enlgdb` files dynamically:

```enlg
include "helper.enlg"
include "style.enlgd"
```

When transpiled, EnLang reads and executes the referenced target file within the current scope seamlessly.
