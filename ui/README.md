# MonkAI Framework Developer UI

This directory contains the Streamlit-based user interface for the MonkAI Framework Developer Assistant.

## Features

- **LLM Provider Selection**: Choose between OpenAI and Groq
- **API Key Management**: Securely input and manage your API keys
- **Model Selection**: Select from available models for each provider
- **Interactive Chat Interface**: Ask questions and get responses about the MonkAI framework
- **Code Generation**: Receive properly formatted code examples with dependencies
- **Chat History**: Save and manage your conversation history

## Getting Started

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit interface:
```bash
streamlit run monkai_agent_ui.py
```

3. Open your browser and navigate to http://localhost:8501

## Usage

1. Select your preferred LLM provider (OpenAI or Groq)
2. Enter your API key in the sidebar
3. Choose a model from the available options
4. Start asking questions about the MonkAI framework

The assistant can help with:
- Framework components and their relationships
- Class and method documentation
- Code generation following framework patterns
- Integration examples
- Best practices and conventions

## Advanced Settings

The interface includes advanced settings for:
- Temperature control (0.0 - 2.0)
- Max tokens limit (1 - 4096)

## Chat Management

- **Clear Chat**: Reset the conversation
- **Save Chat**: Export the conversation history to a JSON file

## Directory Structure

```
ui/
├── README.md           # This documentation
├── requirements.txt    # Project dependencies
├── monkai_agent_ui.py # Main Streamlit interface
└── assets/            # UI assets and resources
```

## Contributing

Feel free to submit issues and enhancement requests! 