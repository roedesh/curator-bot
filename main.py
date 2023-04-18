"""Entry point for the Discord bot"""

import asyncio
import logging
import os

import discord
from discord.utils import get
from dotenv import load_dotenv

from curator.db import get_curation_from_db, insert_curation_to_db, setup_db
from curator.embed import create_curated_message_embeds
from curator.strings import construct_permalink

# Load environment variables
load_dotenv()

# Collect configuration
DEBUG = os.getenv("DEBUG", "False") == "True"
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", None) or 0)
CURATIONS_CHANNEL_ID = int(os.getenv("CURATIONS_CHANNEL_ID", None) or 0)
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
EMOJI_NAME = os.getenv("EMOJI_NAME", "thumbsup")
REACTION_THRESHOLD = int(os.getenv("REACTION_THRESHOLD", None) or 5)
DATABASE_PATH = os.getenv("DATABASE_PATH", "curator.sqlite3")

# Setup logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logging.getLogger("discord").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Setup database and tables
conn = setup_db(DATABASE_PATH)

# Setup Discord bot and its intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
bot = discord.Bot(
    description="Discord bot that curates messages posted by members.",
    intents=intents,
)


@bot.event
async def on_ready():
    """Logs when the bot is ready"""

    logger.info("%s is ready and online!", bot.user)

    for guild in bot.guilds:
        logger.info("Logged into guild '%s' (ID=%s)", guild.name, guild.id)

    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel:
        channel_name = target_channel.name
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"#{channel_name}"
            )
        )
        logger.info("Changed presence to '%s'", f"Watching #{channel_name}")


@bot.event
async def on_raw_reaction_add(event: discord.RawReactionActionEvent):
    """Handles new reactions being added and curates the post if the threshold is met"""

    logger.debug(
        "Event 'on_raw_reaction_add' fired in %s guild. Channel is %s and target channel is %s.",
        event.guild_id,
        event.channel_id,
        TARGET_CHANNEL_ID,
    )

    if event.channel_id != TARGET_CHANNEL_ID or event.emoji.name != EMOJI_NAME:
        return

    curation_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if not curation_channel or not isinstance(curation_channel, discord.TextChannel):
        return logger.error(
            "Did not find the curation text-channel with ID: %s", TARGET_CHANNEL_ID
        )

    message = await curation_channel.fetch_message(event.message_id)

    # If a user adds a EMOJI_NAME reaction to their own post, remove the reaction
    if event.user_id == message.author.id:
        await message.remove_reaction(emoji=event.emoji, member=message.author)
        return

    reaction = get(message.reactions, emoji=event.emoji)
    if not reaction:
        return logger.error(
            "Did not find a reaction with the emoji: %s", event.emoji.name
        )

    if reaction.count < REACTION_THRESHOLD:
        return

    is_already_curated = get_curation_from_db(conn, message.id) is not None
    if is_already_curated:
        return

    curation_gems_channel = bot.get_channel(CURATIONS_CHANNEL_ID)
    if not curation_gems_channel or not isinstance(
        curation_gems_channel, discord.TextChannel
    ):
        return logger.error(
            "Did not find the curation gems text-channel with ID: %s",
            CURATIONS_CHANNEL_ID,
        )

    if not message.content:
        return logger.error(
            "Could not get content for message with ID: %s",
            message.id,
        )

    permalink = construct_permalink(message, TARGET_CHANNEL_ID)
    embeds = create_curated_message_embeds(message, permalink)
    curated_message = await curation_gems_channel.send(embeds=embeds)

    insert_curation_to_db(
        conn,
        message.id,
        message.author.id,
        curated_message.id,
        message.created_at.isoformat(),
    )


@bot.event
async def on_message_edit(_: discord.Message, new_message: discord.Message):
    """Synchronizes posts between curation and curation gems"""

    logger.debug(
        "Event 'on_message_edit' fired in %s guild. Channel is %s and target channel is %s.",
        new_message.guild.id,
        new_message.channel.id,
        TARGET_CHANNEL_ID,
    )

    if new_message.channel.id != TARGET_CHANNEL_ID:
        return

    curation = get_curation_from_db(conn, new_message.id)
    if not curation:
        return

    curation_gems_channel = bot.get_channel(CURATIONS_CHANNEL_ID)
    if not curation_gems_channel or not isinstance(
        curation_gems_channel, discord.TextChannel
    ):
        return logger.error(
            "Did not find the curation gems text-channel with ID: %s",
            CURATIONS_CHANNEL_ID,
        )

    curated_message_id = curation[2]
    curated_message = await curation_gems_channel.fetch_message(curated_message_id)

    if not curated_message:
        return logger.warning(
            "Did not find curated message with ID %s in curation gems channel",
            curated_message_id,
        )

    permalink = construct_permalink(new_message, TARGET_CHANNEL_ID)
    embeds = create_curated_message_embeds(new_message, permalink)
    await curated_message.edit(embeds=embeds)


async def start_bot():
    """Starts the Discord bot"""

    if not DISCORD_BOT_TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN must be set!")

    if not TARGET_CHANNEL_ID:
        raise ValueError("TARGET_CHANNEL_ID must be set!")

    if not CURATIONS_CHANNEL_ID:
        raise ValueError("CURATIONS_CHANNEL_ID must be set!")

    await bot.start(DISCORD_BOT_TOKEN)


async def close_bot():
    """Closes the Discord bots HTTP connection"""

    await bot.http.close()


loop = asyncio.get_event_loop()
try:
    logger.info("Started Discord bot...")
    loop.run_until_complete(start_bot())
except KeyboardInterrupt:
    logger.info("Keyboard interupt by user. Shutting down...")
    loop.run_until_complete(close_bot())
finally:
    loop.close()
    logger.info("Bot has been shutdown.")
