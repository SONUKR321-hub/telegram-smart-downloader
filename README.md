# 🚀 Telegram Smart Downloader

An ultra-fast, interactive Telegram downloader powered by [TDL](https://github.com/iyear/tdl).  
Easily download ranges of messages (PDFs, Videos, etc.) from private or public channels by simply pasting links.

## ✨ Features

- **Interactive Menu**: No need to remember complex commands.
- **Smart Link Detection**: Paste full Telegram links (e.g., `https://t.me/c/1234/100`), and it auto-extracts the ID.
- **Bulk Downloading**: Download hundreds of files (documents, media) in one go by specifying a range (e.g., Msg 400 to 700).
- **Organization**: Choose where to save your files or create new folders on the fly.
- **Resumable**: Downloads are handled by `tdl` for maximum speed and reliability.

---

## 🛠️ Installation

1.  **Clone this repository**:
    ```bash
    git clone https://github.com/SONUKR321-hub/telegram-smart-downloader.git
    cd telegram-smart-downloader
    ```

2.  **Ensure you have Python installed**.

3.  **Setup TDL**:
    - The repository includes a `tdl/bin/tdl.exe` (for Windows).
    - If you are on Linux/Mac, [download the TDL binary](https://github.com/iyear/tdl/releases) and place it in the folder or update the path in the script.

4.  **Login (First Time Only)**:
    Before using the script, you must login to your Telegram account via TDL. Run this in your terminal:
    ```powershell
    .\tdl\bin\tdl.exe login
    ```
    Follow the prompts to enter your phone number and OTP code.

---

## 🚀 How to Run

Simply run the interactive Python script:

```powershell
python interactive_tdl.py
```

### 📋 The Menu

Once started, you will see:

```text
=========================================
       TELEGRAM DOWNLOADER APP          
=========================================
1. Download Individually (via Link)
2. Download Range (ChatID + Start/End)
3. Exit
```

### 🔹 Option 1: Download Single File
- Paste the link to the file/message you want.
- Select a folder to save it in.

### 🔹 Option 2: Download Range (Best for courses/series)
- **Chat ID**: Paste the chat link (e.g., `https://t.me/c/2732989224/411` or just `2732989224`).
- **Start ID**: Paste the link of the *first* message (e.g., `.../411`).
- **End ID**: Paste the link of the *last* message (e.g., `.../702`).
- **Folder**: Create a new folder (e.g., "Physics Notes") or pick an existing one.

The app will handle the rest! 🚀

---

## 📂 Project Structure

- `interactive_tdl.py`: The main magic script. 🧙‍♂️
- `tdl/`: Contains the core downloader engine.
- `download_range.ps1`: (Optional) A quick PowerShell helper for advanced users.

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the tool!