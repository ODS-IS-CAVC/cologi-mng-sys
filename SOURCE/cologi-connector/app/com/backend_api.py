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

import os
import logging
import requests
import json
from urllib.parse import urljoin
from config import ConfigIns

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])


class BackendApi:

    def __init__(self) -> None:
        self.last_error = ""

    def call_api(self, api, method, data=None, param=None, is_shipper= False):
        self.last_error = ""
        if is_shipper:
            url = urljoin(ConfigIns.SHIPPER_BACKEND_ENDPOINT, api)
            logger.debug(f"call_api()->Backend(シッパー): {url}")
        else:
            url = urljoin(ConfigIns.CARRIER_BACKEND_ENDPOINT, api)
            logger.debug(f"call_api()->Backend(キャリア): {url}")
        try:
            headers = {"content-type": "application/json"}
            if ConfigIns.USE_BACKEND_TOKEN:
                headers["Authorization"] = f"Bearer {ConfigIns.BACKEND_TOKEN}"
            response = requests.request(
                method, url, params=param, json=data, headers=headers, verify=False
            )
            if response.status_code != 200:
                logger.error(f"BACKEND ERROR URL {method}:{url}")
                logger.error(f"BACKEND ERROR URL Header:{headers}")
                logger.error(f"BACKEND ERROR URL JSON BODY:{data}")
                logger.error(f"BACKEND ERROR URL Param:{param}")
                logger.error(
                    f"{method} API Error {url} HTTP \n" +
                    f"Status={response.status_code}\n{response.text}"
                )
                try:
                    response.encoding = response.apparent_encoding
                    data = response.json()
                    self.last_error = data["parameters"]["error"]["message"]
                except Exception:
                    self.last_error = "Sorry, can not get Backend error."
                return False
            response.encoding = response.apparent_encoding
            result = response.json()
            # logger.debug(f"Backend API {api}: {json.dumps(result, indent=4)}")
        except Exception as e:
            logging.error("%s", e, exc_info=True)
            result = False
        return result
