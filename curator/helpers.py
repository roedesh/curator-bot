"""General helper functions."""

from typing import List

import discord


def construct_permalink(message: discord.Message):
    """
    Constructs the permalink of a Discord message.
    Returns None if the message does not contain a guild ID.
    """

    return (
        f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        if message.guild
        else None
    )


def map_to_int(str_list: List[str]):
    """Maps a list of strings to integers."""
    return list(map(lambda str_value: int(str_value), str_list))
