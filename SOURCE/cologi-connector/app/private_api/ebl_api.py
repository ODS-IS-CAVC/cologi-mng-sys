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

from flask_restx import Namespace, Resource
import os
from flask import request
import requests
from urllib.parse import urljoin
import json
import logging

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])


ebl_api_ns = Namespace("/private/api/ebl", description="eBL関係API")


@ebl_api_ns.route("/<string:trsp_instruction_id>")
@ebl_api_ns.param("trsp_instruction_id", "運送依頼番号")
class EblApi(Resource):

    @ebl_api_ns.doc(
        description=(
            "API-080 B/L取得API<br/>"
            "- デマンド・サイドからサプライサイドに対してのみ利用可"
        ),
    )
    def get(self, trsp_instruction_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(
            endpoint,
            f"ebl/{trsp_instruction_id}",
        )
        try:
            logger.debug(f"CONNECT:{url}")
            response = requests.get(
                url,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "localhost"},
            )
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
            if response.status_code != 200:
                if response.status_code == 403:
                    raise LookupError("EBL が見つかりません")
                else:
                    raise ValueError("EBL エラー")
            if data["result"] is False:
                raise ValueError("EBL 失敗")
            ret = data
            status = 200
        except LookupError as e:
            logger.error("EBLが見つかりません")
            ret = {
                "result": False,
                "err_msg": str(e.args[0]),
                "carrier_cid": "",
                "recipient_cid": "",
                "shipper_cid": "",
                "trsp_instruction_id": trsp_instruction_id,
                "bl_no": -1,
                "bl": "",
            }
            status = 403
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "err_msg": str(e.args[0]),
                "carrier_cid": "",
                "recipient_cid": "",
                "shipper_cid": "",
                "trsp_instruction_id": trsp_instruction_id,
                "bl_no": -1,
                "bl": "",
            }
            status = 400
        return ret, status
