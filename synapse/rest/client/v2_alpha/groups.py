# -*- coding: utf-8 -*-
# Copyright 2017 Vector Creations Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from twisted.internet import defer

from synapse.http.servlet import RestServlet

from ._base import client_v2_patterns

import logging

logger = logging.getLogger(__name__)


class GroupServlet(RestServlet):
    PATTERNS = client_v2_patterns("/groups/(?P<group_id>[^/]*)/profile$")

    def __init__(self, hs):
        super(GroupServlet, self).__init__()
        self.auth = hs.get_auth()
        self.clock = hs.get_clock()
        self.groups_handler = hs.get_groups_handler()

    @defer.inlineCallbacks
    def on_GET(self, request, group_id):
        requester = yield self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()

        group_description = yield self.groups_handler.get_group_profile(group_id, user_id)

        defer.returnValue((200, group_description))


class GroupSummaryServlet(RestServlet):
    PATTERNS = client_v2_patterns("/groups/(?P<group_id>[^/]*)/summary$")

    def __init__(self, hs):
        super(GroupSummaryServlet, self).__init__()
        self.auth = hs.get_auth()
        self.clock = hs.get_clock()
        self.groups_handler = hs.get_groups_handler()

    @defer.inlineCallbacks
    def on_GET(self, request, group_id):
        requester = yield self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()

        get_group_summary = yield self.groups_handler.get_group_summary(group_id, user_id)

        defer.returnValue((200, get_group_summary))


class GroupRoomServlet(RestServlet):
    PATTERNS = client_v2_patterns("/groups/(?P<group_id>[^/]*)/rooms$")

    def __init__(self, hs):
        super(GroupRoomServlet, self).__init__()
        self.auth = hs.get_auth()
        self.clock = hs.get_clock()
        self.groups_handler = hs.get_groups_handler()

    @defer.inlineCallbacks
    def on_GET(self, request, group_id):
        requester = yield self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()

        result = yield self.groups_handler.get_rooms_in_group(group_id, user_id)

        defer.returnValue((200, result))


class GroupUsersServlet(RestServlet):
    PATTERNS = client_v2_patterns("/groups/(?P<group_id>[^/]*)/users$")

    def __init__(self, hs):
        super(GroupUsersServlet, self).__init__()
        self.auth = hs.get_auth()
        self.clock = hs.get_clock()
        self.groups_handler = hs.get_groups_handler()

    @defer.inlineCallbacks
    def on_GET(self, request, group_id):
        requester = yield self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()

        result = yield self.groups_handler.get_users_in_group(group_id, user_id)

        defer.returnValue((200, result))


def register_servlets(hs, http_server):
    GroupServlet(hs).register(http_server)
    GroupSummaryServlet(hs).register(http_server)
    GroupUsersServlet(hs).register(http_server)
    GroupRoomServlet(hs).register(http_server)
