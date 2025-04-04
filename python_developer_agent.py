from typing import Optional
import os
from crewai import Agent, Task
from langchain_groq import ChatGroq

class PythonDeveloperAgent:
    def __init__(self, groq_api_key: str):
        """
        Initialize the Python Developer Agent with Groq API key
        """
        self.groq_api_key = groq_api_key
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile"
        )
        
        self.agent = Agent(
            role='Python Developer',
            goal='Develop high-quality Python code and create Python files',
            backstory="""You are an experienced Python developer with expertise in 
            creating clean, efficient, and well-documented code. You follow best 
            practices and PEP 8 guidelines.""",
            llm=self.llm,
            verbose=True
        )

    def create_file(self, filename: str, code_content: str, directory: Optional[str] = None) -> str:
        """
        Create a Python file with the generated code
        
        Args:
            filename (str): Name of the file to create
            code_content (str): Python code to write in the file
            directory (Optional[str]): Directory where to create the file
            
        Returns:
            str: Path to the created file
        """
        if not filename.endswith('.py'):
            filename += '.py'
            
        if directory:
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
        else:
            file_path = filename
            
        with open(file_path, 'w') as f:
            f.write(code_content)
            
        return file_path

    def generate_code(self, task_description: str) -> str:
        """
        Generate Python code based on the task description
        
        Args:
            task_description (str): Description of what the code should do
            
        Returns:
            str: Generated Python code
        """
        task = Task(
            description=f"Create Python code that accomplishes the following: {task_description}",
            agent=self.agent
        )
        
        return task.execute()

# Example usage:
if __name__ == "__main__":
    # Replace with your Groq API key
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    if not GROQ_API_KEY:
        raise ValueError("Please set the GROQ_API_KEY environment variable")
    
    # Create the Python developer agent
    dev_agent = PythonDeveloperAgent(GROQ_API_KEY)
    
    # Example: Generate a simple function
    task_description = "Create a function that calculates the factorial of a number"
    generated_code = dev_agent.generate_code(task_description)
    
    # Save the generated code to a file
    file_path = dev_agent.create_file(
        filename="factorial",
        code_content=generated_code,
        directory="generated_code"
    )
    
    print(f"Code generated and saved to: {file_path}") 