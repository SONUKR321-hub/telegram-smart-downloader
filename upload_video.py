"""
Telegram Video Uploader
Uploads videos as streaming video (not as file) to prevent easy downloads
"""
import asyncio
import os
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo

# Import configuration
try:
    from config import API_ID, API_HASH, CE_MADE_EASY_CHAT_ID
    SESSION_NAME = 'video_uploader'
except ImportError:
    print("❌ ERROR: config.py not found!")
    print("Please create config.py with your API credentials")
    print("See UPLOAD_SETUP.md for instructions")
    exit(1)

if not API_ID or not API_HASH:
    print("❌ ERROR: API_ID and API_HASH not configured!")
    print("Edit config.py and add your credentials from https://my.telegram.org/apps")
    exit(1)

def progress_callback(current, total):
    """Display upload progress"""
    import time
    if not hasattr(progress_callback, 'start_time'):
        progress_callback.start_time = time.time()
        progress_callback.last_update = 0
    
    # Update every 0.5 seconds to avoid spam
    current_time = time.time()
    if current_time - progress_callback.last_update < 0.5 and current < total:
        return
    
    progress_callback.last_update = current_time
    percentage = (current / total) * 100
    current_mb = current / (1024 * 1024)
    total_mb = total / (1024 * 1024)
    elapsed = current_time - progress_callback.start_time
    speed_mbps = current_mb / elapsed if elapsed > 0 else 0
    
    print(f"\r🚀 Progress: {percentage:.1f}% | {current_mb:.1f}/{total_mb:.1f} MB | Speed: {speed_mbps:.2f} MB/s", end='', flush=True)

async def upload_video(video_path, chat_id, caption=''):
    """
    Upload a video file as streaming video to a Telegram chat
    
    Args:
        video_path: Path to the video file
        chat_id: Chat ID or username
        caption: Optional caption for the video
    """
    import time
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        filename = os.path.basename(video_path)
        file_size = os.path.getsize(video_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # Use filename as caption if no caption provided
        if not caption:
            caption = filename
        
        print(f"\n{'='*60}")
        print(f"📹 Uploading: {filename}")
        print(f"📊 Size: {file_size_mb:.2f} MB")
        print(f"💬 Caption: {caption}")
        print(f"📤 To chat: {chat_id}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Reset progress callback state
        if hasattr(progress_callback, 'start_time'):
            delattr(progress_callback, 'start_time')
        if hasattr(progress_callback, 'last_update'):
            delattr(progress_callback, 'last_update')
        
        # Upload as video (not as file)
        # supports_streaming=True makes it playable inline
        await client.send_file(
            chat_id,
            video_path,
            caption=caption,
            supports_streaming=True,  # This makes it a streaming video
            force_document=False,  # Don't force as document/file
            progress_callback=progress_callback,
            attributes=[
                DocumentAttributeVideo(
                    duration=0,  # Will be auto-detected
                    w=1920,  # Width (will be auto-detected)
                    h=1080,  # Height (will be auto-detected)
                    supports_streaming=True
                )
            ]
        )
        
        print()  # New line after progress
        end_time = time.time()
        upload_time = end_time - start_time
        upload_speed_mbps = file_size_mb / upload_time if upload_time > 0 else 0
        
        print(f"✅ Upload complete!")
        print(f"⏱️  Time: {upload_time:.2f} seconds")
        print(f"🚀 Speed: {upload_speed_mbps:.2f} MB/s")
        print(f"{'='*60}\n")

async def upload_folder(folder_path, chat_id):
    """Upload all videos from a folder"""
    import time
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv']
        
        # Get all video files and sort them by name for sequential upload
        video_files = []
        for filename in os.listdir(folder_path):
            if any(filename.lower().endswith(ext) for ext in video_extensions):
                video_path = os.path.join(folder_path, filename)
                video_files.append((filename, video_path))
        
        # Sort by filename to maintain sequence
        video_files.sort(key=lambda x: x[0])
        
        total_videos = len(video_files)
        print(f"\n🎬 Found {total_videos} videos to upload")
        print(f"📁 Folder: {folder_path}\n")
        
        for index, (filename, video_path) in enumerate(video_files, 1):
            file_size = os.path.getsize(video_path)
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"\n{'='*60}")
            print(f"📹 [{index}/{total_videos}] Uploading: {filename}")
            print(f"📊 Size: {file_size_mb:.2f} MB")
            print(f"{'='*60}")
            
            start_time = time.time()
            
            # Reset progress callback state
            if hasattr(progress_callback, 'start_time'):
                delattr(progress_callback, 'start_time')
            if hasattr(progress_callback, 'last_update'):
                delattr(progress_callback, 'last_update')
            
            await client.send_file(
                chat_id,
                video_path,
                caption=filename,  # Use filename as caption
                supports_streaming=True,
                force_document=False,
                progress_callback=progress_callback
            )
            
            print()  # New line after progress
            end_time = time.time()
            upload_time = end_time - start_time
            upload_speed_mbps = file_size_mb / upload_time if upload_time > 0 else 0
            
            print(f"✅ Upload complete!")
            print(f"⏱️  Time: {upload_time:.2f} seconds")
            print(f"🚀 Speed: {upload_speed_mbps:.2f} MB/s")
            print(f"{'='*60}\n")
        
        print(f"\n🎉 All {total_videos} videos uploaded successfully!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Single file: python upload_video.py <video_path> <chat_id>")
        print("  Folder:      python upload_video.py <folder_path> <chat_id> --folder")
        print("\nExample:")
        print('  python upload_video.py "E:\\telegram\\downloads\\video.mp4" 3305131927')
        print('  python upload_video.py "E:\\telegram\\downloads" 3305131927 --folder')
        sys.exit(1)
    
    path = sys.argv[1]
    chat = sys.argv[2]
    
    # Convert chat_id to integer if it's a number
    try:
        chat_id = int(chat)
    except ValueError:
        chat_id = chat  # Keep as username if not a number
    
    if len(sys.argv) > 3 and sys.argv[3] == '--folder':
        asyncio.run(upload_folder(path, chat_id))
    else:
        asyncio.run(upload_video(path, chat_id))
