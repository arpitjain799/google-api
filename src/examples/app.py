#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Google API
# Copyright (c) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Google API.
#
# Hive Google API is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Google API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Google API. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import appier

from . import base

class GoogleApp(appier.WebApp):

    def __init__(self):
        appier.WebApp.__init__(self, name = "google")

    @appier.route("/", "GET")
    def index(self):
        return self.me()

    @appier.route("/me", "GET")
    def me(self):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        user = api.self_user()
        return user

    @appier.route("/files", "GET")
    def files(self):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        contents = api.list_drive()
        return contents

    @appier.route("/files/<std:id>", "GET")
    def file(self, id):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        contents = api.get_drive(id)
        return contents

    @appier.route("/files/insert/<str:message>", "GET")
    def file_insert(self, message):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        contents = api.insert_drive(
            message,
            content_type = "text/plain",
            title = message
        )
        return contents

    @appier.route("/folders/insert/<str:title>", "GET")
    def folder_insert(self, title):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        contents = api.folder_drive(title)
        return contents

    @appier.route("/children", "GET")
    def children(self):
        url = self.ensure_api()
        if url: return self.redirect(url)
        id = self.field("id", "root")
        api = self.get_api()
        contents = api.children_drive(id = id)
        return contents

    @appier.route("/oauth", "GET")
    def oauth(self):
        code = self.field("code")
        api = self.get_api()
        access_token = api.oauth_access(code)
        self.session["gg.access_token"] = access_token
        return self.redirect(
            self.url_for("google.index")
        )

    @appier.exception_handler(appier.OAuthAccessError)
    def oauth_error(self, error):
        if "gg.access_token" in self.session: del self.session["gg.access_token"]
        return self.redirect(
            self.url_for("google.index")
        )

    def ensure_api(self):
        access_token = self.session.get("gg.access_token", None)
        if access_token: return
        api = base.get_api()
        return api.oauth_authorize()

    def get_api(self):
        access_token = self.session and self.session.get("gg.access_token", None)
        api = base.get_api()
        api.access_token = access_token
        return api

if __name__ == "__main__":
    app = GoogleApp()
    app.serve()
