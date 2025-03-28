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

MOBILITY_HUB_INFO = {
    "4149999900010015":{
        "gln":"4149999900010015",
        "name": "駿河湾沼津",
        "cid": "999990001",
    },
    "4149999900010022":{
        "gln":"4149999900010022",
        "name": "浜松",
        "cid": "999990001",
    },
    "4149999900010039":{
        "gln":"4149999900010039",
        "name": "MH1",
        "cid": "999990001",
    },
    "4149999900010046":{
        "gln":"4149999900010046",
        "name": "MH2",
        "cid": "999990001",
    },
    "4149999900010053":{
        "gln":"4149999900010053",
        "name": "MH3",
        "cid": "999990001",
    },
}

def get_name_by_gln(gln)->str:
    if gln in MOBILITY_HUB_INFO:
        return MOBILITY_HUB_INFO[gln]["name"]
    else:
        return ""