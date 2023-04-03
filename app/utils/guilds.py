import discord

from typing import Sequence, List

GUILD_IDS: Sequence[int] = (848921520776413213, 528544644678680576, 612600222622810113)


def get_guilds() -> List[discord.Object]:
    """Returns list of discord.Object with guild ID"""

    guilds = []

    for guild_ID in GUILD_IDS:
        guilds.append(discord.Object(id=guild_ID))

    return guilds
