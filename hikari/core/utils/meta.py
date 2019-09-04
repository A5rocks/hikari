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
"""
Metadata tools that look at documentation and versioning of things.

Contains interpreter introspection utilities, Hikari introspection utilities (e.g. version, author, etc) and
documentation decorators used within this library. There is usually zero need for you to touch anything in this
package.
"""
import enum
import inspect


class APIResource(enum.Enum):
    """A documentation resource for the underlying API."""

    AUDIT_LOG = "/resources/audit-log"
    CHANNEL = "/resources/channel"
    EMOJI = "/resources/emoji"
    GUILD = "/resources/guild"
    INVITE = "/resources/invite"
    OAUTH2 = "/topics/oauth2"
    USER = "/resources/user"
    VOICE = "/resources/voice"
    WEBHOOK = "/resources/webhook"
    GATEWAY = "/topics/gateway"


def link_developer_portal(scope: APIResource, specific_resource: str = None):
    """Injects some common documentation into the given member's docstring."""

    def decorator(obj):
        base_url = "https://discordapp.com/developers/docs"
        doc = inspect.cleandoc(inspect.getdoc(obj) or "")
        base_resource = base_url + scope.value
        frag = obj.__name__.lower().replace("_", "-") if specific_resource is None else specific_resource
        uri = base_resource + "#" + frag

        setattr(obj, "__doc__", f"Read the documentation on `Discord's developer portal <{uri}>`__.\n\n{doc}")
        return obj

    return decorator


def unofficial(obj):
    """
    Marks an element that had to be reverse engineered to work out how to use it, rather than being documented
    properly...
    """
    doc = inspect.cleandoc(inspect.getdoc(obj) or "")
    setattr(
        obj,
        "__doc__",
        f"{doc}\nNote:\n    Oh boy! Undocumented functionality! This is currently not documented in Discord's API "
        "documentation, so use this at your own risk. It may break if Discord change their implementation, and "
        "the expected functionality is purely based on speculation and reverse engineering.",
    )
    return obj


__all__ = ("APIResource", "link_developer_portal", "unofficial")
