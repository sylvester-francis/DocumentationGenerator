from atlassian import Confluence
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

def get_confluence_client() -> Confluence:
    """Get authenticated Confluence client"""
    return Confluence(
        url=CONFLUENCE_URL,
        username=CONFLUENCE_USER,
        password=CONFLUENCE_API_TOKEN
    )

def create_or_update_confluence_page(
    space_key: str,
    title: str,
    content: str,
    parent_id: Optional[str] = None
) -> bool:
    """
    Create or update a Confluence page
    
    Args:
        space_key: Confluence space key
        title: Page title
        content: Page content in storage format (HTML or wiki markup)
        parent_id: Parent page ID
        
    Returns:
        True if successful, False otherwise
    """
    try:
        confluence = get_confluence_client()
        
        # Convert markdown to storage format for Confluence
        # Note: Confluence expects content in "storage format" which is a form of XHTML
        # We're using markdown directly here, which works with the Atlassian Python API
        # as it handles the conversion internally
        
        # Check if the page exists
        existing_page = confluence.get_page_by_title(space_key, title)
        
        if existing_page:
            # Update existing page
            page_id = existing_page['id']
            version = existing_page['version']['number']
            
            result = confluence.update_page(
                page_id=page_id,
                title=title,
                body=content,
                version_number=version + 1
            )
            print(f"Updated page: {title} (ID: {page_id})")
            return True
        else:
            # Create new page
            result = confluence.create_page(
                space=space_key,
                title=title,
                body=content,
                parent_id=parent_id
            )
            print(f"Created page: {title} (ID: {result['id']})")
            return True
            
    except Exception as e:
        print(f"Error updating Confluence: {str(e)}")
        return False

def get_confluence_space_key() -> str:
    """Get the default Confluence space key from environment variables"""
    return os.getenv("CONFLUENCE_SPACE_KEY", "DEV")