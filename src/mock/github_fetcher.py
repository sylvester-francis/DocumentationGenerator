import os
from typing import List, Dict, Any
import json

# Sample mock repository data
MOCK_REPO_DATA = {
    "main": [
        {
            "name": "app.py",
            "path": "app.py",
            "type": "file",
            "download_url": "https://mock-github.com/download/app.py"
        },
        {
            "name": "requirements.txt",
            "path": "requirements.txt",
            "type": "file",
            "download_url": "https://mock-github.com/download/requirements.txt"
        },
        {
            "name": "src",
            "path": "src",
            "type": "dir",
            "download_url": None
        },
        {
            "name": "README.md",
            "path": "README.md",
            "type": "file",
            "download_url": "https://mock-github.com/download/README.md"
        }
    ],
    "src": [
        {
            "name": "main.py",
            "path": "src/main.py",
            "type": "file",
            "download_url": "https://mock-github.com/download/src/main.py"
        },
        {
            "name": "config.py",
            "path": "src/config.py",
            "type": "file",
            "download_url": "https://mock-github.com/download/src/config.py"
        },
        {
            "name": "utils.py",
            "path": "src/utils.py",
            "type": "file",
            "download_url": "https://mock-github.com/download/src/utils.py"
        }
    ]
}

# Sample mock file content
MOCK_FILE_CONTENT = {
    "app.py": """
import streamlit as st
from src.main import process_data

def main():
    st.title("Sample App")
    data = st.file_uploader("Upload data")
    if data:
        result = process_data(data)
        st.write(result)

if __name__ == "__main__":
    main()
""",
    "src/main.py": """
from .utils import clean_data, analyze_data
from .config import get_config

def process_data(data_file):
    \"\"\"Process the uploaded data file and return analysis results\"\"\"
    config = get_config()
    data = clean_data(data_file, config['cleaning_params'])
    return analyze_data(data, config['analysis_params'])
""",
    "src/config.py": """
def get_config():
    \"\"\"Return application configuration\"\"\"
    return {
        'cleaning_params': {
            'remove_duplicates': True,
            'fill_missing': 'mean'
        },
        'analysis_params': {
            'method': 'regression',
            'confidence_level': 0.95
        }
    }
""",
    "src/utils.py": """
def clean_data(data_file, params):
    \"\"\"Clean the input data according to the parameters\"\"\"
    # In a real implementation, this would perform data cleaning
    return data_file

def analyze_data(data, params):
    \"\"\"Analyze the data according to the parameters\"\"\"
    # In a real implementation, this would perform data analysis
    return {
        'status': 'success',
        'method': params['method'],
        'confidence': params['confidence_level'],
        'result': 'Sample analysis result'
    }
"""
}

def fetch_repo_files(repo_owner: str, repo_name: str, path: str = "") -> List[Dict[str, Any]]:
    """Mock implementation of fetch_repo_files"""
    # For testing, we'll just return mock data based on the path
    if path == "":
        return MOCK_REPO_DATA["main"]
    elif path == "src":
        return MOCK_REPO_DATA["src"]
    else:
        return []

def get_file_content(download_url: str) -> str:
    """Mock implementation of get_file_content"""
    # Extract the file path from the mock download URL
    file_path = download_url.replace("https://mock-github.com/download/", "")
    
    # Return mock content if available
    if file_path in MOCK_FILE_CONTENT:
        return MOCK_FILE_CONTENT[file_path]
    else:
        return f"Mock content for {file_path}"

def get_file_content_by_path(repo_owner: str, repo_name: str, file_path: str) -> str:
    """Mock implementation of get_file_content_by_path"""
    if file_path in MOCK_FILE_CONTENT:
        return MOCK_FILE_CONTENT[file_path]
    else:
        return f"Mock content for {file_path}"