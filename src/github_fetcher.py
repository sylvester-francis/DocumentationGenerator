import requests
import os
import base64
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_repo_files(repo_owner: str, repo_name: str, path: str = "") -> List[Dict[str, Any]]:
    """
    Fetch files from a GitHub repository
    
    Args:
        repo_owner: Repository owner
        repo_name: Repository name
        path: Path within the repository
        
    Returns:
        List of file information dictionaries
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub data: {str(e)}")
        return []

def get_file_content(download_url: str) -> str:
    """
    Get content of a file from GitHub
    
    Args:
        download_url: URL to download the file content
        
    Returns:
        File content as string
    """
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file content: {str(e)}")
        return ""

def get_file_content_by_path(repo_owner: str, repo_name: str, file_path: str) -> str:
    """
    Get content of a file by its path in the repository
    
    Args:
        repo_owner: Repository owner
        repo_name: Repository name
        file_path: Path to the file in the repository
        
    Returns:
        File content as string
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        content_data = response.json()
        if content_data.get("encoding") == "base64" and content_data.get("content"):
            content = base64.b64decode(content_data["content"]).decode("utf-8")
            return content
        return ""
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file content by path: {str(e)}")
        return ""