# Copyright 2025 Intent Exchange, Inc.
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the “Software”), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

class DataspaceProtocol:
    def __init__(self):
        self.role_permissions = {
            "private": {
                "daia": {"create": True, "read": True, "update": True, "delete": True},
                "deposit": {"create": True, "read": True, "update": False, "delete": False},
                "luggage": {"create": True, "read": True, "update": True, "delete": True},
                "reservation": {"create": True, "read": True, "update": True, "delete": True},
                "transportation": {"create": True, "read": True, "update": True, "delete": True},
                "vehicle": {"create": True, "read": True, "update": True, "delete": True},
            },
            "public": {
                "daia": {"read": True},
                "deposit": {"read": True},
                "luggage": {"read": True},
                "reservation": {"read": True},
                "transportation": {"read": True},
                "vehicle": {"read": True},
            }
        }

    def has_permission(self, role, model, action):
        return self.role_permissions.get(role, {}).get(model, {}).get(action, False)