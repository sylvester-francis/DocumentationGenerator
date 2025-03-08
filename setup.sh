#!/bin/bash

# Setup script for the Documentation Generator

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Documentation Generator Setup ===${NC}"
echo ""

# Check if Python is installed
echo -e "${YELLOW}Checking for Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or later.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"

# Set up virtual environment
echo -e "${YELLOW}Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}Dependencies installed.${NC}"

# Check for .env file and create if it doesn't exist
echo -e "${YELLOW}Checking for .env file...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.sample .env
    echo -e "${GREEN}.env file created. Please edit it to add your API keys and credentials.${NC}"
    echo -e "${YELLOW}You need to set the following environment variables:${NC}"
    echo "GITHUB_TOKEN"
    echo "CONFLUENCE_URL"
    echo "CONFLUENCE_USER"
    echo "CONFLUENCE_API_TOKEN"
    echo "PARENT_PAGE_ID"
    echo "OPENAI_API_KEY"
else
    echo -e "${GREEN}.env file already exists.${NC}"
fi

echo ""
echo -e "${BLUE}=== Setup Complete ===${NC}"
echo -e "${GREEN}To run the application:${NC}"
echo "1. Make sure your virtual environment is activated: source venv/bin/activate"
echo "2. Run the Streamlit app: streamlit run app.py"
echo ""
echo -e "${YELLOW}Note: Make sure to update your .env file with the required API keys and credentials.${NC}"