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
intents.guilds = True
intents.messages = True
intents.message_content = True


async def send_message(channel, messages):
    try:
        async with channel.typing():
            await asyncio.sleep(random.uniform(1.0, 3.0))

        msg = random.choice(messages)
        await channel.send(msg)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sent to #{channel.name}")

    except Exception as e:
        print(f"[!] Send failed: {e}")


async def countdown_send(channel, seconds):
    try:
        while seconds > 0:
            mins = seconds // 60
            secs = seconds % 60

            msg = f"⏳ {mins}m {secs}s remaining"
            await channel.send(msg)

            print(f"[Countdown] {mins}m {secs}s remaining")

            await asyncio.sleep(60)
            seconds -= 60

    except Exception as e:
        print(f"[!] Countdown error: {e}")


async def message_loop(client: discord.Client):
    await client.wait_until_ready()

    while not client.is_closed():
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending messages...")

        for channel_id, messages in targets.items():
            try:
                channel = await client.fetch_channel(channel_id)

                await send_message(channel, messages)

                sleep_time = 120  # change to your real delay later
                print("[⏱] Starting countdown...")
                await countdown_send(channel, sleep_time)

            except Exception as e:
                print(f"[!] Channel error: {e}")


class MyClient(discord.Client):
    async def setup_hook(self):
        asyncio.create_task(message_loop(self))


client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f" Logged in as {client.user} ({client.user.id})")

client.loop.create_task(message_loop())
client.run(TOKEN, bot=False)
