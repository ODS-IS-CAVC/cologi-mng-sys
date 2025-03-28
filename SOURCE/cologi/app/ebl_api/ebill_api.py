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

from flask_restx import Namespace, Resource, fields
import sys
import os
import logging
import json
from flask import request
import requests
from urllib.parse import urljoin

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from com.helper import create_restx_model_usingSchema, create_response_model
from model.ebl_model import EblJson
from com.company_info import (
    get_recipient_tractor,
    get_address_from_cid,
)
from app.config import Config

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])

ebill_api_ns = Namespace("/ebl/v1", description="EBL 関連API")
parser = ebill_api_ns.parser()


@ebill_api_ns.route("/<string:trsp_instruction_id>/<string:tractor_giai>")
class EBillSearchApi(Resource):

    @ebill_api_ns.doc(description=("B/L取得API<br/>" "- MH（バーコードアプリ）用のAPI"))
    @ebill_api_ns.response(200, "Success")
    @ebill_api_ns.response(400, "HTTP400エラー")
    @ebill_api_ns.response(500, "HTTP500エラー")
    def get(self, trsp_instruction_id, tractor_giai):
        try:
            file_path = os.path.join(
                os.environ.get("EBL_DIR"), f"{trsp_instruction_id}.json"
            )
            ebl = EblJson()
            bl_id = int(ebl.load_file(file_path))
            if bl_id == -1:
                raise ValueError(
                    f"trsp_instruction_id:{trsp_instruction_id}のB/Lは発行されてません"
                )
            logger.debug(f"B/L取得 Start ****  bl_id={bl_id}")
            carrier_cid = ebl.get_issue_user_id()
            recipient_cid = ebl.get_recipient_cid()
            shipper_cid = ebl.get_shipper_cid()
            if tractor_giai != ebl.get_recipient_tractor():
                raise ValueError("トラクターのGIAIが一致してない")
            trailers_giai = ebl.get_trailers_giai()
            ret = {
                "carrier_cid": carrier_cid,
                "recipient_cid": recipient_cid,
                "shipper_cid": shipper_cid,
                "trsp_instruction_id": trsp_instruction_id,
                "tractor_giai": tractor_giai,
                "trailers_giai": trailers_giai,
                "bl_cid": carrier_cid,
                "bl_no": bl_id,
                "bl": ebl.get_ebl(),
            }
            status = 200
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "recipient_cid": "",
                "trsp_instruction_id": trsp_instruction_id,
                "tractor_giai": tractor_giai,
                "trailers_giai": [],
                "bl_cid": "",
                "bl_no": -1,
                "bl": {},
            }
            status = 400
        logger.debug(f"B/L取得 End status ={status} ")
        return ret, status


