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
import requests
import json
from dateutil import parser
from urllib.parse import urljoin
from flask import request

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from com.helper import create_restx_model_usingSchema, create_response_model
from model.ebl_model import EblJson
from app.config import Config
from com.company_info import get_address_from_cid, get_endpoint_from_cid

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])

vanning_api_ns = Namespace("/cbapi/v1", description="バンニング/デバンニングCB 関連API")


def check_data(data):
    if "EPCISQueryDocument" not in data:
        raise ValueError("EPCISQueryDocumentがありません")
    epic_doc = data["EPCISQueryDocument"]
    if "EPCISBody" not in epic_doc:
        raise ValueError("EPCISBodyがありません")
    epic_body = epic_doc["EPCISBody"]
    if "resultsBody" not in epic_body:
        raise ValueError("resultsBodyがありません")
    result_body = epic_body["resultsBody"]
    result = []
    for r in result_body:
        param_check = [
            "eventTime",
            "childEPCs",
            "readPoint",
            "bizLocation",
            "custom:planId",
            "bizStep",
        ]
        for p in param_check:
            if p not in r:
                raise ValueError(f"{p}がありません")
        tmp = r["bizLocation"]["id"].split("urn:epc:id:sgln:")
        if len(tmp) != 2:
            raise ValueError(
                "bizLocationのフォーマットはurn:epc:id:sgln:XXXXXXXXXXXXです"
                + f"bizLocation= {r['bizLocation']['id']}"
            )
        mh = tmp[1]

        mh_space_list = []
        tmp = (r["readPoint"]["id"]).split(r["bizLocation"]["id"] + ".")
        if len(tmp) != 2:
            raise ValueError(
                "readPointのフォーマットはurn:epc:id:sgln:XXXXXXXXXXXX.nnnです"
                + f"bizLocation= {r['bizLocation']['id']}"
                + f"/readPoint= {r['readPoint']['id']}"
            )
        mh_space_list.append(tmp[1])
        trsp_instruction_id = r["custom:planId"]
        actual_to_time = r["eventTime"]
        giai_list = [epc.split("urn:epc:id:giai:")[1] for epc in r["childEPCs"]]
        logger.debug(
            f"mh={mh}/mh_space={mh_space_list}/"
            + f"trsp_instruction_id={trsp_instruction_id}/"
            + f"actual_to_time={actual_to_time}/giai_list={giai_list}"
        )
        result.append(
            {
                "mh": mh,
                "mh_space": mh_space_list,
                "trsp_instruction_id": trsp_instruction_id,
                "actual_to_time": actual_to_time,
                "giai_list": giai_list,
                "biz_step": r["bizStep"],
            }
        )
    return result


def get_mh_data(mh, trsp_instruction_id, is_vanning):
    try:
        if is_vanning:
            url = urljoin(
                Config.MH_MNG_ENDPOINT, f"vanning_plan/{mh}/{trsp_instruction_id}"
            )
        else:
            url = urljoin(
                Config.MH_MNG_ENDPOINT, f"devanning_plan/{mh}/{trsp_instruction_id}"
            )
        response = requests.get(
            url,
            verify=False,
        )
        if response.status_code != 200:
            logger.debug(response.json())
            raise ValueError(f"Status Code = {response.status_code}")
        response.encoding = response.apparent_encoding
        data = response.json()
        if data["result"] is False:
            raise ValueError(data["error_msg"])
        return data
    except Exception as e:
        raise ValueError(f"MH CONNECT ERROR {e}")


