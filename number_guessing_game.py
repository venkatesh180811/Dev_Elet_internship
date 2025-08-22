import random
import sys

def get_difficulty_level():
    """Get the difficulty level from the user."""
    print("\n Welcome to the Number Guessing Game! ")
    print("=" * 40)
    print("\nChoose your difficulty level:")
    print("1. Easy (1-50)")
    print("2. Medium (1-100)")
    print("3. Hard (1-500)")
    print("4. Expert (1-1000)")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-4): "))
            if choice == 1:
                return 1, 50, "Easy"
            elif choice == 2:
                return 1, 100, "Medium"
            elif choice == 3:
                return 1, 500, "Hard"
            elif choice == 4:
                return 1, 1000, "Expert"
            else:
                print("❌ Please enter a number between 1 and 4!")
        except ValueError:
            print("❌ Please enter a valid number!")

def get_user_guess(min_num, max_num):
    """Get a valid guess from the user."""
    while True:
        try:
            guess = int(input(f"\nEnter your guess ({min_num}-{max_num}): "))
            if min_num <= guess <= max_num:
                return guess
            else:
                print(f"❌ Please enter a number between {min_num} and {max_num}!")
        except ValueError:
            print("❌ Please enter a valid number!")

def calculate_max_attempts(min_num, max_num):
    """Calculate optimal number of attempts based on range."""
    import math
    return math.ceil(math.log2(max_num - min_num + 1)) + 3

def play_game():
    """Main game logic."""
    # Get difficulty settings
    min_num, max_num, difficulty = get_difficulty_level()
    
    # Generate random number
    secret_number = random.randint(min_num, max_num)
    max_attempts = calculate_max_attempts(min_num, max_num)
    
    print(f"\n🎮 {difficulty} Mode Selected!")
    print(f"I'm thinking of a number between {min_num} and {max_num}")
    print(f"You have {max_attempts} attempts to guess it!")
    print("-" * 40)
    
    attempts = 0
    guessed_numbers = []
    
    while attempts < max_attempts:
        attempts += 1
        remaining = max_attempts - attempts + 1
        
        print(f"\n Attempt {attempts}/{max_attempts} (Remaining: {remaining})")
        
        if guessed_numbers:
            print(f"Previous guesses: {', '.join(map(str, sorted(guessed_numbers)))}")
        
        guess = get_user_guess(min_num, max_num)
        
        # Check if already guessed
        if guess in guessed_numbers:
            print(" You already guessed that number! Try again.")
            attempts -= 1  # Don't count repeated guesses
            continue
            
        guessed_numbers.append(guess)
        
        if guess == secret_number:
            print(f"\n CONGRATULATIONS! ")
            print(f"You guessed the number {secret_number} in {attempts} attempts!")
            
            # Performance feedback
            if attempts <= max_attempts // 3:
                print(" Excellent! You're a guessing master!")
            elif attempts <= max_attempts // 2:
                print(" Great job! Very impressive!")
            elif attempts <= max_attempts * 2 // 3:
                print(" Good work! Well done!")
            else:
                print(" You made it! That was close!")
            
            return True
        
        elif guess < secret_number:
            difference = secret_number - guess
            if difference > (max_num - min_num) // 4:
                print(" Too low! Try going much higher!")
            else:
                print(" Too low! Try a bit higher!")
        
        else:  # guess > secret_number
            difference = guess - secret_number
            if difference > (max_num - min_num) // 4:
                print(" Too high! Try going much lower!")
            else:
                print(" Too high! Try a bit lower!")
        
        # Provide additional hints as attempts increase
        if attempts == max_attempts - 2:
            print("  Warning: Only 2 attempts left!")
        elif attempts == max_attempts - 1:
            print(" Last chance! Make it count!")
    
    # Game over
    print(f"\n Game Over! ")
    print(f"The number was {secret_number}")
    print(f"Your guesses: {', '.join(map(str, sorted(guessed_numbers)))}")
    print("Better luck next time!")
    return False

def show_stats(games_played, games_won):
    """Display player statistics."""
    if games_played > 0:
        win_rate = (games_won / games_played) * 100
        print(f"\n Your Statistics:")
        print(f"Games played: {games_played}")
        print(f"Games won: {games_won}")
        print(f"Win rate: {win_rate:.1f}%")

def main():
    """Main program loop."""
    games_played = 0
    games_won = 0
    
    try:
        while True:
            # Play a game
            won = play_game()
            games_played += 1
            if won:
                games_won += 1
            
            # Show statistics
            show_stats(games_played, games_won)
            
            # Ask to play again
            while True:
                play_again = input("\n Would you like to play again? (y/n): ").lower().strip()
                if play_again in ['y', 'yes']:
                    print("\n" + "=" * 50)
                    break
                elif play_again in ['n', 'no']:
                    print("\n Thanks for playing! Goodbye!")
                    return
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no.")
    
    except KeyboardInterrupt:
        print("\n\n Thanks for playing! Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()