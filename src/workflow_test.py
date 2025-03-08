import os
from typing import Dict, List, Any
from dotenv import load_dotenv
import time

# Check for mock mode before imports
load_dotenv()
MOCK_MODE = os.getenv("MOCK_MODE", "False").lower() in ("true", "1", "t")

if MOCK_MODE:
    # Initialize mock environment
    from src.mock import init_mock_environment
    init_mock_environment()

# Now import components (either real or mock depending on MOCK_MODE)
from src.github_fetcher import fetch_repo_files, get_file_content
from src.code_analyzer import analyze_code, analyze_repository_structure, generate_readme
from src.confluence_updater import create_or_update_confluence_page, get_confluence_space_key

class FileInfo(dict):
    """File information dictionary"""
    pass

class WorkflowState(dict):
    """Workflow state dictionary"""
    pass

def run_documentation_workflow_test(
    repo_owner: str,
    repo_name: str,
    repo_path: str = "",
    confluence_space_key: str = None,
    parent_page_id: str = None
) -> Dict[str, Any]:
    """
    Run the documentation workflow in test mode
    
    Args:
        repo_owner: GitHub repository owner
        repo_name: GitHub repository name
        repo_path: Path within the repository to analyze
        confluence_space_key: Confluence space key
        parent_page_id: Confluence parent page ID
        
    Returns:
        The final state of the workflow
    """
    # Use default values if not provided
    if confluence_space_key is None:
        confluence_space_key = get_confluence_space_key()
    if parent_page_id is None:
        parent_page_id = os.getenv("PARENT_PAGE_ID", "")
    
    # Initialize state
    state = WorkflowState({
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "repo_path": repo_path,
        "files": [],
        "current_file_index": 0,
        "confluence_space_key": confluence_space_key,
        "parent_page_id": parent_page_id,
        "completed": False,
        "error": ""
    })
    
    # Step 1: Fetch files
    print(f"Fetching files from repository: {repo_owner}/{repo_name}, path: {repo_path}")
    files_data = fetch_repo_files(repo_owner, repo_name, repo_path)
    
    if not files_data:
        state["error"] = "Failed to fetch files from GitHub"
        state["completed"] = True
        return state
    
    # Filter only for code files
    code_extensions = ['.py', '.js', '.ts', '.java', '.c', '.cpp', '.cs', '.go', '.rb', '.php']
    files = []
    
    for file in files_data:
        if file["type"] == "file" and any(file["name"].endswith(ext) for ext in code_extensions):
            files.append(FileInfo({
                "name": file["name"],
                "path": file["path"],
                "download_url": file["download_url"],
                "content": "",
                "documentation": ""
            }))
    
    state["files"] = files
    
    # Step 2: Analyze code
    print(f"Analyzing {len(files)} files...")
    for i, file in enumerate(files):
        # Simulate processing time
        time.sleep(0.5)
        
        print(f"Analyzing file {i+1}/{len(files)}: {file['name']}")
        
        # Get file content
        content = get_file_content(file["download_url"])
        state["files"][i]["content"] = content
        
        # Generate documentation
        documentation = analyze_code(content, file["name"])
        state["files"][i]["documentation"] = documentation
        
        # Update state
        state["current_file_index"] = i + 1
    
    # Step 3: Analyze repository structure
    print("Analyzing repository structure...")
    repo_structure_doc = analyze_repository_structure(files)
    
    # Step 4: Generate README
    print("Generating README...")
    readme_doc = generate_readme(repo_name, files)
    
    # Step 5: Update Confluence
    print("Updating Confluence pages...")
    
    # Update individual file pages
    for file in state["files"]:
        title = f"Documentation: {file['name']}"
        content = file["documentation"]
        
        success = create_or_update_confluence_page(
            space_key=confluence_space_key,
            title=title,
            content=content,
            parent_id=parent_page_id
        )
        
        if not success:
            print(f"Failed to update Confluence page for {file['name']}")
    
    # Update repository structure page
    create_or_update_confluence_page(
        space_key=confluence_space_key,
        title=f"Repository Structure: {repo_name}",
        content=repo_structure_doc,
        parent_id=parent_page_id
    )
    
    # Update README page
    create_or_update_confluence_page(
        space_key=confluence_space_key,
        title=f"README: {repo_name}",
        content=readme_doc,
        parent_id=parent_page_id
    )
    
    # Mark workflow as completed
    state["completed"] = True
    
    return state