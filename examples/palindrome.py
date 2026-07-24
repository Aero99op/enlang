# # Simple Palindrome Checker in EnLang (.enlg)

print("=== Simple Palindrome Checker ===")

word = "racecar"
print(str("Original Word: ") + str(word))

reversed_word = word[::-1]
print(str("Reversed Word: ") + str(reversed_word))

if word == reversed_word:
    print(str("Result: '") + str(word) + str("' IS a Palindrome!"))
else:
    print(str("Result: '") + str(word) + str("' IS not a Palindrome."))