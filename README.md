# Documentation Generator

An intelligent workflow automation system that fetches code from GitHub, analyzes its structure, generates comprehensive technical documentation, and automatically updates Confluence pages. This system uses LangGraph for multi-agent orchestration, OpenAI for code analysis, and Streamlit for an interactive user interface.

## 🚀 Key Features

- **GitHub Integration**: Dynamically fetch source code from any GitHub repository
- **AI-Powered Analysis**: Analyze code structure, functions, and purpose using OpenAI LLMs
- **Automated Documentation**: Generate detailed technical documentation in Markdown format
- **Confluence Integration**: Automatically update Confluence pages with generated documentation
- **Multi-Agent Workflow**: Orchestrate the entire process using LangGraph's AI agents
- **Interactive UI**: User-friendly Streamlit interface for easy operation
- **Mock Testing Mode**: Test the application without any actual API keys or credentials

## 🛠️ Tech Stack

- **LangGraph**: AI-powered multi-agent workflow automation
- **OpenAI GPT-4**: Intelligent code analysis and documentation generation
- **GitHub API**: Fetching repository contents
- **Confluence API**: Updating documentation pages
- **Streamlit**: Web UI for user interaction
- **Python**: Core application logic

## 📋 Prerequisites

- Python 3.8 or higher
- GitHub Personal Access Token
- Confluence API credentials
- OpenAI API key

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sylvester-francis/DocumentationGenerator
   cd DocumentationGenerator
   ```

2. **Set up the environment**
   ```bash
   # Run the setup script
   bash setup.sh
   
   # Or manually:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Copy the `.env.sample` file to `.env` and add your API keys:
   ```bash
   cp .env.sample .env
   # Edit .env with your favorite text editor
   ```
   
   Required environment variables:
   - `GITHUB_TOKEN`: Your GitHub Personal Access Token
   - `CONFLUENCE_URL`: Your Confluence instance URL
   - `CONFLUENCE_USER`: Your Confluence username/email
   - `CONFLUENCE_API_TOKEN`: Your Confluence API token
   - `CONFLUENCE_SPACE_KEY`: Your Confluence space key
   - `PARENT_PAGE_ID`: ID of the parent page where documentation will be added
   - `OPENAI_API_KEY`: Your OpenAI API key

## 🚀 Usage

### Running the Full Application

```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the Streamlit app
streamlit run app.py
```

### Using the Application

1. Enter the GitHub repository owner and name
2. Optionally specify a path within the repository to analyze
3. Click "Generate Documentation" to start the process
4. View the generated documentation in the preview tab
5. Documentation will also be updated in Confluence automatically

## 🧪 Testing Without API Keys

The application includes a mock mode for testing without real API keys:

### Running the Mock UI

```bash
streamlit run app_mock.py
```

### Running the Command-Line Test

```bash
python test_app.py
```

### Testing Just the Code Analyzer

```bash
python test_analyzer.py src/main.py
```

## 📁 Project Structure

```
DocumentationGenerator/
├── .env.mock                     # Mock environment variables
├── .env.sample                   # Sample environment variables
├── .gitignore                    # Git ignore file
├── README.md                     # Project README
├── app.py                        # Main Streamlit application
├── app_mock.py                   # Mock Streamlit application
├── requirements.txt              # Project dependencies
├── setup.sh                      # Setup script
├── test_analyzer.py              # Tool to test just the code analyzer
├── test_app.py                   # Script to test the full application
│
└── src/                          # Source code directory
    ├── __init__.py               # Package initializer
    ├── code_analyzer.py          # Code analysis module
    ├── config.py                 # Configuration module
    ├── confluence_updater.py     # Confluence update module
    ├── github_fetcher.py         # GitHub fetching module
    ├── main.py                   # Main script
    ├── ui.py                     # Original UI script
    ├── workflow.py               # LangGraph workflow
    ├── workflow_test.py          # Test version of workflow
    │
    └── mock/                     # Mock implementations for testing
        ├── __init__.py           # Mock environment initializer
        ├── code_analyzer.py      # Mock code analyzer
        ├── confluence_updater.py # Mock confluence updater
        └── github_fetcher.py     # Mock GitHub fetcher
```

## 🔄 Workflow Process

1. **GitHub Fetcher Agent**: Fetches code files from the specified repository
2. **Code Analyzer Agent**: Analyzes each file and generates comprehensive documentation
3. **Confluence Updater Agent**: Updates Confluence with the generated documentation
4. **LangGraph Orchestration**: Manages the state transitions and flow between agents

## 🛠️ Extending the Application

The modular design makes it easy to extend the application:

- **Support for More Languages**: Add language-specific analysis in the code analyzer
- **Additional Documentation Types**: Generate UML diagrams, sequence diagrams, etc.
- **CI/CD Integration**: Run as part of your CI/CD pipeline to keep documentation updated
- **Custom Templates**: Add support for custom documentation templates

## 📝 License

MIT License - See LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 🙏 Acknowledgments

- LangGraph for the multi-agent workflow framework
- OpenAI for the powerful language models
- Streamlit for the easy-to-use UI framework