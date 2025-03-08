import os
from typing import Dict, Any, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Initialize ChatOpenAI with the API key
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

def analyze_code(code: str, filename: str) -> str:
    """
    Analyze code and generate documentation
    
    Args:
        code: Source code to analyze
        filename: Name of the file
        
    Returns:
        Generated documentation in Markdown format
    """
    # Extract file extension to determine language
    _, ext = os.path.splitext(filename)
    language = get_language_from_extension(ext)
    
    # Create a system prompt that guides the AI to generate comprehensive documentation
    system_prompt = f"""You are a technical documentation expert specializing in {language} code analysis.
    
    Analyze the provided code and create comprehensive documentation that includes:
    1. A high-level overview of what the file does
    2. A detailed breakdown of each function/class/component
    3. Parameters, return values, and their types
    4. Dependencies and their purposes
    5. Any important implementation details or design patterns
    6. How this file fits into the overall project architecture
    
    Format the documentation in Markdown with appropriate headings, code blocks, and sections.
    Use the following structure:
    
    # File: [filename]
    
    ## Overview
    [Brief description of the file's purpose]
    
    ## Dependencies
    [List of imports/dependencies and their purposes]
    
    ## Components
    
    ### [Component Name]
    [Description]
    
    #### Parameters
    - `param1` (type): Description
    - `param2` (type): Description
    
    #### Returns
    - (type): Description
    
    #### Example Usage
    ```{language}
    [Example code showing how to use this component]
    ```
    
    ## Implementation Details
    [Any important implementation details, algorithms, or design patterns]
    """
    
    # Create a human message that provides the code to analyze
    human_prompt = f"File: {filename}\n\nCode:\n```{language}\n{code}\n```\n\nPlease generate comprehensive technical documentation for this file."
    
    # Call the LLM to generate documentation
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    response = llm(messages)
    documentation = response.content
    
    return documentation

def analyze_repository_structure(files: List[Dict[str, Any]]) -> str:
    """
    Analyze the structure of a repository and generate documentation
    
    Args:
        files: List of file information dictionaries
        
    Returns:
        Generated documentation about the repository structure
    """
    # Create a file tree representation
    file_tree = "\n".join([file["path"] for file in files])
    
    # Create a system prompt that guides the AI to analyze the repository structure
    system_prompt = """You are a technical documentation expert specializing in software architecture.
    
    Analyze the provided repository structure and create comprehensive documentation that includes:
    1. An overview of the project's architecture
    2. Key components and their purposes
    3. The relationships between components
    4. Design patterns identified in the structure
    
    Format the documentation in Markdown with appropriate headings and sections.
    """
    
    # Create a human message that provides the repository structure
    human_prompt = f"Repository Structure:\n\n```\n{file_tree}\n```\n\nPlease analyze this repository structure and generate documentation about the overall architecture."
    
    # Call the LLM to generate documentation
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    response = llm(messages)
    documentation = response.content
    
    return documentation

def get_language_from_extension(extension: str) -> str:
    """
    Get programming language name from file extension
    
    Args:
        extension: File extension (e.g., '.py', '.js')
        
    Returns:
        Language name
    """
    language_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React JSX',
        '.tsx': 'React TSX',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.cs': 'C#',
        '.go': 'Go',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.rs': 'Rust',
        '.scala': 'Scala',
        '.html': 'HTML',
        '.css': 'CSS',
        '.sh': 'Shell',
        '.md': 'Markdown',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.xml': 'XML',
        '.sql': 'SQL',
        '.r': 'R',
        '.dart': 'Dart',
        '.lua': 'Lua',
        '.ex': 'Elixir',
        '.exs': 'Elixir',
        '.clj': 'Clojure',
        '.elm': 'Elm',
        '.hs': 'Haskell',
        '.m': 'Objective-C',
        '.mm': 'Objective-C++',
        '.pl': 'Perl',
        '.pm': 'Perl',
        '.f': 'Fortran',
        '.f90': 'Fortran',
        '.jl': 'Julia'
    }
    
    return language_map.get(extension.lower(), 'Unknown')

def generate_readme(repository_name: str, files: List[Dict[str, Any]]) -> str:
    """
    Generate a README for the repository
    
    Args:
        repository_name: Name of the repository
        files: List of file information dictionaries
        
    Returns:
        Generated README in Markdown format
    """
    # Create a file tree representation
    file_tree = "\n".join([file["path"] for file in files])
    
    # Extract common patterns from filenames
    extensions = {}
    for file in files:
        _, ext = os.path.splitext(file["name"])
        if ext:
            extensions[ext] = extensions.get(ext, 0) + 1
    
    # Determine main programming languages
    languages = []
    for ext, count in extensions.items():
        language = get_language_from_extension(ext)
        if language != "Unknown":
            languages.append(language)
    
    main_languages = ", ".join(set(languages))
    
    # Create a system prompt for README generation
    system_prompt = """You are a technical documentation expert specializing in creating README files.
    
    Generate a comprehensive README.md file for the repository that includes:
    1. Project title and description
    2. Key features
    3. Tech stack (languages, frameworks, libraries)
    4. Installation instructions
    5. Usage examples
    6. Project structure overview
    7. Contributing guidelines
    8. License information
    
    Format the documentation in Markdown with appropriate headings, code blocks, and sections.
    """
    
    # Create a human message that provides repository information
    human_prompt = f"""Repository Name: {repository_name}
    
    Main Languages: {main_languages}
    
    Repository Structure:
    ```
    {file_tree}
    ```
    
    Please generate a comprehensive README.md file for this repository.
    """
    
    # Call the LLM to generate the README
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    response = llm(messages)
    readme = response.content
    
    return readme