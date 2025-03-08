import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "repo-owner"
REPO_NAME = "repo_name"

def fetch_repo_files(path=""):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    print(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching GitHub data: {response.status_code}")
        return None
