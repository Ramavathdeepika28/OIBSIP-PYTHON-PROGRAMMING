import random
import string

def generate_password(length, use_letters, use_numbers, use_symbols):
    # Let's gather all the characters you want in your password
    characters = ''
    if use_letters:
        characters += string.ascii_letters  # All uppercase and lowercase letters
    if use_numbers:
        characters += string.digits         # Numbers 0-9
    if use_symbols:
        characters += string.punctuation    # Special characters like !, @, #

    if not characters:
        print("Oops! You need to pick at least one type of character to create a password.")
        return ''

    # Now, let's build your password by randomly picking characters
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def ask_yes_no(question):
    # Simple helper to ask yes/no questions and return True/False
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer in ('y', 'yes'):
            return True
        elif answer in ('n', 'no'):
            return False
        else:
            print("Please answer with 'y' or 'n'.")

def ask_positive_integer(question):
    # Helper function to get a positive integer from the user
    while True:
        response = input(question + ": ").strip()
        if response.isdigit() and int(response) > 0:
            return int(response)
        else:
            print("Please enter a valid positive number.")

def main():
    print("Hey there! Welcome to your friendly Password Generator.")
    print("I'll help you create a strong, random password in just a few steps.\n")

    length = ask_positive_integer("First, how long would you like your password to be")

    print("\nGreat! Now let's decide what kind of characters to include.")
    use_letters = ask_yes_no("Would you like to include letters?")
    use_numbers = ask_yes_no("How about numbers?")
    use_symbols = ask_yes_no("And special symbols like !, @, #, etc.?")

    # Make sure user selects at least one type
    if not (use_letters or use_numbers or use_symbols):
        print("\nHmm... you didn't choose any character types. Let's try again!")
        return  # Exit the program or you can loop back if you want

    password = generate_password(length, use_letters, use_numbers, use_symbols)

    if password:
        print("\nAwesome! Here's your shiny new password:\n")
        print(password)
        print("\nRemember to keep it safe!")

if __name__ == "__main__":
    main()
