import os
import sys
from typing import Dict, Any

def init_mock_environment():
    """Initialize the mock environment for testing"""
    # 1. Set the MOCK_MODE environment variable
    os.environ["MOCK_MODE"] = "True"
    
    # 2. Set mock API keys and credentials
    os.environ["GITHUB_TOKEN"] = "mock_github_token"
    os.environ["CONFLUENCE_URL"] = "https://mock-confluence.atlassian.net"
    os.environ["CONFLUENCE_USER"] = "mock_user@example.com"
    os.environ["CONFLUENCE_API_TOKEN"] = "mock_confluence_token"
    os.environ["CONFLUENCE_SPACE_KEY"] = "MOCK"
    os.environ["PARENT_PAGE_ID"] = "12345"
    os.environ["OPENAI_API_KEY"] = "mock_openai_key"
    os.environ["OPENAI_MODEL"] = "mock-model"
    
    # 3. Set up module import redirection
    # This will redirect imports of real modules to their mock versions
    sys.modules["src.github_fetcher"] = __import__("src.mock.github_fetcher", fromlist=["*"])
    sys.modules["src.code_analyzer"] = __import__("src.mock.code_analyzer", fromlist=["*"])
    sys.modules["src.confluence_updater"] = __import__("src.mock.confluence_updater", fromlist=["*"])
    
    print("Mock environment initialized")