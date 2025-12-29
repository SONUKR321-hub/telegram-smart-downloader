import os
import subprocess
import sys
import re

# Configuration
TDL_PATH = r".\tdl\bin\tdl.exe"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def list_directories():
    """Returns a list of directories in the current folder."""
    try:
        items = os.listdir('.')
        dirs = [d for d in items if os.path.isdir(d) and not d.startswith('.')]
        return dirs
    except Exception:
        return []

def select_folder():
    """Handles the logic for selecting a new or existing folder."""
    print("\n--- Folder Selection ---")
    print("1. Create New Folder")
    print("2. Use Existing Folder")
    
    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == '1':
            while True:
                name = input("Enter New Folder Name: ").strip()
                if name:
                    return name
                print("Folder name cannot be empty.")
        
        elif choice == '2':
            dirs = list_directories()
            if not dirs:
                print("No existing folders found. Please create a new one.")
                continue
            
            print("\nAvailable Folders:")
            for i, d in enumerate(dirs, 1):
                print(f"{i}. {d}")
            
            while True:
                folder_input = input("Enter folder name or number: ").strip()
                
                # Check if user entered a number
                if folder_input.isdigit():
                    idx = int(folder_input) - 1
                    if 0 <= idx < len(dirs):
                        return dirs[idx]
                    else:
                        print("Invalid number.")
                # Check if user entered a valid folder name
                elif folder_input in dirs:
                    return folder_input
                else:
                    print("Folder not found. Try again or enter the number.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

def extract_chat_id(input_str):
    """Extracts chat ID from a URL or returns the input if it's just a number."""
    # Pattern to match https://t.me/c/1234567890/123 or just 1234567890
    match = re.search(r't\.me/c/(\d+)', input_str)
    if match:
        return match.group(1)
    
    # If pure number, return as is
    if input_str.isdigit():
        return input_str
        
    return input_str

def extract_message_id(input_str):
    """Extracts message ID from a URL or returns the input if it's just a number."""
    # Pattern to match https://t.me/c/1234567890/123 where 123 is the msg id
    match = re.search(r'/(\d+)(?:\?|$)', input_str)
    if match:
        # If it's a full URL like t.me/c/ID/MSG_ID, the last number is usually the MSG_ID
        parts = input_str.rstrip('/').split('/')
        if parts[-1].isdigit():
            return parts[-1]
            
    if input_str.isdigit():
        return input_str
        
    return input_str

def download_via_link():
    print("\n--- Download via Link ---")
    link = input("Enter Telegram Message Link: ").strip()
    if not link:
        print("Link cannot be empty.")
        return

    folder = select_folder()
    
    cmd = f'"{TDL_PATH}" dl -u {link} -d "{folder}"'
    print(f"\nRunning: {cmd}")
    run_command(cmd)
    input("\nPress Enter to return to menu...")

def download_via_range():
    print("\n--- Download via Range ---")
    print("Tip: You can paste the Chat ID or a full link like https://t.me/c/12345/100")
    
    chat_input = input("Enter Chat ID: ").strip()
    chat_id = extract_chat_id(chat_input)
    
    if not chat_id:
        print("Chat ID is required.")
        return

    start_input = input("Enter Start Message ID (or link): ").strip()
    start_id = extract_message_id(start_input)
    
    end_input = input("Enter End Message ID (or link): ").strip()
    end_id = extract_message_id(end_input)
    
    if not start_id or not end_id:
        print("Start and End IDs are required.")
        return
        
    print(f"Detected: ChatID={chat_id}, Range={start_id}-{end_id}")

    folder = select_folder()

    export_file = f"export_{chat_id}_{start_id}_{end_id}.json"
    
    print("\nStep 1: Exporting message list...")
    # Export command
    export_cmd = f'"{TDL_PATH}" chat export -c {chat_id} -T id -i {start_id},{end_id} -o "{export_file}"'
    if run_command(export_cmd):
        print("\nStep 2: Downloading files...")
        # Download command
        dl_cmd = f'"{TDL_PATH}" dl -f "{export_file}" -d "{folder}"'
        run_command(dl_cmd)
        
        # Cleanup (Optional: keep export file or delete)
        if os.path.exists(export_file):
            try:
                os.remove(export_file)
            except:
                pass
    
    input("\nPress Enter to return to menu...")

def main():
    global TDL_PATH
    # Ensure TDL path is correct
    if not os.path.exists(TDL_PATH):
        # Fallback check for absolute path
        if os.path.exists(r"e:\telegram\tdl\bin\tdl.exe"):
             TDL_PATH = r"e:\telegram\tdl\bin\tdl.exe"
        else:
            print(f"Warning: tdl.exe not found at {TDL_PATH}")

    while True:
        clear_screen()
        print("=========================================")
        print("       TELEGRAM DOWNLOADER APP          ")
        print("=========================================")
        print("1. Download Individually (via Link)")
        print("2. Download Range (ChatID + Start/End)")
        print("3. Exit")
        print("=========================================")
        
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            download_via_link()
        elif choice == '2':
            download_via_range()
        elif choice == '3':
            print("Exiting... Goodbye!")
            sys.exit(0)
        else:
            input("Invalid choice. Press Enter to try again...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
