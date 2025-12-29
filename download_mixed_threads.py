#!/usr/bin/env python3
"""
Download specific Telegram messages from different threads
Thread 31: messages 62, 92
Thread 10: messages 80, 90, 91
"""

import subprocess
import sys
from pathlib import Path

def main():
    # Base URL for the chat
    base_url = "https://t.me/c/3399205162"
    
    # Specific message links from different threads
    links = [
        f"{base_url}/31/62",
        f"{base_url}/31/92",
        f"{base_url}/10/80",
        f"{base_url}/10/90",
        f"{base_url}/10/91",
    ]
    
    # Output folder
    output_folder = Path("mixed_threads_messages")
    output_folder.mkdir(exist_ok=True)
    
    print(f"Downloading media from messages across different threads")
    print(f"Total messages: {len(links)}")
    print(f"Output folder: {output_folder.absolute()}")
    print("\nMessages to download:")
    for link in links:
        print(f"  - {link}")
    
    # Use the tdl_downloader.py script
    cmd = [
        sys.executable,
        "tdl_downloader.py",
        "--out", str(output_folder.absolute())
    ]
    
    # Add all links
    for link in links:
        cmd.extend(["--link", link])
    
    print(f"\nStarting download...\n")
    
    # Run the download
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"\n✓ Download completed successfully!")
        print(f"Files saved to: {output_folder.absolute()}")
    else:
        print(f"\n✗ Download failed with exit code: {result.returncode}", file=sys.stderr)
        print(f"Some files may have been downloaded. Check the folder.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
