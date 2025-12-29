tdl — Telegram Downloader (quick setup)

This short guide shows how to install `tdl` (Windows) and download private Telegram media (videos) you have access to.

Prerequisites
- A Telegram account that has access to the private chat/group containing the videos.
- Windows PowerShell (you're using pwsh.exe).

Quick steps
1. Download the `tdl` Windows release from the project's releases page:
   https://github.com/iyear/tdl/releases/latest
   Choose the matching `tdl_Windows_64bit.zip` (or 32bit/arm if needed) and save it.

2. Unzip the archive and put `tdl.exe` somewhere convenient (or use the included script).

3. Login (interactive):
   - Run: `tdl login -T code` (enter your phone and code when prompted) — this creates an authenticated session.
   - Or import Telegram Desktop session: `tdl login -T desktop -d "C:\Path\To\Telegram\tdata"`.

4. Download a message link (one or more):
   - Get message link from Telegram Desktop: Right-click message -> Copy Message Link (for private chats the link looks like `https://t.me/c/<chatid>/<messageid>`).
   - Run: `tdl download -u "https://t.me/c/123456789/2345" -d "C:\path\to\downloads"`
   - Useful flags:
     - `--group` to auto-detect albums and download grouped entries.
     - `--takeout` to use takeout sessions (lower floodwaits).
     - `-t` / `-l` global flags control threads / concurrent tasks.
     - `--desc` download newest first.

Notes & security
- Bots cannot access private chats. You must login with a Telegram user session (the `tdl login` command creates it).
- If your account has 2FA, you'll be prompted for the password during `tdl login`.
- Sessions are stored per-namespace under the default data dir; protect that data.
- For many files use `tdl download -f exported_file.json` to feed an official-client exported file (tdl supports that).

If you'd like, I can create a small PowerShell script that automates downloading the latest Windows binary, extracts it, runs `tdl login` (interactive), then downloads a link you provide. Let me know if you want that and whether to place it in this workspace (I can create it for you).

Python wrapper (non-interactive)
--------------------------------
I added a small Python helper `tdl_downloader.py` in the workspace root. It wraps the `tdl.exe` binary and lets you:

- Provide one or more message links with `--link` (repeatable) or a file of links with `--file`.
- Set output directory with `--out` (defaults to `./downloads`).
- Optional flags: `--group`, `--takeout`, `--desc`.
- `--login` will run interactive `tdl login -T code` before downloading.
- `--check` runs `tdl version` to ensure `tdl.exe` is available.

Example:

```
python tdl_downloader.py --link "https://t.me/c/123456789/2345" --out "e:\\telegram\\downloads" --group
```

The script tries to locate `tdl.exe` in these places (in order): `TDL_PATH` env var, `./tdl/bin/tdl.exe` inside this workspace, `./bin/tdl.exe`, or on your PATH.