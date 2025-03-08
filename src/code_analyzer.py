import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize ChatOpenAI with the API key
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY  # Pass the API key here
)

def analyze_code(code):
    messages = [
        HumanMessage(content=f"Analyze this code and document its structure:\n\n{code}")
    ]
    response = llm(messages)
    return response.content
