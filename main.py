import discord
import os
import asyncio
import random
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")

targets = {
    1462125650767904768: [
        "a",
        "r",
        "rs",
        "re",
        "ra",
    ],
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def generate_message(messages):
    return random.choice(messages)


async def send_message(channel, messages):
    try:
        async with channel.typing():
            await asyncio.sleep(random.uniform(1.0, 3.0))

        msg = generate_message(messages)
        await channel.send(msg)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sent to #{channel.name}")

    except Exception as e:
        print(f"[!] Send failed: {e}")


async def countdown_sleep(seconds):
    while seconds > 0:
        mins = seconds // 60
        secs = seconds % 60

        print(f"[⏳] Remaining: {mins}m {secs}s")

        await asyncio.sleep(60)
        seconds -= 60


async def message_loop():
    await client.wait_until_ready()

    while not client.is_closed():
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending messages...")

        for channel_id, messages in targets.items():
            try:
                channel = await client.fetch_channel(channel_id)
                await send_message(channel, messages)
            except Exception as e:
                print(f"[!] Channel error: {e}")

        sleep_time = random.randint(41400, 45000)  # ~11.5–12.5 hours
        print(f"[⏱] Sleeping for ~{sleep_time // 3600} hours")

        await countdown_sleep(sleep_time)


@client.event
async def on_ready():
    print(f" Logged in as {client.user} ({client.user.id})")

client.loop.create_task(message_loop())
client.run(TOKEN, bot=False)
