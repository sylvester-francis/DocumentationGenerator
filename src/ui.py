import streamlit as st
from github_fetcher import fetch_repo_files
from code_analyzer import analyze_code
# from confluence_updater import create_or_update_confluence_page
import requests

st.title("Documentation Generator")

repo_path = st.text_input("GitHub Repository Path:")
if st.button("Fetch & Analyze"):
    files = fetch_repo_files(repo_path)
    if files:
        for file in files:
            if file["type"] == "file":
                file_content = requests.get(file["download_url"]).text
                doc = analyze_code(file_content)
                st.text_area(f"Documentation for {file['name']}", doc, height=200)
                create_or_update_confluence_page(file["name"], doc)
                st.success(f"Documentation for {file['name']} updated in Confluence!")
