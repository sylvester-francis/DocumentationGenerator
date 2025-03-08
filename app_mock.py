import streamlit as st
import os
from dotenv import load_dotenv
import time

# Load mock environment
load_dotenv(".env.mock")
os.environ["MOCK_MODE"] = "True"

# Import the test workflow
from src.workflow_test import run_documentation_workflow_test
from src.mock.confluence_updater import get_mock_pages

# Page configuration
st.set_page_config(
    page_title="Documentation Generator (MOCK)",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add a mock mode indicator
st.markdown("""
<div style="background-color: #FFE082; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
    <strong>🧪 MOCK MODE ACTIVE</strong> - No real API calls will be made. This is a simulation for testing purposes.
</div>
""", unsafe_allow_html=True)

# Main header
st.title("Documentation Generator (MOCK)")
st.markdown("Automatically generate technical documentation from your code and update Confluence.")

# Sidebar with mock info
with st.sidebar:
    st.markdown("## Mock Mode Information")
    st.info("This is running in mock mode. No real API calls will be made.")
    
    st.markdown("### Mock Configuration")
    st.code("""
GITHUB_TOKEN=mock_github_token
CONFLUENCE_URL=https://mock-confluence.atlassian.net
CONFLUENCE_USER=mock_user@example.com
CONFLUENCE_API_TOKEN=mock_confluence_token
CONFLUENCE_SPACE_KEY=MOCK
PARENT_PAGE_ID=12345
OPENAI_API_KEY=mock_openai_key
    """)
    
    st.markdown("### Available Mock Repository")
    st.markdown("- Owner: `test-owner`")
    st.markdown("- Name: `test-repo`")
    
    if st.button("View Mock Data Structure"):
        st.json({
            "main": ["app.py", "requirements.txt", "src/", "README.md"],
            "src": ["main.py", "config.py", "utils.py"]
        })

# Repository information
st.markdown("## GitHub Repository")

col1, col2 = st.columns(2)
with col1:
    repo_owner = st.text_input("Repository Owner", value="test-owner")
with col2:
    repo_name = st.text_input("Repository Name", value="test-repo")

repo_path = st.text_input("Repository Path (Optional)", 
                          help="Path within the repository to analyze. Try 'src' to see subdirectory files.")

# Add tabs for different views
tab1, tab2, tab3 = st.tabs(["Generate Documentation", "Documentation Preview", "Mock Confluence"])

with tab1:
    if st.button("Generate Documentation", type="primary"):
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Update status
            status_text.text("Fetching code from GitHub (Mock)...")
            progress_bar.progress(10)
            time.sleep(1)
            
            # Step 2: Analyze code
            status_text.text("Analyzing code (Mock)...")
            progress_bar.progress(30)
            time.sleep(1.5)
            
            # Step 3: Generate documentation
            status_text.text("Generating documentation (Mock)...")
            progress_bar.progress(60)
            time.sleep(1)
            
            # Step 4: Update Confluence
            status_text.text("Updating Confluence (Mock)...")
            progress_bar.progress(90)
            time.sleep(1)
            
            # Run the workflow
            result = run_documentation_workflow_test(
                repo_owner=repo_owner,
                repo_name=repo_name,
                repo_path=repo_path
            )
            
            # Update progress
            progress_bar.progress(100)
            
            # Save result to session state for other tabs
            st.session_state.workflow_result = result
            st.session_state.completed = True
            
            # Show result
            status_text.empty()
            if result.get("error"):
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"Successfully documented {len(result['files'])} files!")
                st.balloons()
        
        except Exception as e:
            status_text.empty()
            st.error(f"Error: {str(e)}")
        
with tab2:
    if "completed" in st.session_state and st.session_state.completed:
        # Show file selection
        result = st.session_state.workflow_result
        files = result["files"]
        
        if files:
            selected_file = st.selectbox("Select a file to preview", options=[file["name"] for file in files])
            
            # Show documentation preview
            selected_file_data = next((file for file in files if file["name"] == selected_file), None)
            if selected_file_data and selected_file_data.get("documentation"):
                st.markdown("### Documentation Preview")
                st.markdown(selected_file_data["documentation"])
            else:
                st.info("No documentation available for this file.")
        else:
            st.info("No files were processed.")
    else:
        st.info("Generate documentation first to see the preview.")

with tab3:
    st.markdown("### Mock Confluence Pages")
    
    if "completed" in st.session_state and st.session_state.completed:
        # Get mock pages from the Confluence updater
        mock_pages = get_mock_pages()
        
        if mock_pages:
            # Create expandable sections for each page
            for title, page in mock_pages.items():
                with st.expander(f"{title} (ID: {page['id']}, Version: {page['version']})"):
                    st.markdown(page["content"])
        else:
            st.info("No pages have been created in mock Confluence yet.")
    else:
        st.info("Generate documentation first to see mock Confluence pages.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit, LangGraph, and OpenAI (Mock Mode)")