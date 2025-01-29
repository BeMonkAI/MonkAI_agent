<img src="./assets/mascote_monkai.png" alt="Logo" width="150">


<h2 style="font-family: 'Courier New', monospace; color: green;"> MonkAI Agent</h2>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<h3 style="font-family: 'Courier New', monospace; color: green;"> The simple <span style="color:yellow;">open source framework</span> for creating intelligent agents, flows quickly, easily, and customizable.</h3>

<p style="text-align: justify;">
  This is an innovative framework designed to facilitate the creation of intelligent agent flows, offering a simple and customizable approach to the development of autonomous agents.
</p>  

<p style="text-align: justify;">    
  With this framework, you can create, manage, and optimize agents quickly and efficiently. Whether for specific tasks or more complex applications, it provides a modular base that adapts to your needs. Its simplicity of use, combined with its flexibility, makes it an ideal choice for both beginners and experienced developers.
</p>

<h3 style="font-family: 'Courier New', monospace; color: green;">Install</h3> 

<p style="font-family: Arial, sans-serif; font-size: 16px; color: #555;">
Make sure you have Python 3.11 or higher installed on your system.

Clone this repository:

<pre style="background-color: #f6f8fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
 git clone https://github.com/BeMonkAI/MonkAI_agent.git
</pre>

Navigate to the project directory and install the dependencies:

<pre style="background-color: #f6f8fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
pip install -r requirements.txt
</pre>

or

<pre style="background-color: #f6f8fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
pip install monkai_agent

</pre>  

<h2 style="font-family: 'Courier New', monospace; color: green;">Arquitecture</h2>  

<h3 style="font-family: 'Courier New', monospace; color: green;">Main Components</h3>  

<p style="text-align: justify;">
The <code>monkai_agent/</code> module concentrates on the main components responsible for the central logic of the system. It defines classes and fundamental structures for creating and managing agents and offering security mechanisms.
</p>

<p style="text-align: justify;">
Definition and Management of Agents: Structures for creating and managing agents are only provided by specialized classes. These classes follow a hierarchy that allows extending and personalizing the behavior of two agents, such as triage and transfer agents.
</p>

<p style="text-align: justify;">
Security and Validation: A validation decorator protects sensitive functions, verifying whether users can access them. If validation is done, the function is executed; Otherwise, access will be denied with an appropriate message.
</p>

<p style="text-align: justify;">
The modules' imports and objects are directly related to offering a robust and secure monkai_agent for the system, focusing on the efficient management of agents and protection of their critical functionalities.
</p>

<h3 style="font-family: 'Courier New', monospace; color: green;">System Logic Modules</h3> 

<code>base</code>: Responsible for providing the core functionality and type definitions for the MonkAI agent. It sets up the necessary environment, including logging configuration, importing essential modules, and defining global variables and constants. In addition, it imports and uses utility functions and specific types necessary for the efficient operation of the agent.

<code>monkai_agent_criator</code>: This module establishes the main structure for creating agent instances within the MonkAI framework. It provides an abstract class, 'MonkaiAgentCreator', a template for developing various types of agents, ensuring that all subclasses implement the essential methods for creating and describing agents. In addition, it includes a concrete class, 'TransferTriageAgentCreator', which extends 'MonkaiAgentCreator' and implements specific logic for creating and managing a triage agent.

<code>repl</code>: This module is responsible for processing and printing streaming responses from an agent, formatting the output with colors for easy viewing on the terminal. The term REPL is widely recognized in the development community and reflects the classic Read-Eval-Print Loop pattern commonly used in interactive environments. This choice reinforces familiarity and facilitates understanding of its purpose within the framework.

<code>security</code>: This module is one of the main differentiators of the framework, designed to offer robust security through access validation. It stands out by providing a validation decorator, an efficient mechanism that automates protecting sensitive functions, ensuring access only to properly validated users.

The 'validate' decorator creates a wrapper around the protected function, ensuring only authenticated users can access the agents' functions. The developer only needs to implement the specific validation logic. If the validation fails, the decorator blocks the function's execution and returns a clear "access denied" message.

Security is managed centrally and independently and is not the direct responsibility of the agents. This approach adds an extra layer of protection, ensuring that security is above the level of the agents and eliminating vulnerabilities caused by inconsistencies in the validations implemented individually.

Key Features:

- Simple Integration: Decorators automate validations, eliminating the need for manual checks.

- Centralized Security: Validation is managed from a single point, reducing errors and ensuring consistency across the system.

- Flexible Customization: Access conditions can be adapted to different scenarios or user profiles.

<code>triage_agent_creator</code>: This module is a standout feature of the MonkAI framework, setting it apart by enabling the seamless creation and management of triage agents. These agents ensure efficient user interaction by determining the most appropriate agent to handle each user's request.

The <code>TriageAgentCreator</code> class, a key component of this module, extends the abstract <code>MonkaiAgentCreator</code> and incorporates advanced logic for triage management. Its functionality includes creating dynamic handoff functions, which allow conversations to be redirected to the right agent based on the context and user needs.

