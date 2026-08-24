# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:34:40 2026

@author: fatemeh
"""

# src/telegram.py
# Telegram Channel Scraper – Fetch Messages from a Public Channel

from telethon import TelegramClient, sync
import pandas as pd
import os
import asyncio

# ---------- YOUR CREDENTIALS ----------
API_ID = #change with yours
API_HASH = ''->#change with yours  
PHONE_NUMBER = ""#change with yours 

# Output directory (reuse your existing one)
OUTPUT_DIR = r"C:\Users\Administrator\Desktop\new"

async def scrape_telegram_channel(channel_username, limit=300):
    print("="*60)
    print(f"⭐ TELEGRAM SCRAPER: @{channel_username}")
    print("="*60)

    # Create client WITHOUT bot token – using your personal account
    client = TelegramClient('user_session', API_ID, API_HASH)
    
    try:
        # Start with your phone number (you'll be prompted for a code)
        await client.start(phone=PHONE_NUMBER)
        print("✅ Logged in as your personal account!")

        # Get the channel entity
        channel = await client.get_entity(f"@{channel_username}")
        print(f"📢 Channel: {channel.title} (ID: {channel.id})")

        # Fetch messages (same as before)
        all_messages = []
        offset_id = 0

        while len(all_messages) < limit:
            messages = await client.get_messages(
                channel,
                limit=min(100, limit - len(all_messages)),
                offset_id=offset_id
            )
            if not messages:
                break

            all_messages.extend(messages)
            offset_id = messages[-1].id
            print(f"   Fetched {len(messages)} messages (total: {len(all_messages)})")

            if len(messages) < 100:
                break

        # Convert to dict list
        message_list = []
        for msg in all_messages:
            message_list.append({
                'message_id': msg.id,
                'sender': msg.sender_id,
                'date': msg.date,
                'text': msg.text or '',
                'views': getattr(msg, 'views', None),
                'replies': getattr(msg, 'replies', None),
            })

        print(f"\n✅ Successfully fetched {len(message_list)} messages.")

        # Save to CSV
        if message_list:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            df = pd.DataFrame(message_list)
            df['channel'] = channel_username
            file_path = os.path.join(OUTPUT_DIR, "telegram_messages.csv")
            df.to_csv(file_path, index=False, encoding='utf-8')
            print(f"   ✅ Saved {len(message_list)} messages to {file_path}")

        return message_list

    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    finally:
        await client.disconnect()
        print("🔌 Disconnected.")

# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    channel = input("Enter channel username (without @, e.g., binance_announcements): ").strip()
    if not channel:
        channel = "binance_announcements"

    # Get or create a running event loop
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Run the async function
    if loop.is_running():
        # If loop is already running, create a task (for Jupyter/IPython)
        import nest_asyncio
        nest_asyncio.apply()
        messages = loop.run_until_complete(scrape_telegram_channel(channel, limit=300))
    else:
        messages = loop.run_until_complete(scrape_telegram_channel(channel, limit=300))
    
    print(f"\n✅ Done! Scraped {len(messages)} messages.")
