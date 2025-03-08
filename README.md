# DocumentationGenerator
An AI-powered workflow automation system that fetches code from GitHub, analyzes its structure, generates technical documentation, and updates Confluence. Uses LangGraph for multi-agent orchestration, OpenAI for code analysis, and Streamlit for an interactive UI. Automates documentation and keeps it up to date effortlessly. 🚀
# **AI-Powered Code Documentation & Confluence Updater 🚀**  

## **Overview**  
This project automates the process of fetching code from a GitHub repository, analyzing its structure, generating technical documentation, and updating Confluence pages. It leverages **LangGraph**, **OpenAI LLMs**, and **Streamlit** to streamline workflow automation.  

## **Key Features**  
✅ Fetch source code dynamically from a GitHub repository 📂  
✅ Analyze code structure, functions, and purpose using AI 🤖  
✅ Generate detailed technical documentation 📜  
✅ Automatically update Confluence pages under a given parent page ID 🏢  
✅ Interactive **Streamlit UI** for ease of use 🎛️  

## **Tech Stack**  
- **LangGraph** - AI-powered multi-agent workflow automation  
- **OpenAI GPT-4** - Code analysis & documentation generation  
- **GitHub API** - Fetching repository contents  
- **Confluence API** - Updating documentation  
- **Streamlit** - Web UI for interaction  

## **Installation & Usage**  

### **1. Clone the Repository**  
```bash
git clone [https://github.com/yourusername/ai-code-docs.git](https://github.com/sylvester-francis/DocumentationGenerator)
cd DocumentationGenerator
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3. Set Up Environment Variables**  
Create a `.env` file and add:  
```ini
GITHUB_TOKEN=your_github_token
CONFLUENCE_URL=https://yourcompany.atlassian.net
CONFLUENCE_USER=your_email
CONFLUENCE_API_TOKEN=your_api_token
PARENT_PAGE_ID=your_confluence_parent_page_id
```

### **4. Run the Streamlit App**  
```bash
streamlit run app.py
```

## **How It Works**  
1. Enter the GitHub repository path in the UI.  
2. Click **"Fetch & Analyze"** to retrieve and analyze code.  
3. The AI generates documentation for each function and file.  
4. The documentation is automatically updated in Confluence.  
5. Review the output in Confluence or via the UI.  

## **Future Enhancements**  
🚀 Support for multiple programming languages  
🚀 Enhanced LLM prompt tuning for better documentation  
🚀 Asynchronous agent processing for improved efficiency  

### **Contributions Welcome!**  
Feel free to **fork**, **submit issues**, and **contribute** to this project!  
