import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GitHub settings
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Confluence settings
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY", "DEV")
PARENT_PAGE_ID = os.getenv("PARENT_PAGE_ID")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

def validate_configuration() -> Dict[str, Any]:
    """
    Validate that all required configuration variables are set
    
    Returns:
        Dictionary with validation results
    """
    missing = []
    
    # Check GitHub settings
    if not GITHUB_TOKEN:
        missing.append("GITHUB_TOKEN")
    
    # Check Confluence settings
    if not CONFLUENCE_URL:
        missing.append("CONFLUENCE_URL")
    if not CONFLUENCE_USER:
        missing.append("CONFLUENCE_USER")
    if not CONFLUENCE_API_TOKEN:
        missing.append("CONFLUENCE_API_TOKEN")
    if not PARENT_PAGE_ID:
        missing.append("PARENT_PAGE_ID")
    
    # Check OpenAI settings
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    
    return {
        "valid": len(missing) == 0,
        "missing": missing
    }

def get_config() -> Dict[str, Any]:
    """
    Get all configuration settings
    
    Returns:
        Dictionary with all config values
    """
    return {
        "github": {
            "token": GITHUB_TOKEN
        },
        "confluence": {
            "url": CONFLUENCE_URL,
            "user": CONFLUENCE_USER,
            "token": CONFLUENCE_API_TOKEN,
            "space_key": CONFLUENCE_SPACE_KEY,
            "parent_page_id": PARENT_PAGE_ID
        },
        "openai": {
            "api_key": OPENAI_API_KEY,
            "model": OPENAI_MODEL
        }
    }

def update_config(key: str, value: str) -> None:
    """
    Update a configuration setting for the current session
    
    Args:
        key: Environment variable key
        value: Value to set
    """
    os.environ[key] = value