Key Features:

- Centralized Decision Making: Simplifies determining agent responsibilities, reducing complexity in multi-agent systems.

- Improved User Experience: Ensures users are routed to the correct agent promptly, minimizing delays and miscommunication.

- Customizable and Scalable: The triage logic is flexible and can adapt to various application scenarios, making it suitable for projects of any scale.

This module exemplifies the innovation and practicality at the core of MonkAI, providing a robust solution for efficient agent orchestration.

<code>types</code>: This module defines the data types and models the MonkAI agent uses. It includes class and type definitions representing the agent's functions, processable messages, instructions, and associated models. These definitions are crucial in ensuring data consistency and validation, facilitating maintenance and continuous scalability of the codebase.

<code>util</code>: Responsible for providing utility functions that aid in the functioning of the MonkAI agent. These functions include printing debug messages with timestamps, merging dictionary fields, and handling chunked responses. These utilities are essential to the maintenance and efficient operation of the agent, providing supporting functionality that is reused in multiple parts of the code.

<h3 style="font-family: 'Courier New', monospace; color: green;">Practical Module</h3> 

<p style="text-align: justify;">
The <code>examples/</code> module serves as a repository of practical cases that demonstrate how to use the central components of the system, especially the breeding agents defined in the monkai_agent module. It presents specific implementations of breeding agents for different tasks, using the breeder agent class as a basis. It constitutes a bridge between the abstract logic of the <code>monkai_agent</code> and the practical application, allowing users to explore the system's capabilities and adapt the breeding agents to their needs.
</p>

<p style="text-align: justify;">
Application: The main purpose of this module is to illustrate the flexibility and extensibility of the system, providing practical cases and customization of agents for different scenarios. It guides developers, showing how to create and adapt specialized agents using the <code>monkai_agent</code> structure efficiently, maximizing code reuse, and adding to the defined monkai_agent architecture.
</p>

<h3 style="font-family: 'Courier New', monospace; color: green;">Interaction Diagram</h3> 

<p style="text-align: justify;"> 
The framework architecture is modular and extensive, allowing the creation and management of AI agents interacting with the user. The <code>AgentManager</code> is the central management and orchestration point, coordinating the interactions between the user and the agents.
</p>

<img src="./assets/Arq1.png" alt="Logo">


<p style="text-align: justify;">
<code>AgentManager</code>: Manages interaction with agents. Initializes with a client, a list of agent creators, context variables, and streaming and debugging options. Has methods to execute conversations asynchronously.
</p>

<p style="text-align: justify;">
<code>MonkaiAgentCreator</code>: This is an abstract class that creates agent instances, returns an Agent object, and provides a brief description of its capabilities. It can be configured to create different types of agents based on the system's needs.
</p>

<p style="text-align: justify;">
<code>TriaggentAgentCreator</code>: Inherits from <code>MonkaiAgentCreator</code>, it creates the triage agent that decides which agent should handle the user's request. Based on the instructions provided, it makes functions that transfer the conversation to the appropriate agent. When the selected agent can no longer respond to a given task, the triggering agent is triggered again to choose another agent that better adapts to the needs of the user's request. It provides clear instructions on when to transfer the conversation to each specific agent, a notable difference from this framework. 
</p>

<h4 style="font-family: 'Courier New', monospace; color: green;">Agents Examples</h4>   

<p style="text-align: justify;">
<code>PythonDeveloperAgentCreator</code>: Responsible for creating and managing Python development agents within the system. Provides features related to software development in Python, such as generating code, documenting, testing, and optimizing Python code by generating an executable .py file. Encapsulates the logic needed to create an agent specialized in performing software development tasks in Python to help automate and facilitate the work of Python developers.
</p> 

<p style="text-align: justify;">
<code>ResearcherAgentCreator</code>: Responsible for creating and managing research agents within the system. This agent provides features related to information research, such as searching for data, analyzing content, and providing answers based on collected information, and also returns links to the sources consulted. Encapsulates the logic needed to create an agent specialized in performing information research tasks.
</p> 

<p style="text-align: justify;">
<code>CalculatorAgentCreator</code>: Responsible for creating and managing calculation agents within the system and providing features related to mathematical operations. Encapsulates the logic needed to make an agent specialized in performing mathematical calculations.
</p> 

<p style="text-align: justify;">
<code>JournalistAgentCreator</code>: Created and managed journalism agents within the system. This agent provides functionalities for collecting, analyzing, and summarizing news and articles. It encapsulates the logic required to create an agent specialized in performing journalism tasks, such as reading and summarizing news.
</p> 

<p style="text-align: justify;">
In the <code>demo.py</code> file demonstrates how the multi-agent system works, including the efficient execution of all specialized agents: Python Developer Agent, Researcher, Journalist, and Secure Calculator. It is a practical demonstration of how these agents are managed and operate together.
</p>  

