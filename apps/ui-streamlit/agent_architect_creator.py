from monkai_agent import MonkaiAgentCreator, Agent, Result
from typing import Optional, Dict, List
import json

class AgentArchitectCreator(MonkaiAgentCreator):
    """
    Creates an agent that specializes in designing and generating MonkAI framework agents.
    This creator helps users build agents that conform to the framework's architecture.
    """
    
    def __init__(self):
        super().__init__()
        self.agent = Agent(
            name="Agent Architect",
            instructions="""You are an expert AI agent specialized in creating MonkAI framework agents.
            You understand the framework's architecture and can help users create new agents that follow best practices.
            
            When designing agents, consider:
            1. Clear agent purpose and responsibilities
            2. Well-defined functions with proper type hints
            3. Security considerations using decorators
            4. Error handling and validation
            5. Integration with the framework's core features
            
            Always follow the MonkAI framework patterns and conventions.
            """,
            functions=[
                self.create_agent_template,
                self.validate_agent_structure,
                self.generate_agent_code
            ],
            tool_choice="auto"
        )

    def _parse_functions_string(self, functions_str: str) -> List[Dict[str, str]]:
        """
        Parse functions string in the format:
        '1. function_name: function description'
        
        Returns list of dicts with name and description
        """
        functions = []
        if not functions_str:
            return functions
            
        for line in functions_str.split('\n'):
            if not line.strip() or ':' not in line:
                continue
                
            # Remove number and dot prefix
            clean_line = line.split('.', 1)[-1].strip()
            name_part, desc = [x.strip() for x in clean_line.split(':', 1)]
            
            # Clean up function name
            # Remove any parentheses and their contents
            name = name_part.split('(')[0].strip()
            
            # Replace invalid characters with underscores
            import re
            name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
            
            # Ensure name starts with letter or underscore
            if name and not name[0].isalpha() and name[0] != '_':
                name = f'_{name}'
                
            functions.append({
                'name': name,
                'description': desc.strip(),
                'parameters': 'self'  # Default parameters
            })
            
        return functions

    def create_agent_template(self, agent_name: str, purpose: str, functions: str) -> Result:
        """
        Creates a template for a new agent based on provided specifications.

        Args:
            agent_name: Name of the agent to create
            purpose: Main purpose and responsibilities of the agent
            functions: String containing numbered list of functions and their descriptions

        Returns:
            Result containing the agent template code
        """
        parsed_functions = self._parse_functions_string(functions)
        function_names = [f['name'] for f in parsed_functions]
        
        template = f"""from monkai_agent import MonkaiAgentCreator, Agent, Result
from typing import Optional, Dict, Any

class {agent_name}Creator(MonkaiAgentCreator):
    def __init__(self):
        super().__init__()
        self.agent = Agent(
            name="{agent_name}",
            instructions=\"\"\"{purpose}\"\"\",
            functions=[{', '.join(f'self.{f}' for f in function_names)}],
            tool_choice="auto"
        )
        
    def get_agent(self) -> Agent:
        return self.agent
        
    def get_agent_briefing(self) -> str:
        return "{purpose}"
"""
        for func in parsed_functions:
            template += f"""
    def {func['name']}(self) -> Result:
        \"\"\"
        {func['description']}
        \"\"\"
        return Result(value="Not implemented")
"""
        
        return Result(
            value=json.dumps({
                "code": template,
                "message": f"Created template for {agent_name} agent"
            })
        )

    def validate_agent_structure(self, agent_code: str) -> Result:
        """
        Validates if the provided agent code follows framework architecture.

        Args:
            agent_code: The agent implementation code to validate

        Returns:
            Result containing validation findings
        """
        validation_results = []
        
        # Check for required imports
        if "from monkai_agent import" not in agent_code:
            validation_results.append("Missing required MonkAI framework imports")
            
        # Check class inheritance
        if "MonkaiAgentCreator)" not in agent_code:
            validation_results.append("Agent creator must inherit from MonkaiAgentCreator")
            
        # Check required methods
        required_methods = ["get_agent", "get_agent_briefing"]
        for method in required_methods:
            if f"def {method}" not in agent_code:
                validation_results.append(f"Missing required method: {method}")
                
        if validation_results:
            return Result(
                value=json.dumps({
                    "valid": False,
                    "issues": validation_results
                })
            )
        
        return Result(
            value=json.dumps({
                "valid": True,
                "message": "Agent structure follows framework architecture"
            })
        )

    def generate_agent_code(self, 
                          agent_name: str,
                          purpose: str,
                          functions: str) -> Result:
        """
        Generates complete agent code with implemented functions.

        Args:
            agent_name: Name of the agent
            purpose: Agent's purpose description
            functions: String containing numbered list of functions and their descriptions

        Returns:
            Result containing the complete agent implementation
        """
        parsed_functions = self._parse_functions_string(functions)
        function_implementations = []
        function_references = []
        
        for func in parsed_functions:
            func_name = func['name']
            function_references.append(f"self.{func_name}")
            
            impl = f"""
    def {func_name}(self) -> Result:
        \"\"\"
        {func['description']}
        \"\"\"
        # TODO: Implement function logic
        return Result(value="Implementation pending")
"""
            function_implementations.append(impl)

        code = f"""from monkai_agent import MonkaiAgentCreator, Agent, Result
from typing import Optional, Dict, Any

class {agent_name}Creator(MonkaiAgentCreator):
    \"\"\"
    {purpose}
    \"\"\"
    
    def __init__(self):
        super().__init__()
        self.agent = Agent(
            name="{agent_name}",
            instructions=\"\"\"{purpose}\"\"\",
            functions=[{', '.join(function_references)}],
            tool_choice="auto"
        )
    
    def get_agent(self) -> Agent:
        return self.agent
        
    def get_agent_briefing(self) -> str:
        return "{purpose}"
        
{"".join(function_implementations)}
"""
        
        return Result(
            value=json.dumps({
                "code": code,
                "message": f"Generated complete implementation for {agent_name} agent"
            })
        )

    def get_agent(self) -> Agent:
        """Returns the agent architect agent instance."""
        return self.agent
    
    def get_agent_briefing(self) -> str:
        """Returns a brief description of the agent architect's capabilities."""
        return "Expert agent for designing and generating MonkAI framework agents"