def update_plan(result, plan, is_vanning=True):
    # チェックGIAI
    for giai in result["giai_list"]:
        if giai == plan["tractor_giai"]:
            continue
        if giai in plan["trailer_giai_list"]:
            continue
        raise ValueError(f"{giai} は計画にありません")
    # 状態(idle(0),planning(1),done(2),cancel(-1))
    status = plan["status"]
    trsp_instruction_id = result["trsp_instruction_id"]
    mh = result["mh"]
    # 今年度は複数トレーラーの矛盾チェックを行わない
    # if status == 2:
    #     raise ValueError(f"{trsp_instruction_id} は実行済みです")
    if status == -1:
        raise ValueError(f"{trsp_instruction_id} はキャンセル済みです")
    plan["status"] = 2  # Done
    d = parser.parse(result["actual_to_time"])
    plan["actual_time"] = d.strftime("%Y-%m-%dT%H:%M:%S")
    logger.debug(f"MH UPDATE: {plan}")
    try:
        if is_vanning:
            url = urljoin(
                Config.MH_MNG_ENDPOINT, f"vanning_plan/{mh}/{trsp_instruction_id}"
            )
        else:
            url = urljoin(
                Config.MH_MNG_ENDPOINT, f"devanning_plan/{mh}/{trsp_instruction_id}"
            )
        response = requests.put(
            url,
            json=plan,
            verify=False,
        )
        if response.status_code != 200:
            raise ValueError(f"Status Code = {response.status_code}")
        return plan
    except Exception as e:
        raise ValueError(f"MH CONNECT ERROR {e}")


@vanning_api_ns.route("vanning_result")
class CBVanningResultApi(Resource):

    @vanning_api_ns.doc(
        description=("バンニング結果通知用CB API<br/>" "- トレーサビリティ用のAPI")
    )
    @vanning_api_ns.response(200, "Success")
    @vanning_api_ns.response(400, "HTTP400エラー")
    @vanning_api_ns.response(500, "HTTP500エラー")
    def post(self):
        try:
            data = request.get_json()
            logger.debug(f"バンニング結果通知用CB API POST start:{data}")
            result = check_data(data)
            for r in result:
                trsp_instruction_id = r["trsp_instruction_id"]
                biz_step = r["biz_step"]
                if biz_step == "loading":
                    is_vanning = True
                elif biz_step == "unloading":
                    is_vanning = False
                else:
                    continue
                mh_data = get_mh_data(
                    r["mh"], trsp_instruction_id, is_vanning=is_vanning
                )
                logger.debug(f"バンニング結果通知用CB MH DATA:{mh_data}")
                plan = (
                    mh_data["vanning_plan"] if is_vanning else mh_data["devanning_plan"]
                )
                if int(plan["is_bl_need"]) == 1 and plan["status"] == 1:
                    #  着MHのバンニングの場合にはE/Lを使用済みにする
                    file_path = os.path.join(
                        os.environ.get("EBL_DIR"), f"{trsp_instruction_id}.json"
                    )
                    if os.path.isfile(file_path) is False:
                        raise ValueError(f"B/L {file_path}が見つかりません")
                    ebl = EblJson()
                    bl_id = ebl.load_file(file_path)
                    recipient_cid = ebl.get_recipient_cid()
                    url = urljoin(
                        Config.TRUST_MNG_ENDPOINT,
                        "bl/used",
                    )
                    data = {
                        "cid": recipient_cid,
                        "bl_id": bl_id,
                    }
                    logger.debug(f"バンニング結果通知用CB B/L 情報使用済み： {url}")
                    logger.debug(f"                                    ： {data}")
                    response = requests.post(
                        url,
                        json=data,
                        verify=False,
                    )
                    if response.status_code != 200:
                        logger.debug(response)
                        # 今年度は2回呼ばれることがあるので
                        # エラーは無視 raise ValueError("B/L 情報使用済み失敗")
                    response.encoding = response.apparent_encoding
                    data = response.json()
                    logger.debug(f"バンニング結果通知用CB B/L 情報使用済結果： {data}")
                plan = update_plan(r, plan, is_vanning=is_vanning)
            ret = {"result": True, "err_msg": "", "updated_plan": plan}
            status = 200
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "err_msg": str(e),
                "updated_plan": None,
            }
            status = 400
            plan = {}
        logger.debug(f"バンニング結果通知用CB API POST END plan={plan}/ status = {status}")
        return ret, status


