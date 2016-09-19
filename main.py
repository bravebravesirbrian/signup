#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import re
import cgi

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
</head>
<body>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

signup_form = """
<form action="/user_info" method="post">
    <b>Username:</b>
    <label>
        <input type="text" name="username">
    </label>
    <br>
    <b>Password:</b>
    <label>
        <input type="password" name="password">
    </label>
    <br>
    <b>Verify Password:</b>
    <label>
        <input type="password" name="verify">
    </label>
    <br>
    <b>Email(optional):</b>
    <label>
        <input type="text" name="email">
    </label>
    <br>
    <input type="submit" value="Enter"/>
</form>
"""
class MainHandler(webapp2.RequestHandler):
    """Handles requests coming in to '/' (the root of the site)
    """

    def get(self):
        self.response.write(page_header + signup_form)

class User_InfoHandler(webapp2.RequestHandler):
    """Handles requests coing in to '/user_info'
    """

    def post(self):

        error_user = "<div>Please enter a valid username.</div>"
        error_pass1 = "<div>Please enter a valid password.</div>"
        error_pass2 = "<div>Please confirm your password.</div>"
        error_address = "<div>Please enter a valid email address.</div>"

        user_name = self.request.get("username")
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        number_errors = 0
        def valid_user_name(username):
            return USER_RE.match(username)
        if valid_user_name(user_name):
            error_user = ""
        else:
            number_errors += 1

        password1 = self.request.get("password")
        PASS_RE = re.compile(r"^.{3,20}$")
        def valid_password(password):
            return PASS_RE.match(password)
        if valid_password(password1):
            error_pass1 = ""
        else:
            number_errors += 1

        password2 = self.request.get("verify")
        if password1 == password2:
            error_pass2 = ""
        else:
            number_errors += 1

        email_address = self.request.get("email")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]$")
        def valid_email(email):
            return EMAIL_RE.match(email)
        if valid_email(email_address):
            error_address = ""
        elif email_address == "":
            error_address = ""
        else:
            number_errors += 1

        signup_form = """
        <form action="/user_info" method="post">
            <b>Username:</b>
            <label>
                <input type="text" name="username">{0}
            </label>
            <br>
            <b>Password:</b>
            <label>
                <input type="password" name="password">{1}
            </label>
            <br>
            <b>Verify Password:</b>
            <label>
                <input type="password" name="verify">{2}
            </label>
            <br>
            <b>Email(optional):</b>
            <label>
                <input type="text" name="email">{3}
            </label>
            <br>
                <input type="submit" value="Enter"/>
            </form>
            """.format(error_user, error_pass1, error_pass2, error_address)

        if number_errors == 0:
            self.response.write("<h1>Welcome, " + user_name + "!</h1>" + page_footer)
        else:
            self.response.write(page_header + signup_form)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/user_info', User_InfoHandler)
], debug=True)