@ebill_api_ns.route("/bl_check")
class EBillCheckApi(Resource):

    @ebill_api_ns.doc(
        description=("B/LトラストチェックAPI<br/>" "- MH（バーコードアプリ）用のAPI")
    )
    @ebill_api_ns.response(200, "Success")
    @ebill_api_ns.response(400, "HTTP400エラー")
    @ebill_api_ns.response(500, "HTTP500エラー")
    def post(self):
        try:
            file_path = os.path.join(os.environ.get("EBL_DIR"), "EBL_NO_CHECK")
            is_ebl_no_check = os.path.isfile(file_path)
            if is_ebl_no_check:
                logger.debug("******* EBL NO CHECK *******")
                return {"result": True, "err_msg": ""}, 200
            else:
                logger.debug("******* EBL CHECK *******")
            # B/L チェックを行う
            data = request.get_json(force=True)
            logger.debug(f"B/Lトラストチェック data={data}")
            if "recipient_cid" in data:
                recipient_cid = data["recipient_cid"]
            else:
                raise ValueError("recipient_cid missing")
            if "trsp_instruction_id" in data:
                trsp_instruction_id = data["trsp_instruction_id"]
            else:
                ValueError("trsp_instruction_id missing")
            if "tractor_giai" in data:
                tractor_giai = data["tractor_giai"]
            else:
                raise ValueError("tractor_giai missing")
            if "bl_cid" in data:
                bl_cid = data["bl_cid"]
            else:
                raise ValueError("bl_cid missing")
            if "bl_no" in data:
                bl_no = data["bl_no"]
            else:
                raise ValueError("recipienbl_not_cid missing")
            if "bl" in data:
                bl = data["bl"]
            else:
                raise ValueError("bl missing")
            ebl = EblJson()
            ebl.load_json(bl)
            file_path = os.path.join(
                os.environ.get("EBL_DIR"), f"{trsp_instruction_id}.json"
            )
            if os.path.isfile(file_path) is False:
                raise ValueError(f"B/L {file_path}が見つかりません")
            with open(file_path, "r", encoding="utf-8") as f:
                bl_file = json.load(f)
            logger.debug(f"B/L 現在の所有者: {bl_file['current_owner']}/ チェックする所有者: {recipient_cid}")
            if tractor_giai != ebl.get_recipient_tractor():
                raise ValueError(f"トラクターのGIAIが一致してない ebl: {ebl.get_recipient_tractor()}")
            # 電子署名
            url = urljoin(
                Config.TRUST_MNG_ENDPOINT,
                "sign/verify",
            )
            data = {
                "cid": recipient_cid,
                "signature": bl,
            }
            logger.debug(f"bl_no      : {bl_no}")
            logger.debug(f"電子署名検証： {url}")
            logger.debug(f"           ： {data}")
            response = requests.post(
                url,
                json=data,
                verify=False,
            )
            if response.status_code != 200:
                logger.debug(response)
                raise ValueError("電子署名検証失敗")
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"電子署名 response:{data}")
            if data["status"] != "success" or data["isValid"] is False:
                logger.debug(f"電子署名検証エラー:{data}")
                return {"result": False, "err_msg": "SIGN_ERROR"}, 200
            # B/L 検証
            url = urljoin(
                Config.TRUST_MNG_ENDPOINT,
                "bl/verify",
            )
            data = {
                "cid": bl_cid,
                "bl_id": int(bl_no),
                "signed_bl": bl,
            }
            logger.debug(f"B/L 情報検証： {url}")
            logger.debug(f"           ： {data}")
            response = requests.post(
                url,
                json=data,
                verify=False,
            )
            if response.status_code != 200:
                logger.debug(response)
                raise ValueError("B/L 情報検証失敗")
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"B/L 情報検証 response:{data}")
            if data["status"] != "success" or data["result"] is False:
                logger.debug(f"B/L 情報検証エラー:{data}")
                return {"result": False, "err_msg": "INVALID_BL"}, 200
            # B/L 詳細
            url = urljoin(
                Config.TRUST_MNG_ENDPOINT,
                "bl/detail",
            )
            logger.debug(f"B/L 情報詳細： {url}")
            logger.debug(f"           ： bl_id = {bl_no}")
            response = requests.get(
                url,
                params={"bl_id": int(bl_no)},
                verify=False,
            )
            if response.status_code != 200:
                logger.debug(response)
                raise ValueError("B/L 情報詳細失敗")
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"B/L 情報詳細： {data}")
            owner = data["owner"]
            recipient_address = get_address_from_cid(recipient_cid)
            if recipient_address != owner:
                logger.debug(
                    f"B/L オーナーが違う owner:{owner}/ recipient_cid{recipient_cid}"
                )
                return {"result": False, "err_msg": "SIGN_ERROR"}, 200
            if (
                data["status"] != "success"
                or data["invalidate"] is True
                or data["used"] is True
            ):
                logger.debug(f"B/L 情報詳細エラー status:{data}")
                return {"result": False, "err_msg": "USED_BL"}, 200
            # エラー内容は
            # "USED_BL" : 使用済みのＢ／Ｌ
            # "SIGN_ERROR" : 署名が不正
            # "INVALID_BL" : B/Lの改ざんを検出
            return {"result": True, "err_msg": ""}, 200
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            return {"result": False, "err_msg": "PARAM_ERROR"}, 400
