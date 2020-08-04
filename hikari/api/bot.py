# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright © Nekoka.tt 2019-2020
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""Core interfaces for types of Hikari application."""

from __future__ import annotations

__all__: typing.Final[typing.List[str]] = ["IBotApp"]

import abc
import typing

from hikari.api import cache
from hikari.api import event_consumer
from hikari.api import event_dispatcher
from hikari.api import shard
from hikari.api import voice

if typing.TYPE_CHECKING:
    import datetime

    from hikari.models import guilds
    from hikari.models import intents as intents_
    from hikari.models import users
    from hikari.utilities import snowflake


class IBotApp(event_consumer.IEventConsumerApp, event_dispatcher.IEventDispatcherApp, voice.IVoiceApp, abc.ABC):
    """Base for bot applications.

    Bots are components that have access to a HTTP API, an event dispatcher,
    and an event consumer.

    Additionally, bots may contain a collection of Gateway client objects. This
    is not mandatory though, as the bot may consume its events from another managed
    component that manages gateway zookeeping instead.
    """

    __slots__: typing.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def heartbeat_latencies(self) -> typing.Mapping[int, typing.Optional[datetime.timedelta]]:
        """Return a mapping of shard ID to heartbeat latency.

        Any shards that are not yet started will be `builtins.None`.

        Returns
        -------
        typing.Mapping[builtins.int, datetime.timedelta]
            Each shard ID mapped to the corresponding heartbeat latency.
        """

    @property
    @abc.abstractmethod
    def heartbeat_latency(self) -> typing.Optional[datetime.timedelta]:
        """Return the average heartbeat latency of all started shards.

        If no shards are started, this will return `None`.

        Returns
        -------
        datetime.timedelta or builtins.None
            The average heartbeat latency of all started shards, or
            `builtins.None`.
        """

    @property
    @abc.abstractmethod
    def intents(self) -> typing.Optional[intents_.Intent]:
        """Return the intents registered for the application.

        If no intents are in use, `builtins.None` is returned instead.

        Returns
        -------
        hikari.models.intents.Intent or builtins.None
            The intents registered on this application.
        """

    @property
    @abc.abstractmethod
    def me(self) -> typing.Optional[users.OwnUser]:
        """Return the bot user, if known.

        This should be available as soon as the bot has fired the
        `hikari.events.lifetime_events.StartingEvent`.

        Until then, this may or may not be `builtins.None`.

        Returns
        -------
        hikari.models.users.OwnUser or builtins.None
            The bot user, if known, otherwise `builtins.None`.
        """

    @property
    @abc.abstractmethod
    def started_at(self) -> typing.Optional[datetime.datetime]:
        """Return the timestamp when the bot was started.

        If the application has not been started, then this will return
        `builtins.None`.

        Returns
        -------
        datetime.datetime or builtins.None
            The date/time that the application started at, or `builtins.None` if
            not yet running.
        """

    @property
    @abc.abstractmethod
    def shards(self) -> typing.Mapping[int, shard.IGatewayShard]:
        """Return a mapping of the shards managed by this process.

        This mapping will map each shard ID to the shard instance.

        If the application has not started, it is acceptable to assume that
        this will be empty.

        Returns
        -------
        typing.Mapping[builtins.int, hikari.api.gateway.shard.IGatewayShard]
            The mapping of shard ID to shard instance.
        """

    @property
    @abc.abstractmethod
    def shard_count(self) -> int:
        """Return the number of shards in the application in total.

        This does not count the active shards, but produces the total shard
        count sent when you connected. If you distribute your shards between
        multiple processes or hosts, this will represent the combined total
        shard count (minus any duplicates).

        For the instance specific shard count, return the `builtins.len` of
        `IBotApp.shards`.

        If you are using auto-sharding (i.e. not providing explicit sharding
        preferences on startup), then this will be `0` until the application
        has been started properly.

        Returns
        -------
        builtins.int
            The number of shards in the entire application.
        """

    @property
    @abc.abstractmethod
    def uptime(self) -> datetime.timedelta:
        """Return how long the bot has been alive for.

        If the application has not been started, then this will return
        a `datetime.timedelta` of 0 seconds.

        Returns
        -------
        datetime.timedelta
            The number of seconds the application has been running.
        """

    @abc.abstractmethod
    def get_guild(self, guild_id: snowflake.Snowflake) -> typing.Optional[guilds.GatewayGuild]:
        """Find a cached guild.

        Parameters
        ----------
        guild_id : hikari.utilities.snowflake.Snowflake
            The guild ID to search for.

        Returns
        -------
        hikari.models.guilds.GatewayGuild or builtins.None
            The cached guild, or `builtins.None` if it is not cached.
        """

    @abc.abstractmethod
    def get_guilds(self) -> cache.ICacheView[snowflake.Snowflake, guilds.GatewayGuild]:
        """Generate a view of all cached guilds and return it.

        Returns
        -------
        hikari.api.cache.ICacheView[hikari.utilities.snowflake.Snowflake, hikari.models.guilds.GatewayGuild]
            The view of the guild cache.
        """

    @abc.abstractmethod
    async def fetch_guild(self, guild_id: snowflake.Snowflake) -> typing.Optional[guilds.Guild]:
        """Fetch a guild from the API.

        Parameters
        ----------
        guild_id : hikari.utilities.snowflake.Snowflake
            The guild ID to search for.

        Returns
        -------
        hikari.models.guilds.Guild or builtins.None
            The guild, or `builtins.None` if it is not found.
        """

    @abc.abstractmethod
    def get_user(self, user_id: snowflake.Snowflake) -> typing.Optional[users.User]:
        """Find a cached user.

        Parameters
        ----------
        user_id : hikari.utilities.snowflake.Snowflake
            The user ID to search for.

        Returns
        -------
        hikari.models.users.User or builtins.None
            The cached user, or `builtins.None` if it is not cached.
        """

    @abc.abstractmethod
    def get_users(self) -> cache.ICacheView[snowflake.Snowflake, users.User]:
        """Generate a view of all cached users and return it.

        Returns
        -------
        hikari.api.cache.ICacheView[hikari.utilities.snowflake.Snowflake, hikari.models.users.User]
            The view of the user cache.
        """

    @abc.abstractmethod
    async def fetch_user(self, user_id: snowflake.Snowflake) -> typing.Optional[users.User]:
        """Fetch a user from the API.

        Parameters
        ----------
        user_id : hikari.utilities.snowflake.Snowflake
            The user ID to search for.

        Returns
        -------
        hikari.models.users.User or builtins.None
            The user, or `builtins.None` if it is not found.
        """