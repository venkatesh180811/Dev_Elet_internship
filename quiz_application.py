#!/usr/bin/env python3

import random
import time

class QuizGame:
    def __init__(self):
        self.score = 0
        self.total_questions = 0
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["A) London", "B) Berlin", "C) Paris", "D) Madrid"],
                "correct": "C",
                "explanation": "Paris is the capital and largest city of France."
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"],
                "correct": "B",
                "explanation": "Mars appears red due to iron oxide (rust) on its surface."
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["A) African Elephant", "B) Blue Whale", "C) Giraffe", "D) Polar Bear"],
                "correct": "B",
                "explanation": "The Blue Whale can grow up to 100 feet long and weigh up to 200 tons."
            },
            {
                "question": "In which year did World War II end?",
                "options": ["A) 1944", "B) 1945", "C) 1946", "D) 1947"],
                "correct": "B",
                "explanation": "World War II ended in 1945 with the surrender of Japan in August."
            },
            {
                "question": "What is the chemical symbol for gold?",
                "options": ["A) Go", "B) Gd", "C) Au", "D) Ag"],
                "correct": "C",
                "explanation": "Au comes from the Latin word 'aurum' meaning gold."
            },
            {
                "question": "Which programming language is known for its use in data science?",
                "options": ["A) Java", "B) Python", "C) C++", "D) JavaScript"],
                "correct": "B",
                "explanation": "Python is widely used in data science due to libraries like pandas, numpy, and scikit-learn."
            },
            {
                "question": "What is the smallest country in the world?",
                "options": ["A) Monaco", "B) Nauru", "C) Vatican City", "D) San Marino"],
                "correct": "C",
                "explanation": "Vatican City is the smallest country with an area of just 0.17 square miles."
            },
            {
                "question": "Who painted the Mona Lisa?",
                "options": ["A) Vincent van Gogh", "B) Pablo Picasso", "C) Leonardo da Vinci", "D) Michelangelo"],
                "correct": "C",
                "explanation": "Leonardo da Vinci painted the Mona Lisa between 1503 and 1519."
            },
            {
                "question": "What is the speed of light in vacuum?",
                "options": ["A) 300,000 km/s", "B) 299,792,458 m/s", "C) 186,000 miles/s", "D) All of the above"],
                "correct": "D",
                "explanation": "All options represent the speed of light in different units."
            },
            {
                "question": "Which ocean is the largest?",
                "options": ["A) Atlantic Ocean", "B) Indian Ocean", "C) Pacific Ocean", "D) Arctic Ocean"],
                "correct": "C",
                "explanation": "The Pacific Ocean covers about 46% of the Earth's water surface."
            }
        ]
    
    def display_welcome(self):
        print("=" * 60)
        print("WELCOME TO THE ULTIMATE QUIZ GAME!")
        print("=" * 60)
        print("\nINSTRUCTIONS:")
        print("• Answer each multiple-choice question by typing A, B, C, or D")
        print("• You'll get immediate feedback after each answer")
        print("• Your final score will be displayed at the end")
        print("• Type 'quit' at any time to exit the game")
        print("\n" + "=" * 60)
        
        input("\nPress ENTER to start the quiz...")
        print()
    
    def display_question(self, question_data, question_num):
        print(f"Question {question_num}/{len(self.questions)}")
        print("-" * 40)
        print(f"{question_data['question']}")
        print()
        
        for option in question_data['options']:
            print(f"   {option}")
        print()
    
    def get_user_answer(self):
        while True:
            answer = input("Your answer (A/B/C/D or 'quit'): ").strip().upper()
            
            if answer == 'QUIT':
                return 'QUIT'
            elif answer in ['A', 'B', 'C', 'D']:
                return answer
            else:
                print("❌ Invalid input! Please enter A, B, C, D, or 'quit'")
    
    def check_answer(self, user_answer, correct_answer, explanation):
        if user_answer == correct_answer:
            print("✅ CORRECT! Great job!")
            self.score += 1
        else:
            print(f"❌ INCORRECT! The correct answer was {correct_answer}")
        
        print(f"Explanation: {explanation}")
        print()
        return user_answer == correct_answer
    
    def display_progress(self):
        print(f"Current Score: {self.score}/{self.total_questions}")
        print("-" * 40)
        print()
    
    def run_quiz(self):
        quiz_questions = self.questions.copy()
        random.shuffle(quiz_questions)
        
        for i, question_data in enumerate(quiz_questions, 1):
            self.total_questions += 1
            
            self.display_question(question_data, i)
            
            user_answer = self.get_user_answer()
            
            if user_answer == 'QUIT':
                print("\nThanks for playing! Goodbye!")
                return
            
            self.check_answer(user_answer, question_data['correct'], question_data['explanation'])
            
            self.display_progress()
            
            if i < len(quiz_questions):
                time.sleep(1)
    
    def display_final_results(self):
        print("=" * 60)
        print("QUIZ COMPLETED!")
        print("=" * 60)
        
        percentage = (self.score / self.total_questions) * 100
        
        print(f"\nFINAL RESULTS:")
        print(f"   Correct Answers: {self.score}")
        print(f"   Total Questions: {self.total_questions}")
        print(f"   Score: {percentage:.1f}%")
        print()
        
        if percentage >= 90:
            print("OUTSTANDING! You're a quiz master!")
        elif percentage >= 80:
            print("EXCELLENT! Great knowledge!")
        elif percentage >= 70:
            print("GOOD JOB! Well done!")
        elif percentage >= 60:
            print("NOT BAD! Keep learning!")
        else:
            print("KEEP PRACTICING! You'll improve!")
        
        print("\n" + "=" * 60)
    
    def play_again(self):
        while True:
            again = input("\nWould you like to play again? (yes/no): ").strip().lower()
            if again in ['yes', 'y']:
                return True
            elif again in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'")

def main():
    print("Starting Quiz Game...")
    time.sleep(1)
    
    while True:
        game = QuizGame()
        
        game.display_welcome()
        
        game.run_quiz()
        
        if game.total_questions > 0:
            game.display_final_results()
        
        if not game.play_again():
            print("\nThank you for playing the Ultimate Quiz Game!")
            print("See you next time!")
            break
        
        print("\nStarting a new game...\n")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please try running the game again.")