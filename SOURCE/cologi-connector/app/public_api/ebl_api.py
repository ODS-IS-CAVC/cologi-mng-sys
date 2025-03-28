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
import sys
import os
from flask import request
import requests
from urllib.parse import urljoin
import logging

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from model.ebl_model import EblJson
from app.config import Config
from com.company_info import (
    get_address_from_cid,
)

ebl_api_ns = Namespace("/public/api/ebl", description="eBL関係API")


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
        try:
            query_params = request.args.to_dict()
            logger.debug(f"API-080 B/L取得API query_params = {query_params}")
            recipient_cid = query_params.get("recipient_cid", None)
            shipper_cid = query_params.get("shipper_cid", None)
            file_path = os.path.join(
                os.environ.get("EBL_DIR"), f"{trsp_instruction_id}.json"
            )
            ebl = EblJson()
            bl_id = int(ebl.load_file(file_path))
            if bl_id == -1:
                raise LookupError(
                    f"trsp_instruction_id:{trsp_instruction_id}のB/Lは発行されてません"
                )
            ebl_carrier_cid = ebl.get_issue_user_id()
            ebl_recipient_cid = ebl.get_recipient_cid()
            ebl_shipper_cid = ebl.get_shipper_cid()
            if ebl_recipient_cid != recipient_cid or ebl_shipper_cid != shipper_cid:
                raise ValueError(
                    f"{trsp_instruction_id} のB/Lを {recipient_cid}/ {shipper_cid}に移動できません"
                )
            # B/L を荷主に移動
            to_address = get_address_from_cid(shipper_cid)
            url = urljoin(
                Config.TRUST_MNG_ENDPOINT,
                "bl/transfer",
            )
            data = {
                "cid": ebl_carrier_cid,
                "bl_id": bl_id,
                "to_address": to_address,
            }
            logger.debug(f"API-080 B/L取得API B/L 移転申請： {url}")
            logger.debug(f"        ： {data}")
            response = requests.post(
                url,
                json=data,
                verify=False,
            )
            logger.debug(f"API-080 B/L取得API Response Code: {response.status_code}")
            if response.status_code != 200:
                logger.debug(response)
                raise ValueError("トラスト基盤 BL移転申請 ERROR")
            response.encoding = response.apparent_encoding
            data = response.json()
            if data["result"] is False:
                raise ValueError(f"トラスト基盤 BL移転申請 result {data}")
            ret = {
                "result": True,
                "carrier_cid": ebl_carrier_cid,
                "recipient_cid": recipient_cid,
                "shipper_cid": shipper_cid,
                "trsp_instruction_id": trsp_instruction_id,
                "bl_no": bl_id,
                "bl": ebl.get_ebl(),
            }
            status = 200
        except LookupError as e:
            logger.error("API-080 B/L取得API B/Lが見つかりません")
            ret = {
                "result": False,
                "err_msg": str(e.args[0]),
                "carrier_cid": "",
                "recipient_cid": recipient_cid,
                "shipper_cid": shipper_cid,
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
                "recipient_cid": recipient_cid,
                "shipper_cid": shipper_cid,
                "trsp_instruction_id": trsp_instruction_id,
                "bl_no": -1,
                "bl": "",
            }
            status = 400
        return ret, status
