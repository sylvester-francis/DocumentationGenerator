import streamlit as st
import os
from dotenv import load_dotenv
import time
from typing import Dict, List, Any

# Import our workflow
from src.workflow import run_documentation_workflow
from src.confluence_updater import get_confluence_space_key

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Documentation Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## Configuration")
    
    # GitHub Configuration
    st.markdown("### GitHub Settings")
    github_token = st.text_input("GitHub Token", value=os.getenv("GITHUB_TOKEN", ""), type="password")
    
    # Confluence Configuration
    st.markdown("### Confluence Settings")
    confluence_url = st.text_input("Confluence URL", value=os.getenv("CONFLUENCE_URL", ""))
    confluence_user = st.text_input("Confluence User", value=os.getenv("CONFLUENCE_USER", ""))
    confluence_token = st.text_input("Confluence API Token", value=os.getenv("CONFLUENCE_API_TOKEN", ""), type="password")
    confluence_space = st.text_input("Confluence Space Key", value=get_confluence_space_key())
    parent_page_id = st.text_input("Parent Page ID", value=os.getenv("PARENT_PAGE_ID", ""))
    
    # Save configuration
    if st.button("Save Configuration"):
        # Update environment variables (this will only be for the current session)
        os.environ["GITHUB_TOKEN"] = github_token
        os.environ["CONFLUENCE_URL"] = confluence_url
        os.environ["CONFLUENCE_USER"] = confluence_user
        os.environ["CONFLUENCE_API_TOKEN"] = confluence_token
        os.environ["CONFLUENCE_SPACE_KEY"] = confluence_space
        os.environ["PARENT_PAGE_ID"] = parent_page_id
        
        st.success("Configuration saved for this session!")
        st.info("To permanently save this configuration, update your .env file.")

# Main content
st.markdown('<h1 class="main-header">Documentation Generator</h1>', unsafe_allow_html=True)
st.markdown("Automatically generate technical documentation from your code and update Confluence.")

# Repository information
st.markdown('<h2 class="subheader">GitHub Repository</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    repo_owner = st.text_input("Repository Owner", help="The GitHub username or organization name.")
with col2:
    repo_name = st.text_input("Repository Name", help="The name of the repository.")

repo_path = st.text_input("Repository Path (Optional)", help="Path within the repository to analyze. Leave empty to analyze the entire repository.")

# Documentation settings
st.markdown('<h2 class="subheader">Documentation Settings</h2>', unsafe_allow_html=True)

# Add more settings if needed
include_readme = st.checkbox("Include README in documentation", value=True)
analyze_directories = st.checkbox("Analyze directory structure", value=True)

# Preview tab
tab1, tab2 = st.tabs(["Generate Documentation", "Documentation Preview"])

with tab1:
    if st.button("Generate Documentation", type="primary", disabled=not (repo_owner and repo_name)):
        if not os.getenv("GITHUB_TOKEN"):
            st.error("GitHub token is missing. Please configure it in the sidebar.")
        elif not (os.getenv("CONFLUENCE_URL") and os.getenv("CONFLUENCE_USER") and os.getenv("CONFLUENCE_API_TOKEN")):
            st.error("Confluence credentials are missing. Please configure them in the sidebar.")
        elif not os.getenv("PARENT_PAGE_ID"):
            st.error("Confluence parent page ID is missing. Please configure it in the sidebar.")
        else:
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Update status
                status_text.text("Fetching code from GitHub...")
                progress_bar.progress(10)
                
                # Run the workflow
                result = run_documentation_workflow(
                    repo_owner=repo_owner,
                    repo_name=repo_name,
                    repo_path=repo_path,
                    confluence_space_key=os.getenv("CONFLUENCE_SPACE_KEY", "DEV"),
                    parent_page_id=os.getenv("PARENT_PAGE_ID", "")
                )
                
                # Update progress
                progress_bar.progress(100)
                
                # Check result
                if result.get("error"):
                    st.error(f"Error: {result['error']}")
                else:
                    file_count = len(result.get("files", []))
                    st.markdown(f'<div class="status-box success-box">Successfully documented {file_count} files and updated Confluence!</div>', unsafe_allow_html=True)
                    
                    # Store files in session state for preview
                    st.session_state.files = result.get("files", [])
                    
                    # Show link to Confluence
                    if os.getenv("CONFLUENCE_URL") and os.getenv("PARENT_PAGE_ID"):
                        confluence_link = f"{os.getenv('CONFLUENCE_URL')}/pages/viewpage.action?pageId={os.getenv('PARENT_PAGE_ID')}"
                        st.markdown(f"[View documentation in Confluence]({confluence_link})")
            
            except Exception as e:
                st.markdown(f'<div class="status-box error-box">Error: {str(e)}</div>', unsafe_allow_html=True)
            
            finally:
                # Clean up
                status_text.empty()

with tab2:
    if "files" in st.session_state and st.session_state.files:
        # Show file selection
        files = st.session_state.files
        selected_file = st.selectbox("Select a file to preview", options=[file["name"] for file in files])
        
        # Show documentation preview
        selected_file_data = next((file for file in files if file["name"] == selected_file), None)
        if selected_file_data and selected_file_data.get("documentation"):
            st.markdown("## Documentation Preview")
            st.markdown(selected_file_data["documentation"])
        else:
            st.info("No documentation available for this file.")
    else:
        st.info("Generate documentation first to see the preview.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit, LangGraph, and OpenAI")