from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pathlib import Path
import os
# File tools (assumed to be defined in 'tools.py')
from tools import read_file, list_files, rename_file

# Define base directory
base_dir = Path("test")

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Initialize AI model and agent
gemini_model = GeminiModel("gemini-2.5-flash-preview-04-17")
agent = Agent(
    model=gemini_model,
    system_prompt=(
        "You are an experienced programmer managing files in a test directory. "
        "Use tools to list, read, or rename files. Handle errors gracefully."
    ),
    tools=[read_file, list_files, rename_file]
)

file_cache = {}  # Cache for file contents

def update_cache_on_read(user_input: str):
    """Check if a file should be cached after reading."""
    for file_name in list_files():
        if file_name in user_input:
            content = read_file(file_name)
            file_cache[file_name] = content
            print(f"(cache_hit {file_name})")
            print(f"Cached content for '{file_name}':\n{content}")
            return content
    return None

def main():
    print("AI File Management Agent - Enter commands to manage files.")
    print("Available commands: list files, read <file>, rename <old> to <new>, exit")

    while True:
        user_input = input("\nEnter command (or 'exit'): ").strip()
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        # Auto-cache file content if it's a read-related query
        if any(kw in user_input.lower() for kw in ["read", "content"]):
            cached = False
            for name in file_cache:
                if name in user_input:
                    print(f"AI Response (cached): {file_cache[name]}")
                    cached = True
                    break
            if not cached:
                response = agent.run_sync(user_input)
                print("AI Response:", response.data)
                update_cache_on_read(user_input)

        # Handle other commands like rename or list
        else:
            response = agent.run_sync(user_input)
            print("AI Response:", response.data)

            # If rename, update cache
            if "rename" in user_input.lower():
                old_name = next((name for name in file_cache if name in user_input), None)
                if old_name:
                    del file_cache[old_name]
                    print(f"(cache_removed {old_name})")

if __name__ == "__main__":
    main()
    
    
