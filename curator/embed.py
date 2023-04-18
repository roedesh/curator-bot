"""Helper functions for creating the curated messages"""

from typing import List, Optional

import discord


def create_curated_message_embeds(
    message: discord.Message, permalink: Optional[str]
) -> List[discord.Embed]:
    """Creates the Discord embeds that should be added to the message"""

    avatar_url = message.author.avatar.url if message.author.avatar else ""

    details_embed = discord.Embed(title="A post has been curated!", description="")
    details_embed.set_author(name=message.author.name, icon_url=avatar_url)
    details_embed.add_field(
        name="",
        value=f":calendar_spiral: <t:{int(message.created_at.timestamp())}:R>",
    )

    if permalink:
        details_embed.add_field(name="", value=f":link: [Permalink]({permalink})")

    content_embed = discord.Embed(description=message.content)

    attachment_embeds = []
    for attachment in message.attachments:
        # We give each attachment the same URL, so that images are shown in a grid.
        attachment_embeds.append(
            discord.Embed(url="https://discord.com", description="").set_image(
                url=attachment.url
            )
        )

    return [details_embed, content_embed, *attachment_embeds]
