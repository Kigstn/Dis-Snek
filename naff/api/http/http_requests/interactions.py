from typing import TYPE_CHECKING, cast

import discord_typings

from naff.models.naff.protocols import CanRequest
from naff.client.const import GLOBAL_SCOPE
from ..route import Route

__all__ = ("InteractionRequests",)


if TYPE_CHECKING:
    from naff.models.discord.snowflake import Snowflake_Type
    from naff import UPLOADABLE_TYPE


class InteractionRequests(CanRequest):
    async def delete_application_command(
        self, application_id: "Snowflake_Type", guild_id: "Snowflake_Type", command_id: "Snowflake_Type"
    ) -> None:
        """
        Delete an existing application command for this application.

        Args:
            application_id: the what application to delete for
            guild_id: specify a guild to delete commands from
            command_id: the command to delete

        """
        if guild_id == GLOBAL_SCOPE:
            await self.request(Route("DELETE", f"/applications/{int(application_id)}/commands/{int(command_id)}"))
        else:
            await self.request(
                Route(
                    "DELETE", f"/applications/{int(application_id)}/guilds/{int(guild_id)}/commands/{int(command_id)}"
                )
            )

    async def get_application_commands(
        self, application_id: "Snowflake_Type", guild_id: "Snowflake_Type", with_localisations: bool = True
    ) -> list[discord_typings.ApplicationCommandData]:
        """
        Get all application commands for this application from discord.

        Args:
            application_id: the what application to query
            guild_id: specify a guild to get commands from
            with_localisations: whether to include all localisations in the response

        Returns:
            Application command data

        """
        if guild_id == GLOBAL_SCOPE:
            return await self.request(
                Route("GET", f"/applications/{application_id}/commands"),
                params={"with_localizations": int(with_localisations)},
            )
        return await self.request(
            Route("GET", f"/applications/{application_id}/guilds/{guild_id}/commands"),
            params={"with_localizations": int(with_localisations)},
        )

    async def overwrite_application_commands(
        self, app_id: "Snowflake_Type", data: list[dict], guild_id: "Snowflake_Type"  # todo type "data"
    ) -> list[discord_typings.ApplicationCommandData]:
        """
        Take a list of commands and overwrite the existing command list within the given scope

        Args:
            app_id: The application ID of this bot
            guild_id: The ID of the guild this command is for, if this is a guild command
            data: List of your interaction data

        """
        if guild_id == GLOBAL_SCOPE:
            result = await self.request(Route("PUT", f"/applications/{app_id}/commands"), payload=data)
        else:
            result = await self.request(
                Route("PUT", f"/applications/{app_id}/guilds/{int(guild_id)}/commands"), payload=data
            )
        return cast(list[discord_typings.ApplicationCommandData], result)

    async def create_application_command(
        self, app_id: "Snowflake_Type", command: dict, guild_id: "Snowflake_Type"
    ) -> discord_typings.ApplicationCommandData:
        """
        Add a given command to scope.

        Args:
            app_id: The application ID of this bot
            command: A dictionary representing a command to be created
            guild_id: The ID of the guild this command is for, if this is a guild command

        Returns:
            An application command object
        """
        if guild_id == GLOBAL_SCOPE:
            result = await self.request(Route("POST", f"/applications/{app_id}/commands"), payload=command)
        else:
            result = await self.request(
                Route("POST", f"/applications/{app_id}/guilds/{int(guild_id)}/commands"), payload=command
            )
        return cast(discord_typings.ApplicationCommandData, result)

    async def post_initial_response(
        self, payload: dict, interaction_id: str, token: str, files: list["UPLOADABLE_TYPE"] | None = None
    ) -> None:
        """
        Post an initial response to an interaction.

        Args:
            payload: the payload to send
            interaction_id: the id of the interaction
            token: the token of the interaction
            files: The files to send in this message

        """
        return await self.request(
            Route("POST", f"/interactions/{interaction_id}/{token}/callback"), payload=payload, files=files
        )

    async def post_followup(
        self, payload: dict, application_id: "Snowflake_Type", token: str, files: list["UPLOADABLE_TYPE"] | None = None
    ) -> None:
        """
        Send a followup to an interaction.

        Args:
            payload: the payload to send
            application_id: the id of the application
            token: the token of the interaction
            files: The files to send with this interaction

        """
        return await self.request(
            Route("POST", f"/webhooks/{int(application_id)}/{token}"), payload=payload, files=files
        )

    async def edit_interaction_message(
        self,
        payload: dict,
        application_id: "Snowflake_Type",
        token: str,
        message_id: str = "@original",
        files: list["UPLOADABLE_TYPE"] | None = None,
    ) -> discord_typings.MessageData:
        """
        Edits an existing interaction message.

        Args:
            payload: The payload to send.
            application_id: The id of the application.
            token: The token of the interaction.
            message_id: The target message to edit. Defaults to @original which represents the initial response message.
            files: The files to send with this interaction

        Returns:
            The edited message data.

        """
        result = await self.request(
            Route("PATCH", f"/webhooks/{int(application_id)}/{token}/messages/{message_id}"),
            payload=payload,
            files=files,
        )
        return cast(discord_typings.MessageData, result)

    async def get_interaction_message(
        self, application_id: "Snowflake_Type", token: str, message_id: str = "@original"
    ) -> discord_typings.MessageData:
        """
        Gets an existing interaction message.

        Args:
            application_id: The id of the application.
            token: The token of the interaction.
            message_id: The target message to get. Defaults to @original which represents the initial response message.

        Returns:
            The message data.

        """
        result = await self.request(Route("GET", f"/webhooks/{int(application_id)}/{token}/messages/{message_id}"))
        return cast(discord_typings.MessageData, result)

    async def edit_application_command_permissions(
        self,
        application_id: "Snowflake_Type",
        scope: "Snowflake_Type",
        command_id: "Snowflake_Type",
        permissions: list[dict],  # todo better typing
    ) -> discord_typings.ApplicationCommandPermissionsData:
        """
        Edits command permissions for a specific command.

        Args:
            application_id: the id of the application
            scope: The scope this command is in
            command_id: The command id to edit
            permissions: The permissions to set to this command

        Returns:
            Guild Application Command Permissions

        """
        result = await self.request(
            Route(
                "PUT", f"/applications/{int(application_id)}/guilds/{int(scope)}/commands/{int(command_id)}/permissions"
            ),
            payload=permissions,
        )
        return cast(discord_typings.ApplicationCommandPermissionsData, result)

    async def get_application_command_permissions(
        self, application_id: "Snowflake_Type", scope: "Snowflake_Type", command_id: "Snowflake_Type"
    ) -> list[discord_typings.ApplicationCommandPermissionsData]:
        """
        Get permission data for a command.

        Args:
            application_id: the id of the application
            scope: The scope this command is in
            command_id: The command id to edit

        Returns:
            guild application command permissions

        """
        result = await self.request(
            Route(
                "GET", f"/applications/{int(application_id)}/guilds/{int(scope)}/commands/{int(command_id)}/permissions"
            )
        )
        return cast(list[discord_typings.ApplicationCommandPermissionsData], result)

    async def batch_get_application_command_permissions(
        self, application_id: "Snowflake_Type", scope: "Snowflake_Type"
    ) -> list[discord_typings.ApplicationCommandPermissionsData]:
        """
        Get permission data for all commands in a scope.

        Args:
            application_id: the id of the application
            scope: The scope this command is in

        Returns:
            list of guild application command permissions

        """
        result = await self.request(
            Route("GET", f"/applications/{int(application_id)}/guilds/{int(scope)}/commands/permissions")
        )
        return cast(list[discord_typings.ApplicationCommandPermissionsData], result)
