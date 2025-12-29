# Video Upload Setup Guide

## Why This Script?

The `tdl` tool uploads videos as **files** (downloadable). This Python script uploads videos as **streaming videos** (plays inline like in your screenshot), which makes it harder for users to download.

## Setup Steps

### 1. Get Telegram API Credentials

1. Go to https://my.telegram.org/apps
2. Login with your phone number
3. Click "API development tools"
4. Create a new application:
   - App title: "Video Uploader"
   - Short name: "uploader"
   - Platform: Desktop
5. Copy your **API ID** and **API hash**

### 2. Install Python Package

```powershell
pip install telethon
```

### 3. Configure the Script

Edit `upload_video.py` and replace:
```python
API_ID = 'YOUR_API_ID'      # Replace with your API ID (number)
API_HASH = 'YOUR_API_HASH'  # Replace with your API hash (string)
```

### 4. First Run (Authentication)

The first time you run the script, it will ask for your phone number and verification code:

```powershell
python upload_video.py "E:\telegram\downloads\video.mp4" 3305131927
```

Enter your phone number and the code Telegram sends you.

## Usage

### Upload Single Video

```powershell
python upload_video.py "E:\telegram\downloads\EM - Lecture 1.mp4" 3305131927
```

### Upload All Videos from Folder

```powershell
python upload_video.py "E:\telegram\downloads" 3305131927 --folder
```

## Chat IDs

- **CE made easy**: 3305131927
- **Prime batch private**: 3399205162
- **MIT-J**: 4880826523

## Important Notes

⚠️ **This does NOT fully prevent downloads!** Users can still:
- Screen record
- Use tools like `tdl` to download
- Take screenshots

✅ **But it makes it harder** because:
- Video plays inline (no download button)
- Must enable "Restrict Saving Content" in group settings
- Combine with watermarking for better protection

## Enable Group Protection

1. Open CE made easy group in Telegram
2. Click group name → Edit
3. Enable **"Restrict Saving Content"**
4. This prevents forwarding and official download buttons

## Next Steps: Watermarking

For better protection, add watermarks with FFmpeg before uploading.
