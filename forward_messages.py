#!/usr/bin/env python3
"""
Telegram Message Forwarder
Forward messages from one group/chat to another
"""
import asyncio
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterEmpty

# Import configuration
try:
    from config import API_ID, API_HASH
    SESSION_NAME = 'video_uploader'  # Use existing authenticated session
except ImportError:
    print("❌ ERROR: config.py not found!")
    print("Please create config.py with your API credentials")
    exit(1)

if not API_ID or not API_HASH:
    print("❌ ERROR: API_ID and API_HASH not configured!")
    print("Edit config.py and add your credentials from https://my.telegram.org/apps")
    exit(1)

async def forward_messages(source_chat_id, dest_chat_id, start_msg_id, end_msg_id):
    """
    Forward messages from source chat to destination chat
    
    Args:
        source_chat_id: Source chat ID (can be negative for groups/channels)
        dest_chat_id: Destination chat ID
        start_msg_id: Starting message ID
        end_msg_id: Ending message ID
    """
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print(f"\n{'='*60}")
        print(f"📨 Forwarding Messages")
        print(f"{'='*60}")
        print(f"📤 From: {source_chat_id}")
        print(f"📥 To: {dest_chat_id}")
        print(f"📊 Message range: {start_msg_id} to {end_msg_id}")
        print(f"📝 Total messages: {end_msg_id - start_msg_id + 1}")
        print(f"{'='*60}\n")
        
        # Get the source and destination entities
        try:
            source_entity = await client.get_entity(source_chat_id)
            dest_entity = await client.get_entity(dest_chat_id)
            print(f"✅ Source chat verified: {getattr(source_entity, 'title', source_chat_id)}")
            print(f"✅ Destination chat verified: {getattr(dest_entity, 'title', dest_chat_id)}\n")
        except Exception as e:
            print(f"❌ Error getting chat entities: {e}")
            return
        
        # Forward messages
        successful = 0
        failed = 0
        skipped = 0
        
        for msg_id in range(start_msg_id, end_msg_id + 1):
            try:
                # Get the message
                message = await client.get_messages(source_entity, ids=msg_id)
                
                if message is None:
                    print(f"⊘ Message {msg_id}: Skipped (deleted or not found)")
                    skipped += 1
                    continue
                
                # Forward the message
                await client.forward_messages(
                    entity=dest_entity,
                    messages=msg_id,
                    from_peer=source_entity
                )
                
                print(f"✅ Message {msg_id}: Forwarded successfully")
                successful += 1
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Message {msg_id}: Failed - {str(e)[:50]}")
                failed += 1
                continue
        
        # Summary
        print(f"\n{'='*60}")
        print(f"📊 Forwarding Summary")
        print(f"{'='*60}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"⊘ Skipped: {skipped}")
        print(f"📝 Total: {successful + failed + skipped}")
        print(f"{'='*60}\n")

async def forward_messages_bulk(source_chat_id, dest_chat_id, start_msg_id, end_msg_id):
    """
    Forward messages in bulk (faster but less control)
    
    Args:
        source_chat_id: Source chat ID
        dest_chat_id: Destination chat ID
        start_msg_id: Starting message ID
        end_msg_id: Ending message ID
    """
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print(f"\n{'='*60}")
        print(f"📨 Bulk Forwarding Messages")
        print(f"{'='*60}")
        print(f"📤 From: {source_chat_id}")
        print(f"📥 To: {dest_chat_id}")
        print(f"📊 Message range: {start_msg_id} to {end_msg_id}")
        print(f"{'='*60}\n")
        
        try:
            source_entity = await client.get_entity(source_chat_id)
            dest_entity = await client.get_entity(dest_chat_id)
            
            # Create list of message IDs
            message_ids = list(range(start_msg_id, end_msg_id + 1))
            
            print(f"🚀 Forwarding {len(message_ids)} messages in bulk...")
            
            # Forward all messages at once
            await client.forward_messages(
                entity=dest_entity,
                messages=message_ids,
                from_peer=source_entity
            )
            
            print(f"✅ Bulk forward completed!")
            print(f"📝 Note: Some messages may have been skipped if deleted/empty\n")
            
        except Exception as e:
            print(f"❌ Error during bulk forward: {e}\n")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 5:
        print("Usage:")
        print("  Individual: python forward_messages.py <source_chat_id> <dest_chat_id> <start_msg_id> <end_msg_id>")
        print("  Bulk:       python forward_messages.py <source_chat_id> <dest_chat_id> <start_msg_id> <end_msg_id> --bulk")
        print("\nExample:")
        print('  python forward_messages.py -1003159701355 -1003305131927 51 56')
        print('  python forward_messages.py -1003159701355 -1003305131927 51 56 --bulk')
        print("\nNote:")
        print("  - For private groups/channels, use negative chat IDs: -100<channel_id>")
        print("  - Individual mode: Forwards one by one with detailed feedback")
        print("  - Bulk mode: Faster but less detailed feedback")
        sys.exit(1)
    
    try:
        source = int(sys.argv[1])
        dest = int(sys.argv[2])
        start = int(sys.argv[3])
        end = int(sys.argv[4])
    except ValueError:
        print("❌ Error: Chat IDs and message IDs must be numbers")
        sys.exit(1)
    
    # Check if bulk mode
    bulk_mode = len(sys.argv) > 5 and sys.argv[5] == '--bulk'
    
    if bulk_mode:
        asyncio.run(forward_messages_bulk(source, dest, start, end))
    else:
        asyncio.run(forward_messages(source, dest, start, end))
