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

import sys
import os
from urllib.parse import urljoin
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.config import Config


class Vanning:
    def search_plan(self, is_departure_mh, trsp_instruction_id, is_vanning):
        url = urljoin(
            Config.MH_MNG_ENDPOINT,
            "plan_search",
        )
        params = {
            "is_departure_mh": is_departure_mh,
            "trsp_instruction_id": trsp_instruction_id,
            "is_vanning": is_vanning,
        }
        response = requests.get(url, params=params, verify=False)
        response.encoding = response.apparent_encoding
        data = response.json()
        plan = None
        if data["result"] is True:
            plan = data["plan"]
        return plan

    def get_plan(self, api, mh, trsp_instruction_id):
        url = urljoin(
            Config.MH_MNG_ENDPOINT,
            f"{api}/{mh}/{trsp_instruction_id}",
        )
        response = requests.get(url, verify=False)
        response.encoding = response.apparent_encoding
        data = response.json()
        plan = None
        if data["result"] is True:
            if api == "devanning_plan":
                plan = data["devanning_plan"]
            elif api == "vanning_plan":
                plan = data["vanning_plan"]
        if plan is None:
            plan = {
                "mh": mh,
                "mh_space_list": [],
                "shipper_cid": "",
                "recipient_cid": "",
                "carrier_cid": "",
                "trsp_instruction_id": trsp_instruction_id,
                "tractor_giai": "",
                "trailer_giai_list": [],
                "req_from_time": "",
                "req_to_time": "",
                "status": 1,
                "is_bl_need": 0,
                "is_departure_mh": 0,
            }
        return plan

    def save_plan(self, api, mh, trsp_instruction_id, plan):
        url = urljoin(
            Config.MH_MNG_ENDPOINT,
            f"{api}/{mh}/{trsp_instruction_id}",
        )
        response = requests.post(url, verify=False, json=plan)
        if response.status_code != 200:
            raise ValueError(f"{api}/{mh}/{trsp_instruction_id} 更新エラー")
        response.encoding = response.apparent_encoding
        data = response.json()
        if data["result"] is False:
            raise ValueError(f"{api}/{mh}/{trsp_instruction_id} 更新失敗")
        return data

    def delete_plan(self, api, mh, trsp_instruction_id):
        url = urljoin(
            Config.MH_MNG_ENDPOINT,
            f"{api}/{mh}/{trsp_instruction_id}",
        )
        response = requests.delete(url, verify=False)
        if response.status_code != 200:
            return False
        else:
            return True
