import os
import sys
from dotenv import load_dotenv

# Load mock environment
load_dotenv(".env.mock")

# Import the test workflow
from src.workflow_test import run_documentation_workflow_test

def main():
    """Run a test of the documentation workflow"""
    print("=== Testing Documentation Generator ===")
    print("Running in mock mode...")
    
    # Test repository information
    repo_owner = "test-owner"
    repo_name = "test-repo"
    repo_path = ""  # Root path
    
    # Run the workflow
    result = run_documentation_workflow_test(
        repo_owner=repo_owner,
        repo_name=repo_name,
        repo_path=repo_path
    )
    
    # Print results
    print("\n=== Workflow Results ===")
    print(f"Completed: {result['completed']}")
    
    if result.get("error"):
        print(f"Error: {result['error']}")
    else:
        print(f"Files processed: {len(result['files'])}")
        
        print("\nDocumented files:")
        for file in result["files"]:
            print(f"- {file['name']}")
        
        # In a real test, you might want to assert that certain things happened
        # Here we just log what would typically be tested
        print("\nChecks that would be performed in a real test:")
        print("1. Correct number of files were processed")
        print("2. Documentation was generated for each file")
        print("3. Confluence pages were created/updated")
        print("4. Repository structure documentation was created")
        print("5. README was generated")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()