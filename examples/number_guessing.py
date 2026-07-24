# # Number Guessing Game in EnLang (.enlg)

import random

print("=== Welcome to EnLang Number Guessing Game! ===")
print("I have chosen a secret number between 1 and 50.")

secret_number = random.randint(1, 50)
attempts = 0
guessed = False

while guessed == False:
    user_input = input("Enter your guess (1-50): ")
    guess = int(user_input)
    attempts += 1

    if guess == secret_number:
        print(str("🎉 Congratulations! You guessed the secret number: ") + str(secret_number))
        print(str("Total attempts taken: ") + str(attempts))
        guessed = True
    elif guess > secret_number:
        print("📉 Too high! Try a smaller number.")
    else:
        print("📈 Too low! Try a larger number.")

print("Game Over! Thanks for playing EnLang Number Guessing Game.")