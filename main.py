from dotenv import load_dotenv
from pydantic_ai.models.gemini import GeminiModel
import os

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")
# Initialize the Gemini model
gemini_model = GeminiModel("gemini-2.5-flash-preview-04-17")

from pydantic_ai import Agent
from tools import read_file, list_files, rename_file

# Create the agent with a descriptive system prompt
agent = Agent(
    model=gemini_model,
    system_prompt=(
        "You are an experienced programmer tasked with managing files in a test directory. "
        "You can list files, read their contents, and rename them using provided tools. "
        "Provide clear, concise responses and handle errors gracefully."
    ),
    tools=[read_file, list_files, rename_file]
)

file_cache = {}  # Cache to store file contents

def main():
    print("AI File Management Agent - Enter commands to manage files in the test directory.")
    print("Available commands: list files, read <file>, rename <old_name> to <new_name>, exit")
    
    while True:
        user_input = input("\nEnter your command (or 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            print("Exiting AI File Management Agent.")
            break

# Check cache for read/content queries
        if any(keyword in user_input.lower() for keyword in ["read", "content", "function"]):
            for file_name in file_cache:
                if file_name in user_input:
                    print(f"(cache_hit {file_name})")
                    print(f"AI Response: Cached content for '{file_name}':\n{file_cache[file_name]}")
                    break
            else:
                # If not in cache, proceed with agent
                response = agent.run_sync(user_input)
                print("AI Response:", response)
                # Update cache for read operations
                if "read_file" in str(response).lower():
                    for file_name in list_files():
                        if file_name in user_input:
                            content = read_file(file_name)
                            file_cache[file_name] = content
                            break
        else:
            # Handle non-read commands (e.g., list, rename)
            response = agent.run_sync(user_input)
            print("AI Response:", response)
            # Update cache for rename operations
            if "rename_file" in str(response).lower():
                for file_name in list_files():
                    if file_name in user_input:
                        # Remove old file from cache
                        old_name = next((n for n in file_cache if n in user_input), None)
                        if old_name:
                            del file_cache[old_name]
                        break
if __name__ == "__main__":
    main()
    
    