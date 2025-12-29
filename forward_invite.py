#!/usr/bin/env python3
"""
Forward messages using invite link for destination
"""
import asyncio
from telethon import TelegramClient

# Import configuration
try:
    from config import API_ID, API_HASH
    SESSION_NAME = 'video_uploader'
except ImportError:
    print("❌ ERROR: config.py not found!")
    exit(1)

async def forward_to_invite_link(source_chat_id, dest_invite_link, start_msg_id, end_msg_id):
    """
    Forward messages to a group using its invite link
    """
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print(f"\n{'='*60}")
        print(f"📨 Forwarding Messages via Invite Link")
        print(f"{'='*60}")
        
        try:
            # Join the destination group using invite link
            print(f"🔗 Processing invite link...")
            
            # Extract hash from invite link
            invite_hash = dest_invite_link.split('/')[-1].replace('+', '')
            
            # Join the chat
            try:
                updates = await client(functions.messages.ImportChatInviteRequest(invite_hash))
                dest_entity = updates.chats[0]
                print(f"✅ Joined group: {dest_entity.title}")
            except Exception as e:
                # Already a member, get the entity
                if "already a participant" in str(e).lower() or "INVITE_REQUEST_SENT" in str(e):
                    print(f"✅ Already a member or request sent")
                    # Try to get entity by hash
                    dest_entity = await client.get_entity(dest_invite_link)
                else:
                    raise e
            
            # Get source entity
            source_entity = await client.get_entity(-1000000000000 - source_chat_id)
            
            print(f"📤 From: {getattr(source_entity, 'title', source_chat_id)}")
            print(f"📥 To: {getattr(dest_entity, 'title', 'Group')}")
            print(f"📊 Message range: {start_msg_id} to {end_msg_id}")
            print(f"📝 Total messages: {end_msg_id - start_msg_id + 1}")
            print(f"{'='*60}\n")
            
            # Forward messages one by one
            successful = 0
            failed = 0
            skipped = 0
            
            for msg_id in range(start_msg_id, end_msg_id + 1):
                try:
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
                    error_msg = str(e)
                    if "protected" in error_msg.lower():
                        print(f"❌ Message {msg_id}: Failed - Source chat has forwarding protection")
                    else:
                        print(f"❌ Message {msg_id}: Failed - {error_msg[:50]}")
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
            
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == '__main__':
    import sys
    from telethon.tl import functions
    
    if len(sys.argv) < 5:
        print("Usage:")
        print("  python forward_invite.py <source_chat_id> <dest_invite_link> <start_msg_id> <end_msg_id>")
        print("\nExample:")
        print('  python forward_invite.py 2732989224 "https://t.me/+YEZw2KYgHf9lNGJl" 2 32')
        sys.exit(1)
    
    try:
        source = int(sys.argv[1])
        dest_link = sys.argv[2]
        start = int(sys.argv[3])
        end = int(sys.argv[4])
    except ValueError:
        print("❌ Error: Source chat ID and message IDs must be numbers")
        sys.exit(1)
    
    asyncio.run(forward_to_invite_link(source, dest_link, start, end))
