# # EnLang Recursive Function Example
# # Recursively prints numbers from n to 10

def print_numbers(n):
    if n > 10:
        return
    print(n)
    print_numbers(n + 1)

# # Start recursion from 1
print_numbers(1)