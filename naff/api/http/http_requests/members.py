from typing import TYPE_CHECKING, cast
from datetime import datetime

import discord_typings

from naff.client.const import Missing, MISSING
from naff.models.naff.protocols import CanRequest
from ..route import Route, PAYLOAD_TYPE
from naff.models.discord.timestamp import Timestamp
from naff.client.utils.serializer import dict_filter_none

__all__ = ("MemberRequests",)


if TYPE_CHECKING:
    from naff.models.discord.snowflake import Snowflake_Type


class MemberRequests(CanRequest):
    async def get_member(
        self, guild_id: "Snowflake_Type", user_id: "Snowflake_Type"
    ) -> discord_typings.GuildMemberData:
        """
        Get a member of a guild by ID.

        Args:
            guild_id: The id of the guild
            user_id: The user id to grab

        """
        result = await self.request(Route("GET", f"/guilds/{int(guild_id)}/members/{int(user_id)}"))
        return cast(discord_typings.GuildMemberData, result)

    async def list_members(
        self, guild_id: "Snowflake_Type", limit: int = 1, after: "Snowflake_Type | None" = None
    ) -> list[discord_typings.GuildMemberData]:
        """
        List the members of a guild.

        Args:
            guild_id: The ID of the guild
            limit: How many members to get (max 1000)
            after: Get IDs after this snowflake

        """
        payload: PAYLOAD_TYPE = {
            "limit": limit,
            "after": int(after) if after else None,
        }
        payload = dict_filter_none(payload)

        result = await self.request(Route("GET", f"/guilds/{int(guild_id)}/members"), params=payload)
        return cast(list[discord_typings.GuildMemberData], result)

    async def search_guild_members(
        self, guild_id: "Snowflake_Type", query: str, limit: int = 1
    ) -> list[discord_typings.GuildMemberData]:
        """
        Search a guild for members who's username or nickname starts with provided string.

        Args:
            guild_id: The ID of the guild to search
            query: The string to search for
            limit: The number of members to return

        """
        result = await self.request(
            Route("GET", f"/guilds/{int(guild_id)}/members/search"), params={"query": query, "limit": limit}
        )
        return cast(list[discord_typings.GuildMemberData], result)

    async def modify_guild_member(
        self,
        guild_id: "Snowflake_Type",
        user_id: "Snowflake_Type",
        nickname: str | None | Missing = MISSING,
        roles: list["Snowflake_Type"] | None = None,
        mute: bool | None = None,
        deaf: bool | None = None,
        channel_id: "Snowflake_Type | None" = None,
        communication_disabled_until: str | datetime | Timestamp | None | Missing = MISSING,
        reason: str | None = None,
    ) -> discord_typings.GuildMemberData:
        """
        Modify attributes of a guild member.

        Args:
            guild_id: The ID of the guild
            user_id: The ID of the user we're modifying
            nickname: Value to set users nickname to
            roles: Array of role ids the member is assigned
            mute: Whether the user is muted in voice channels. Will throw a 400 if the user is not in a voice channel
            deaf: Whether the user is deafened in voice channels
            channel_id: id of channel to move user to (if they are connected to voice)
            communication_disabled_until: 	when the user's timeout will expire and the user will be able to communicate in the guild again
            reason: An optional reason for the audit log

        Returns:
            The updated member object

        """
        if isinstance(communication_disabled_until, datetime):
            communication_disabled_until = communication_disabled_until.isoformat()

        payload: PAYLOAD_TYPE = {
            "roles": roles,
            "mute": mute,
            "deaf": deaf,
            "channel_id": int(channel_id) if channel_id else None,
        }
        payload = dict_filter_none(payload)

        if not isinstance(nickname, Missing):
            payload["nick"] = nickname
        if not isinstance(communication_disabled_until, Missing):
            payload["communication_disabled_until"] = communication_disabled_until

        result = await self.request(
            Route("PATCH", f"/guilds/{int(guild_id)}/members/{int(user_id)}"),
            payload=payload,
            reason=reason,
        )
        return cast(discord_typings.GuildMemberData, result)

    async def modify_current_member(
        self,
        guild_id: "Snowflake_Type",
        nickname: str | None | Missing = MISSING,
        reason: str | None = None,
    ) -> None:
        """
        Modify attributes of the user

        Args:
            guild_id: The ID of the guild to modify current member in
            nickname: The new nickname to apply
            reason: An optional reason for the audit log

        """
        payload: PAYLOAD_TYPE = {"nick": nickname if not isinstance(nickname, Missing) else None}
        await self.request(
            Route("PATCH", f"/guilds/{int(guild_id)}/members/@me"),
            payload=payload,
            reason=reason,
        )

    async def add_guild_member_role(
        self,
        guild_id: "Snowflake_Type",
        user_id: "Snowflake_Type",
        role_id: "Snowflake_Type",
        reason: str | None = None,
    ) -> None:
        """
        Adds a role to a guild member.

        Args:
            guild_id: The ID of the guild
            user_id: The ID of the user
            role_id: The ID of the role to add
            reason: The reason for this action

        """
        await self.request(
            Route("PUT", f"/guilds/{int(guild_id)}/members/{int(user_id)}/roles/{int(role_id)}"), reason=reason
        )

    async def remove_guild_member_role(
        self,
        guild_id: "Snowflake_Type",
        user_id: "Snowflake_Type",
        role_id: "Snowflake_Type",
        reason: str | None = None,
    ) -> None:
        """
        Remove a role from a guild member.

        Args:
            guild_id: The ID of the guild
            user_id: The ID of the user
            role_id: The ID of the role to remove
            reason: The reason for this action

        """
        await self.request(
            Route("DELETE", f"/guilds/{int(guild_id)}/members/{int(user_id)}/roles/{int(role_id)}"), reason=reason
        )
