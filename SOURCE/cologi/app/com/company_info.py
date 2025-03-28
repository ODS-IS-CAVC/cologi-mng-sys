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

COMPANY_INFOS = {
    "XXXXXXXXXXXXX": {
        "cid": "XXXXXXXXXXXXX",
        "name": "XXXXXXXXXXXXX",
        "role": "carrier",
        "gs1": "XXXXXXXXXXXXX",
        "endpoint": "http://XXXXXXXXXXXXX/public/api/",
        "wallet_adress": "XXXXXXXXXXXXX",
        "tractor": "-",
    },
    "XXXXXXXXXXXXX": {
        "cid": "XXXXXXXXXXXXX",
        "name": "荷主1",
        "role": "shipper",
        "gs1": "XXXXXXXXXXXXX",
        "endpoint": "http://XXXXXXXXXXX/public/api/",
        "wallet_adress": "XXXXXXXXXXXXX",
        "tractor": "XXXXXXXXXXXXX",
    },
    "XXXXXXXXXXXXX": {
        "cid": "XXXXXXXXXXXXX",
        "name": "荷受人1",
        "role": "recipient",
        "gs1": "XXXXXXXXXXXXX",
        "endpoint": "http://XXXXXXXXXXXXX/public/api/",
        "wallet_adress": "XXXXXXXXXXXXX",
        "tractor": "XXXXXXXXXXXXX",
    },
}


def get_endpoint_from_cid(cid: str) -> str:
    if cid in COMPANY_INFOS:
        return COMPANY_INFOS[cid]["endpoint"]
    else:
        return None


def get_name_from_cid(cid: str) -> str:
    if cid in COMPANY_INFOS:
        return COMPANY_INFOS[cid]["name"]
    else:
        return ""


def get_address_from_cid(cid: str) -> str:
    if cid in COMPANY_INFOS:
        return COMPANY_INFOS[cid]["wallet_adress"]
    else:
        return None


def get_shipper_tractor(cid: str) -> str:
    if cid in COMPANY_INFOS:
        return COMPANY_INFOS[cid]["tractor"]
    else:
        return None


def get_recipient_tractor(cid: str) -> str:
    if cid in COMPANY_INFOS:
        return COMPANY_INFOS[cid]["tractor"]
    else:
        return None
