import discord
import os
import asyncio
import random
from datetime import datetime
from transformers import pipeline

# Load paraphrasing model (this may take time on first run)
rephrase = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

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

client = discord.Client(intents=intents)


def rephrase_message(text):
    try:
        out = rephrase(
            f"paraphrase: {text} </s>",
            max_length=64,
            num_return_sequences=1,
            do_sample=True
        )
        return out[0]['generated_text']
    except Exception as e:
        print(f"[!] Rephrase failed: {e}")
        return text


async def send_message(channel, messages):
    try:
        async with channel.typing():
            await asyncio.sleep(random.uniform(1.0, 3.0))

        original_msg = random.choice(messages)
        msg = rephrase_message(original_msg)

        await channel.send(msg)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sent to #{channel.name}")

    except Exception as e:
        print(f"[!] Failed in {channel.id}: {e}")


async def countdown_sleep(seconds):
    start = datetime.now()

    while True:
        elapsed = (datetime.now() - start).total_seconds()
        remaining = int(seconds - elapsed)

        if remaining <= 0:
            break

        mins = remaining // 60
        secs = remaining % 60

        print(f"[⏳] Remaining: {mins}m {secs}s")
        await asyncio.sleep(60)


async def message_loop():
    await client.wait_until_ready()

    while not client.is_closed():
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending messages...")

        for channel_id, messages in targets.items():
            channel = client.get_channel(channel_id)

            if channel is None:
                try:
                    channel = await client.fetch_channel(channel_id)
                except Exception:
                    print(f"[!] Cannot access channel {channel_id}")
                    continue

            await send_message(channel, messages)

        sleep_time = random.randint(41400, 45000)  # ~11.5–12.5 hrs
        print(f"[⏱] Sleeping for ~{sleep_time // 3600} hours")

        await countdown_sleep(sleep_time)


@client.event
async def on_ready():
    print(f" Logged in as {client.user} ({client.user.id})")

client.loop.create_task(message_loop())
client.run(TOKEN, bot=False)
