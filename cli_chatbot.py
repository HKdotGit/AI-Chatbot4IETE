import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from data_manager import DataManager

# Load environment variables
load_dotenv()

# Colors for terminal styling
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Fallback API key to run out-of-the-box
DEFAULT_API_KEY = "AIzaSyCEIeNfyQFj_wG0tiXf7wNXx-wX5sDs1qo"
API_KEY = os.environ.get("GEMINI_API_KEY", DEFAULT_API_KEY)

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load dynamic database content
data_manager = DataManager()
SYSTEM_INSTRUCTION = data_manager.generate_system_instruction()

def main():
    # Setup model
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        chat = model.start_chat(history=[])
    except Exception as e:
        print(f"{Colors.RED}Failed to initialize Gemini Client: {e}{Colors.END}")
        sys.exit(1)

    print("\n" + "="*60)
    print(f" {Colors.HEADER}{Colors.BOLD}IETE-SF AI CHATBOT - TERMINAL INTERFACE{Colors.END}")
    print(f" Powered by Gemini 2.0 Flash")
    print(f" Motto: {Colors.CYAN}'For the Engineers, By the Engineers.'{Colors.END}")
    print("="*60)
    print(f" Type {Colors.RED}'exit'{Colors.END} or {Colors.RED}'quit'{Colors.END} to end the chat.")
    print(f" Type {Colors.YELLOW}'clear'{Colors.END} to reset history.")
    print("="*60 + "\n")

    print(f"{Colors.BLUE}IETE-SF AI:{Colors.END} Hello, Engineer! 👋 How can I help you today?")

    while True:
        try:
            user_input = input(f"\n{Colors.GREEN}You:{Colors.END} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.BLUE}IETE-SF AI:{Colors.END} Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ['exit', 'quit']:
            print(f"{Colors.BLUE}IETE-SF AI:{Colors.END} Goodbye!")
            break

        if user_input.lower() == 'clear':
            chat = model.start_chat(history=[])
            print(f"\n{Colors.BLUE}System:{Colors.END} Chat history has been cleared.")
            print(f"{Colors.BLUE}IETE-SF AI:{Colors.END} Hello again! How can I help you?")
            continue

        # Show thinking indicator
        print(f"{Colors.CYAN}Thinking...{Colors.END}", end="\r")

        try:
            response = chat.send_message(user_input)
            # Clear thinking line
            sys.stdout.write("\033[K")
            print(f"{Colors.BLUE}IETE-SF AI:{Colors.END} {response.text}")
        except Exception as e:
            # Clear thinking line
            sys.stdout.write("\033[K")
            print(f"{Colors.RED}Error:{Colors.END} Could not fetch response. Details: {e}")

if __name__ == "__main__":
    main()
