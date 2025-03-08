import os
from typing import Dict, List, Any, Annotated, TypedDict
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import requests
from pydantic import BaseModel, Field

# Import our modules
from github_fetcher import fetch_repo_files, get_file_content
from confluence_updater import create_or_update_confluence_page

# Load environment variables
load_dotenv()

# Define our state
class FileInfo(TypedDict):
    name: str
    path: str
    download_url: str
    content: str
    documentation: str
    
class WorkflowState(TypedDict):
    repo_owner: str
    repo_name: str
    repo_path: str
    files: List[FileInfo]
    current_file_index: int
    confluence_space_key: str
    parent_page_id: str
    completed: bool
    error: str

# Initialize our LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define our nodes (agents)

def github_fetcher(state: WorkflowState) -> WorkflowState:
    """Fetch files from GitHub repository"""
    try:
        repo_owner = state["repo_owner"]
        repo_name = state["repo_name"]
        repo_path = state.get("repo_path", "")
        
        files_data = fetch_repo_files(repo_owner, repo_name, repo_path)
        
        if not files_data:
            return {**state, "error": "Failed to fetch files from GitHub", "completed": True}
        
        # Filter only for code files
        code_extensions = ['.py', '.js', '.ts', '.java', '.c', '.cpp', '.cs', '.go', '.rb', '.php']
        files = []
        
        for file in files_data:
            if file["type"] == "file" and any(file["name"].endswith(ext) for ext in code_extensions):
                files.append({
                    "name": file["name"],
                    "path": file["path"],
                    "download_url": file["download_url"],
                    "content": "",
                    "documentation": ""
                })
        
        return {**state, "files": files, "current_file_index": 0}
    except Exception as e:
        return {**state, "error": f"Error in GitHub fetcher: {str(e)}", "completed": True}

def code_analyzer(state: WorkflowState) -> WorkflowState:
    """Analyze code and generate documentation"""
    try:
        if not state["files"]:
            return {**state, "completed": True}
        
        current_idx = state["current_file_index"]
        if current_idx >= len(state["files"]):
            return {**state, "completed": True}
        
        current_file = state["files"][current_idx]
        
        # Get file content if not already fetched
        if not current_file["content"]:
            content = get_file_content(current_file["download_url"])
            state["files"][current_idx]["content"] = content
        else:
            content = current_file["content"]
        
        # Define our prompt for code analysis
        messages = [
            SystemMessage(content="""You are a technical documentation expert specializing in code analysis.
            Analyze the provided code and create comprehensive documentation that includes:
            1. A high-level overview of what the file does
            2. A detailed breakdown of each function/class/component
            3. Parameters, return values, and their types
            4. Dependencies and their purposes
            5. Any important implementation details or design patterns
            
            Format the documentation in Markdown with appropriate headings, code blocks, and sections.
            """),
            HumanMessage(content=f"File: {current_file['name']}\n\nCode:\n```\n{content}\n```\n\nPlease generate comprehensive technical documentation for this file.")
        ]
        
        # Get documentation from LLM
        response = llm(messages)
        documentation = response.content
        
        # Update the state with documentation
        state["files"][current_idx]["documentation"] = documentation
        
        # Move to the next file
        return {**state, "current_file_index": current_idx + 1}
    except Exception as e:
        return {**state, "error": f"Error in code analyzer: {str(e)}", "completed": True}

def confluence_updater(state: WorkflowState) -> WorkflowState:
    """Update documentation in Confluence"""
    try:
        if state.get("error"):
            return {**state, "completed": True}
        
        space_key = state["confluence_space_key"]
        parent_id = state["parent_page_id"]
        
        for file in state["files"]:
            if file["documentation"]:
                title = f"Documentation: {file['name']}"
                content = file["documentation"]
                create_or_update_confluence_page(space_key, title, content, parent_id)
        
        return {**state, "completed": True}
    except Exception as e:
        return {**state, "error": f"Error updating Confluence: {str(e)}", "completed": True}

# Define our routing logic
def should_continue(state: WorkflowState) -> str:
    """Determine the next step in the workflow"""
    if state.get("error") or state.get("completed"):
        return "end"
    
    current_idx = state["current_file_index"]
    if current_idx >= len(state["files"]):
        return "confluence_updater"
    
    return "code_analyzer"

# Create our workflow graph
def create_workflow() -> StateGraph:
    """Create and return the workflow graph"""
    workflow = StateGraph(WorkflowState)
    
    # Add our nodes
    workflow.add_node("github_fetcher", github_fetcher)
    workflow.add_node("code_analyzer", code_analyzer)
    workflow.add_node("confluence_updater", confluence_updater)
    
    # Add our edges
    workflow.add_edge("github_fetcher", "code_analyzer")
    workflow.set_conditional_edge("code_analyzer", should_continue)
    workflow.add_edge("confluence_updater", END)
    
    # Set the entry point
    workflow.set_entry_point("github_fetcher")
    
    return workflow

# Function to run the workflow
def run_documentation_workflow(
    repo_owner: str,
    repo_name: str,
    repo_path: str = "",
    confluence_space_key: str = "DEV",
    parent_page_id: str = os.getenv("PARENT_PAGE_ID", "")
) -> Dict[str, Any]:
    """
    Run the documentation workflow
    
    Args:
        repo_owner: GitHub repository owner
        repo_name: GitHub repository name
        repo_path: Path within the repository to analyze
        confluence_space_key: Confluence space key
        parent_page_id: Confluence parent page ID
        
    Returns:
        The final state of the workflow
    """
    # Create the workflow
    workflow = create_workflow()
    
    # Create the initial state
    initial_state: WorkflowState = {
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "repo_path": repo_path,
        "files": [],
        "current_file_index": 0,
        "confluence_space_key": confluence_space_key,
        "parent_page_id": parent_page_id,
        "completed": False,
        "error": ""
    }
    
    # Run the workflow
    result = workflow.invoke(initial_state)
    
    return result