from monkai_agent.monkai_agent_creator import  TransferTriageAgentCreator
from monkai_agent.types import Agent
import monkai_agent.security as security
import os

class PythonDeveloperAgentCreator(TransferTriageAgentCreator):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.agent = Agent(
            name="Python Developer Agent",
           instructions="""You are a Python developer and you have to create Python code from text provided by the user.


                1. Interpret the user's text to understand the requirements of the Python code to be generated.
                2. Generate the Python code, defining classes as necessary and following good object-oriented practices. Ensure that the generated code is properly documented.
                3. Check if there is an address provided by the user in the message. If no address is provided, use the current folder.
                4. Create a .py file in the specified folder.
                5. Define a class in the created file with the functionality that meets the conditions specified by the user.
                6. If you cannot provide an answer, trigger the transfer_to_triage function to escalate the request to the triage agent.
            """,
            functions=[  
                        self.verify_address,    
                        self.create_python_file,
                        self.write_code_in_file,
                        self.transfer_to_triage
                      ])
        
    def is_user_valid(self):
        if self.user=="valid_user":
            return True
        else:
            return False
    
    
    def verify_address(self, address):
        if not address:
            return os.getcwd()
        if not os.path.isdir(address):
            return f"Endereço {address} não é valido."
        return address

    @security.validate(is_user_valid)
    def create_python_file(self, path, file_name):
        complete_path = os.path.join(path, file_name)
        with open(complete_path, 'w') as f:
            f.write('')
    
    
    @security.validate(is_user_valid)
    def write_code_in_file(self,path, file_name, code):
        """
        Write the code in the file.
        """
        complete_path = os.path.join(path, file_name)
        with open(complete_path, 'w') as f:
            f.write(code)

    def replace_code_in_file(self, path, file_name, code):
        """
        Replace the code in the file.
        """
        complete_path = os.path.join(path, file_name)
        with open(complete_path, 'w') as f:
            f.write(code)

    def get_agent(self) -> Agent:
        """
        Returns the Python Developer Agent.
        """
        return self.agent
    
    def get_agent_briefing(self) -> str:
        return "You are a Python developer and you have to create Python code from text provided by the user."

            