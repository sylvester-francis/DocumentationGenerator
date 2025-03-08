from atlassian import Confluence
import os
from dotenv import load_dotenv

load_dotenv()

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
PARENT_PAGE_ID = os.getenv("PARENT_PAGE_ID")

confluence = Confluence(
    url=CONFLUENCE_URL,
    username=CONFLUENCE_USER,
    password=CONFLUENCE_API_TOKEN
)

def create_or_update_confluence_page(title, content):
    existing_page = confluence.get_page_by_title("Your Space Key", title)
    if existing_page:
        confluence.update_page(existing_page['id'], title, content, existing_page['version']['number'] + 1)
        print(f"Updated page: {title}")
    else:
        confluence.create_page("Your Space Key", title, content, parent_id=PARENT_PAGE_ID)
        print(f"Created page: {title}")
