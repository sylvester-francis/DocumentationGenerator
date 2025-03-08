import os
import sys
from dotenv import load_dotenv
from src.code_analyzer import analyze_code

# Load environment variables
load_dotenv()

def test_analyzer():
    """Test the code analyzer with a sample file"""
    
    # Check if a filename is provided as a command-line argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        
        try:
            # Read the file content
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Analyze the code
            documentation = analyze_code(code, os.path.basename(filename))
            
            # Print the documentation
            print("\n" + "="*50 + "\n")
            print(documentation)
            print("\n" + "="*50 + "\n")
            
            # Optionally save the documentation to a file
            output_filename = os.path.basename(filename) + '.md'
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(documentation)
            print(f"Documentation saved to {output_filename}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Usage: python test_analyzer.py <filename>")

if __name__ == "__main__":
    test_analyzer()