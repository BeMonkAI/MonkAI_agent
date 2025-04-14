# MonkAI Agent Framework Documentation

## Overview
MonkAI Agent is an open-source framework designed for creating intelligent agent flows. It provides a simple and customizable approach to developing autonomous agents, making it suitable for both beginners and experienced developers.

## Project Structure
```
MonkAI_agent/
├── apps/                  # Application-specific implementations
├── assets/               # Static assets (images, etc.)
├── dist/                 # Distribution files
├── libs/                 # Core libraries
│   ├── monkai_agent/     # Main framework
│   └── monkai_agent_groq/ # Groq-specific implementations
├── .vscode/              # VS Code configuration
├── venv/                 # Python virtual environment
├── pyproject.toml        # Project configuration
├── requirements.txt      # Python dependencies
└── README.md            # Project overview
```

## Core Components

### 1. Main Framework (`libs/monkai_agent/src/`)
The framework consists of several key modules:

#### Base Module (`base.py`)
- Core functionality and type definitions
- Environment setup and configuration
- Global variables and constants
- Essential utility functions

#### Agent Creation (`monkai_agent_creator.py`)
- Abstract `MonkaiAgentCreator` class
- Template for developing various agent types
- Implementation of agent creation logic

#### Security Module (`security.py`)
- Access validation mechanisms
- Security decorators
- User authentication and authorization
- Centralized security management

#### Triage System (`triage_agent_creator.py`)
- Intelligent request routing
- Dynamic agent selection
- Conversation handoff management
- Context-aware decision making

#### Memory Management (`memory.py`)
- Agent memory handling
- State persistence
- Context management

#### Prompt Optimization (`prompt_optimizer.py`)
- Prompt engineering
- Response optimization
- Context enhancement

#### Rate Limiting (`rate_limiter.py`)
- API call throttling
- Resource usage management
- Performance optimization

#### REPL Interface (`repl.py`)
- Interactive command interface
- Response streaming
- Terminal formatting

#### Type System (`types.py`)
- Data type definitions
- Model specifications
- Validation schemas

#### Utilities (`util.py`)
- Helper functions
- Common operations
- Debug utilities

### 2. Provider System (`providers.py`)
- Integration with various AI providers
- API management
- Response handling
- Error management

## Detailed Class and Function Documentation

### Core Classes

#### MonkaiAgentCreator
```python
class MonkaiAgentCreator:
    """
    Abstract base class for creating MonkAI agents.
    
    This class serves as a template for implementing various types of agents.
    It defines the core interface that all agent creators must implement.
    
    Methods:
        create_agent(): Creates and returns a new agent instance
        describe_agent(): Returns a string description of the agent
    """
```

#### TriageAgentCreator
```python
class TriageAgentCreator:
    """
    Specialized agent creator for handling request routing and agent selection.
    
    This class implements intelligent routing logic to determine which agent
    should handle a given request based on context and capabilities.
    
    Methods:
        route_request(request): Routes incoming requests to appropriate agents
        select_agent(context): Selects the most suitable agent for a given context
        handoff_conversation(from_agent, to_agent, context): Manages conversation handoffs
    """
```

### Core Functions

#### validate
```python
@validate
def validate(func):
    """
    Security decorator for function validation.
    
    This decorator ensures that functions are only executed when all security
    requirements are met. It handles authentication, authorization, and input
    validation.
    
    Args:
        func: The function to be validated
        
    Returns:
        Wrapped function with validation checks
    """
```

#### create_agent
```python
def create_agent(agent_type, config=None):
    """
    Factory function for creating new agent instances.
    
    This function provides a convenient way to create different types of agents
    with specific configurations.
    
    Args:
        agent_type: Type of agent to create
        config: Optional configuration dictionary
        
    Returns:
        New agent instance
    """
```

#### optimize_prompt
```python
def optimize_prompt(prompt, context=None):
    """
    Optimizes and enhances prompts for better AI responses.
    
    This function applies various optimization techniques to improve
    the quality and effectiveness of prompts.
    
    Args:
        prompt: Original prompt text
        context: Optional context information
        
    Returns:
        Optimized prompt
    """
```

#### manage_memory
```python
def manage_memory(agent, action, data=None):
    """
    Handles agent memory operations.
    
    This function manages the storage, retrieval, and manipulation of
    agent memory and state.
    
    Args:
        agent: Agent instance
        action: Memory operation to perform
        data: Optional data for the operation
        
    Returns:
        Result of the memory operation
    """
```

#### rate_limit
```python
def rate_limit(func):
    """
    Decorator for implementing rate limiting on functions.
    
    This decorator controls the frequency of function calls to prevent
    overuse of resources and API rate limits.
    
    Args:
        func: Function to apply rate limiting to
        
    Returns:
        Wrapped function with rate limiting
    """
```

### Utility Functions

#### format_response
```python
def format_response(response, format_type='text'):
    """
    Formats AI responses according to specified format.
    
    This function handles the formatting of agent responses for different
    output types and contexts.
    
    Args:
        response: Raw response to format
        format_type: Desired output format
        
    Returns:
        Formatted response
    """
```

#### validate_config
```python
def validate_config(config):
    """
    Validates agent configuration settings.
    
    This function ensures that all required configuration parameters
    are present and valid.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        Boolean indicating if configuration is valid
    """
```

#### debug_log
```python
def debug_log(message, level='info'):
    """
    Logs debug information with specified severity level.
    
    This function provides a standardized way to log debug information
    throughout the framework.
    
    Args:
        message: Message to log
        level: Log level (info, warning, error, debug)
    """
```

## Key Features

### 1. Modular Architecture
- Extensible design
- Component-based structure
- Easy integration of new features

### 2. Security
- Centralized security management
- Access control mechanisms
- Validation decorators
- Secure function execution

### 3. Agent Management
- Dynamic agent creation
- Intelligent routing
- Context-aware processing
- State management

### 4. Performance
- Rate limiting
- Resource optimization
- Efficient memory usage
- Streamlined processing

## Usage Examples

### Basic Agent Creation
```python
from monkai_agent import MonkaiAgentCreator

class MyAgentCreator(MonkaiAgentCreator):
    def create_agent(self):
        # Implement agent creation logic
        pass
    
    def describe_agent(self):
        # Provide agent description
        return "My custom agent"
```

### Security Implementation
```python
from monkai_agent import validate

@validate
def protected_function():
    # Function implementation
    pass
```

### Triage System Usage
```python
from monkai_agent import TriageAgentCreator

class MyTriageAgent(TriageAgentCreator):
    def route_request(self, request):
        # Implement routing logic
        pass
```

## Dependencies
- Python 3.11 or higher
- Core dependencies listed in `requirements.txt`
- Additional provider-specific requirements

## Installation
1. Clone the repository:
```bash
git clone https://github.com/BeMonkAI/MonkAI_agent.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap
- Enhanced provider support
- Advanced security features
- Improved performance optimizations
- Extended documentation
- Additional example implementations 