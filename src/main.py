from github_fetcher import fetch_repo_files
from code_analyzer import analyze_code
from confluence_updater import create_or_update_confluence_page
import requests

def main():
    repo_path = input("Enter GitHub Repository Path: ")
    files = fetch_repo_files(repo_path)
    
    if files:
        for file in files:
            if file["type"] == "file":
                file_content = requests.get(file["download_url"]).text
                doc = analyze_code(file_content)
                create_or_update_confluence_page(file["name"], doc)
                print(f"Documentation for {file['name']} updated in Confluence!")

if __name__ == "__main__":
    main()
