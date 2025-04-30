from groq_tester import PythonDeveloperAgent
import os

def main():
    # Initialize the agent with your Groq API key
    # You should store this in an environment variable
    api_key = os.getenv('GROQ_API_KEY')
    developer = PythonDeveloperAgent(api_key=api_key)

    # Example problems to solve
    problems = [
        "Create a function that sorts a list of dictionaries by a specific key",
        "Create a class to manage a simple todo list with add, remove, and list tasks functionality",
        "Create a function that checks if a string is a valid palindrome ignoring spaces and punctuation"
    ]

    # Create solutions for each problem
    for problem in problems:
        print(f"\nGenerating solution for problem: {problem}")
        try:
            # Generate the solution
            solution = developer.create_solution(problem)
            
            # Create a 'solutions' directory
            solutions_dir = os.path.join(os.path.dirname(__file__), 'solutions')
            
            # Save the solution
            file_path = developer.save_solution(solution, solutions_dir)
            
            print(f"✅ Solution saved to: {file_path}")
            print(f"Description: {solution.description}\n")
            print("-" * 80)
            
        except Exception as e:
            print(f"❌ Error generating solution: {str(e)}")

if __name__ == "__main__":
    main()