@vanning_api_ns.route("devanning_result")
class CBDevanningResultApi(Resource):

    @vanning_api_ns.doc(
        description=("デバンニング結果通知用CB API<br/>" "- トレーサビリティ用のAPI")
    )
    @vanning_api_ns.response(200, "Success")
    @vanning_api_ns.response(400, "HTTP400エラー")
    @vanning_api_ns.response(500, "HTTP500エラー")
    def post(self):
        try:
            data = request.get_json()
            logger.debug(f"デバンニング結果通知用CB Start data={data}")
            result = check_data(data)
            for r in result:
                trsp_instruction_id = r["trsp_instruction_id"]
                mh_data = get_mh_data(r["mh"], trsp_instruction_id, is_vanning=False)
                logger.debug(f"デバンニング結果通知用CB MH DATA:{mh_data}")
                devanning_plan = mh_data["devanning_plan"]
                # 発MHのデバンニングの実施の際にEBLをキャリアから荷主に移動する
                # 状態がplanning(1)物だけ対象
                if (
                    int(devanning_plan["is_departure_mh"]) == 1
                    and int(devanning_plan["status"]) == 1
                ):
                    file_path = os.path.join(
                        os.environ.get("EBL_DIR"), f"{trsp_instruction_id}.json"
                    )
                    if os.path.isfile(file_path) is False:
                        raise ValueError(f"B/L {file_path}が見つかりません")
                    with open(file_path, "r", encoding="utf-8") as f:
                        bl_file = json.load(f)
                    current_owner = bl_file.get("current_owner", "")
                    if current_owner == devanning_plan["carrier_cid"]:
                        # 荷主からB/Lを取得(発行)
                        logger.debug("デバンニング結果通知用CB BL発行")
                        self.get_bl(
                            trsp_instruction_id,
                            devanning_plan["shipper_cid"],
                            devanning_plan["recipient_cid"],
                            devanning_plan["carrier_cid"],
                        )
                        logger.debug("デバンニング結果通知用CB BL 荷主→荷受移動申請")
                        # まず荷主として受領し、荷受け人に移動
                        self.save_bl(
                            trsp_instruction_id,
                            devanning_plan["shipper_cid"],
                            devanning_plan["recipient_cid"],
                        )
                        # 荷受け人として受領
                        self.save_bl(trsp_instruction_id, devanning_plan["recipient_cid"])
                        logger.debug(f"デバンニング結果通知用CB BL 荷受人受領成功 current_owner = {devanning_plan['recipient_cid']}")
                    else:
                        logger.debug(f"デバンニング結果通知用CB BL 移転済み current_owner = {current_owner}")
                else:
                    logger.debug("デバンニング結果通知用CB BL処理不要")
                updated_plan = update_plan(r, devanning_plan, is_vanning=False)
            ret = {"result": True, "err_msg": "", "updated_plan": updated_plan}
            status = 200
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "err_msg": str(e),
                "updated_plan": None,
            }
            status = 400
            updated_plan = {}
        logger.debug(f"デバンニング結果通知用CB updated_plan={updated_plan} / status ={status}")
        return ret, status

    def get_bl(self, trsp_instruction_id, shipper_cid, recipient_cid, carrier_cid):
        url = urljoin(
            Config.CONNECTOR_PRIVATE_ENDPOINT,
            f"ebl/{trsp_instruction_id}",
        )
        query_params = {
            "recipient_cid": recipient_cid,
            "shipper_cid": shipper_cid,
        }
        endpoint = get_endpoint_from_cid(carrier_cid)
        logger.debug(f"CONNECT cid:{url} / {endpoint}/ {query_params}")
        headers = {"X-ENDPOINT": endpoint}
        response = requests.get(
            url,
            params=query_params,
            verify=False,
            proxies={"no_proxy": "co_logi_connector"},
            headers=headers,
        )
        if response.status_code == 403:
            raise LookupError(
                f"EBL が見つからない trsp_instruction_id={trsp_instruction_id}"
            )
        if response.status_code != 200:
            raise ValueError(f"EBL エラー trsp_instruction_id={trsp_instruction_id}")
        response.encoding = response.apparent_encoding
        data = response.json()
        logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
        if data["result"] is False:
            raise ValueError(f"EBL 失敗 trsp_instruction_id={trsp_instruction_id}")
        return data

    def save_bl(self, trsp_instruction_id, cid, to_cid=None):
        file_path = os.path.join(
            os.environ.get("EBL_DIR"), f"{trsp_instruction_id}.json"
        )
        if os.path.isfile(file_path) is False:
            raise ValueError(f"B/L {file_path}が見つかりません")
        with open(file_path, "r", encoding="utf-8") as f:
            bl_file = json.load(f)
        if "signed_bl" not in bl_file:
            raise ValueError("B/Lにsigned_blがありません")
        if "bl_id" not in bl_file:
            raise ValueError("B/Lにbl_idがありません")
        signed_bl = bl_file["signed_bl"]
        bl_id = int(bl_file["bl_id"])
        current_owner = bl_file.get("current_owner", "")
        logger.debug(f"B/L current_owner = {current_owner}")
        if current_owner != cid and current_owner != to_cid:
            url = urljoin(
                Config.TRUST_MNG_ENDPOINT,
                "bl/approve",
            )
            data = {
                "cid": cid,
                "bl_id": bl_id,
                "signed_bl": signed_bl,
            }
            logger.debug(f"B/L 受領承認： {url}")
            logger.debug(f"           ： {data}")
            response = requests.post(
                url,
                json=data,
                verify=False,
            )
            if response.status_code != 200:
                logger.debug(response)
                raise ValueError("B/L 受領失敗")
            # 新しい署名のB/Lを保存
            response.encoding = response.apparent_encoding
            bl_reg = response.json()
            signed_bl = bl_reg.get("signed_signed_bl")
            bl_file = {
                "signed_bl": signed_bl,
                "bl_id": bl_id,
                "current_owner": cid,
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(bl_file, f, indent=4, ensure_ascii=False)
            logger.debug(f"save New EBL for shipper {file_path}")
            logger.debug(signed_bl)
            if to_cid is None:
                return
            current_owner = cid
        else:
            logger.debug(f"キャリア→荷主 B/Lの所有権はすでに {to_cid} に移ってます")

        if current_owner != to_cid and to_cid is not None:
            # 荷主→荷受け人へ移動のケース
            to_address = get_address_from_cid(to_cid)
            url = urljoin(
                Config.TRUST_MNG_ENDPOINT,
                "bl/transfer",
            )
            data = {
                "cid": cid,
                "bl_id": bl_id,
                "to_address": to_address,
            }
            logger.debug(f"B/L 移転申請： {url}")
            logger.debug(f"        ： {data}")
            response = requests.post(
                url,
                json=data,
                verify=False,
            )
            logger.debug(f"Response Code: {response.status_code}")
            if response.status_code != 200:
                logger.debug(response)
                raise ValueError("トラスト基盤 BL移転申請 ERROR")
            response.encoding = response.apparent_encoding
            data = response.json()
            if data["result"] is False:
                raise ValueError(f"トラスト基盤 BL移転申請 result {data}")
            bl_file = {
                "signed_bl": signed_bl,
                "bl_id": bl_id,
                "current_owner": cid,
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(bl_file, f, indent=4, ensure_ascii=False)
            logger.debug(f"save EBL {file_path}")
        else:
            logger.debug(f"荷主→荷受け人 B/Lの所有権はすでに {to_cid} に移ってます")
