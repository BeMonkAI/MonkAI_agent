from pydantic import BaseModel
from typing import Optional
import os
from monkai_agent.groq import GroqProvider
import config

class PythonSolution(BaseModel):
    file_name: str
    code: str
    description: str

class PythonDeveloperAgent:
    def __init__(self, api_key: str):
        self.provider = GroqProvider(api_key=api_key)
        
    def create_solution(self, problem: str) -> PythonSolution:
        prompt = f"""
        Act as an expert Python developer. Create a solution for the following problem:
        {problem}
        
        Provide your response in the following format:
        - A descriptive Python file name
        - The complete Python code solution
        - A brief description of how the solution works
        
        Make sure the code is well-documented, follows PEP 8 standards, and includes error handling.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert Python developer that creates well-documented and PEP 8 compliant code."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.provider.get_completion(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        # Parse the response to extract file name, code, and description
        lines = response.choices[0].message.content.split('\n')
        file_name = lines[0].strip().rstrip('.py') + '.py'
        code_lines = []
        description = ""
        
        parsing_code = False
        for line in lines[1:]:
            if line.startswith('"""') or line.startswith("'''"):
                parsing_code = not parsing_code
                continue
            if parsing_code:
                code_lines.append(line)
            else:
                if line.strip() and not line.startswith('#'):
                    description += line.strip() + " "
        
        return PythonSolution(
            file_name=file_name,
            code="\n".join(code_lines),
            description=description.strip()
        )
    
    def save_solution(self, solution: PythonSolution, directory: Optional[str] = None) -> str:
        """
        Saves the Python solution to a file in the specified directory.
        Returns the full path of the created file.
        """
        if directory is None:
            directory = os.getcwd()
            
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        file_path = os.path.join(directory, solution.file_name)
        
        with open(file_path, 'w') as f:
            f.write(f'"""\n{solution.description}\n"""\n\n')
            f.write(solution.code)
            
        return file_path

# Example usage
if __name__ == "__main__":
    developer = PythonDeveloperAgent(api_key=config.GROQ_API_KEY)
    
    # Example problem
    problem = "Create a function that calculates the Fibonacci sequence up to n terms"
    
    # Generate solution
    solution = developer.create_solution(problem)
    
    # Save the solution
    file_path = developer.save_solution(solution)
    print(f"Solution saved to: {file_path}")
    print(f"Description: {solution.description}")

