#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019
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
from unittest import mock

import pytest

from hikari.orm import fabric
from hikari.orm import state_registry
from hikari.orm.models import guilds
from hikari.orm.models import permissions
from hikari.orm.models import roles
from tests.hikari import _helpers


@pytest.fixture
def mock_state_registry():
    return mock.MagicMock(spec_set=state_registry.IStateRegistry)


@pytest.fixture()
def fabric_obj(mock_state_registry):
    return fabric.Fabric(state_registry=mock_state_registry)


@pytest.fixture
def payload():
    return {
        "id": "41771983423143936",
        "name": "WE DEM BOYZZ!!!!!!",
        "color": 3447003,
        "hoist": True,
        "position": 1,
        "permissions": 66321471,
        "managed": False,
        "mentionable": False,
    }


@pytest.mark.model
def test_Role(fabric_obj, payload):
    guild_obj = _helpers.mock_model(guilds.Guild)
    role_obj = roles.Role(fabric_obj, payload, guild_obj)

    assert role_obj.id == 41771983423143936
    assert role_obj.name == "WE DEM BOYZZ!!!!!!"
    assert role_obj.color == 0x3498DB
    assert role_obj.hoist is True
    assert role_obj.position == 1
    assert role_obj.guild == guild_obj
    assert role_obj.permissions == (
        permissions.Permission.USE_VAD
        | permissions.Permission.MOVE_MEMBERS
        | permissions.Permission.DEAFEN_MEMBERS
        | permissions.Permission.MUTE_MEMBERS
        | permissions.Permission.SPEAK
        | permissions.Permission.CONNECT
        | permissions.Permission.MENTION_EVERYONE
        | permissions.Permission.READ_MESSAGE_HISTORY
        | permissions.Permission.ATTACH_FILES
        | permissions.Permission.EMBED_LINKS
        | permissions.Permission.MANAGE_MESSAGES
        | permissions.Permission.SEND_TTS_MESSAGES
        | permissions.Permission.SEND_MESSAGES
        | permissions.Permission.VIEW_CHANNEL
        | permissions.Permission.MANAGE_GUILD
        | permissions.Permission.MANAGE_CHANNELS
        | permissions.Permission.ADMINISTRATOR
        | permissions.Permission.BAN_MEMBERS
        | permissions.Permission.KICK_MEMBERS
        | permissions.Permission.CREATE_INSTANT_INVITE
    )
    assert role_obj.managed is False
    assert role_obj.mentionable is False