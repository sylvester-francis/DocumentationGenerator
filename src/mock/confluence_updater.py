import os
from typing import Dict, Any, Optional

# Store mock pages in memory
MOCK_PAGES = {}

def get_confluence_client():
    """Mock implementation of get_confluence_client"""
    return "MOCK_CONFLUENCE_CLIENT"

def create_or_update_confluence_page(
    space_key: str,
    title: str,
    content: str,
    parent_id: Optional[str] = None
) -> bool:
    """Mock implementation of create_or_update_confluence_page"""
    # Check if the page exists in our mock storage
    if title in MOCK_PAGES:
        # Update existing page
        MOCK_PAGES[title]["content"] = content
        MOCK_PAGES[title]["version"] += 1
        print(f"MOCK: Updated page: {title} (ID: {MOCK_PAGES[title]['id']})")
    else:
        # Create new page
        page_id = f"mock-page-{len(MOCK_PAGES) + 1}"
        MOCK_PAGES[title] = {
            "id": page_id,
            "title": title,
            "content": content,
            "space_key": space_key,
            "parent_id": parent_id,
            "version": 1
        }
        print(f"MOCK: Created page: {title} (ID: {page_id})")
    
    return True

def get_confluence_space_key() -> str:
    """Mock implementation of get_confluence_space_key"""
    return os.getenv("CONFLUENCE_SPACE_KEY", "MOCK")

def get_mock_pages() -> Dict[str, Dict[str, Any]]:
    """Get all mock pages created during testing"""
    return MOCK_PAGES