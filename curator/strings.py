"""General helper functions"""

import discord


def construct_permalink(message: discord.Message, target_channel_id: int):
    """
    Constructs the permalink of a Discord message.
    Returns None if the message does not contain a guild ID.
    """

    return (
        f"https://discord.com/channels/{message.guild.id}/{target_channel_id}/{message.id}"
        if message.guild
        else None
    )
