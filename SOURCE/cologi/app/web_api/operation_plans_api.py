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
from flask import request
import requests
from urllib.parse import urljoin
import logging
import json
import dateutil.parser

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from com.helper import (
    create_restx_model_usingSchema,
    create_response_model,
)
from model.operation_plan_model import OperationPlanSchema
from model.model_5001.trsp_ability_line_item_model import TrspAbilityLineItemSchema
from model.model_3012_operation.trsp_plan_line_item_model import TrspPlanLineItemSchema
from model.model_3012_operation.trsp_plan_model import TrspPlanSchema
from model.model_3012_operation.msg_info_model import MsgInfoSchema
from model.ebl_model import EblJson
from app.config import Config
from com.company_info import (
    get_endpoint_from_cid,
    get_address_from_cid,
    get_name_from_cid,
    COMPANY_INFOS,
)
from com.vanning import Vanning


operation_plans_api_ns = Namespace("/webapi/v1/operation_plans", description="運行計画")

parser = operation_plans_api_ns.parser()
parser.add_argument("q", type=str, help="クエリ文字列", required=False, location="args")
parser.add_argument(
    "o", type=int, help="オフセット", default=0, required=False, location="args"
)
parser.add_argument(
    "n", type=int, help="取得数", default=100, required=False, location="args"
)
id_parser = operation_plans_api_ns.parser()
id_parser.add_argument("cid", type=str, help="事業者ID", required=True, location="args")

def update_devanning_vanning_plan(
    trsp_instruction_id,
    shipper_cid,
    carrier_cid,
    departure_mh,
    departure_mh_space_list,
    arrival_mh,
    arrival_mh_space_list,
    tractor_giai,
    dep_req_from_time,
    dep_req_to_time,
    arv_req_from_time,
    arv_req_to_time,
):
    # 前の情報があれば取得、無ければ初期データ取得
    vanning = Vanning()
    ## 出発MH
    dep_devanning_plan = vanning.get_plan(
        "devanning_plan", departure_mh, trsp_instruction_id
    )
    dep_vanning_plan = vanning.get_plan(
        "vanning_plan", departure_mh, trsp_instruction_id
    )
    ## 到着MH
    arv_devanning_plan = vanning.get_plan(
        "devanning_plan", arrival_mh, trsp_instruction_id
    )
    arv_vanning_plan = vanning.get_plan(
        "vanning_plan", arrival_mh, trsp_instruction_id
    )
    # 必要なデータの更新
    ## 出発MH
    ### 時間の算出
    dep_van_from_datetime = dateutil.parser.parse(dep_req_from_time)
    dep_van_to_datetime = dateutil.parser.parse(dep_req_to_time)
    ### データ
    dep_devanning_plan["mh"] = departure_mh
    dep_vanning_plan["mh"] = departure_mh
    dep_devanning_plan["mh_space_list"] = departure_mh_space_list
    dep_vanning_plan["mh_space_list"] = departure_mh_space_list
    dep_devanning_plan["carrier_cid"] = carrier_cid
    dep_vanning_plan["carrier_cid"] = carrier_cid
    dep_devanning_plan["trsp_instruction_id"] = trsp_instruction_id
    dep_vanning_plan["trsp_instruction_id"] = trsp_instruction_id
    dep_devanning_plan["status"] = 1
    dep_vanning_plan["status"] = 1
    dep_devanning_plan["is_bl_need"] = 0
    dep_vanning_plan["is_bl_need"] = 0
    dep_devanning_plan["is_departure_mh"] = 1
    dep_vanning_plan["is_departure_mh"] = 1
    dep_devanning_plan["shipper_cid"] = shipper_cid
    dep_vanning_plan["shipper_cid"] = shipper_cid
    # キャリアのデータなので発MHはバンニングのみ
    dep_vanning_plan["req_from_time"] = dep_van_from_datetime.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    dep_vanning_plan["req_to_time"] = dep_van_to_datetime.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    dep_vanning_plan["tractor_giai"] = tractor_giai

    ## 到着MH
    ### 時間の算出
    aped_devan_from_datetime = dateutil.parser.parse(arv_req_from_time)
    aped_devan_to_datetime = dateutil.parser.parse(arv_req_to_time)
    ### データ
    arv_devanning_plan["mh"] = arrival_mh
    arv_vanning_plan["mh"] = arrival_mh
    arv_devanning_plan["mh_space_list"] = arrival_mh_space_list
    arv_vanning_plan["mh_space_list"] = arrival_mh_space_list
    arv_devanning_plan["carrier_cid"] = carrier_cid
    arv_vanning_plan["carrier_cid"] = carrier_cid
    arv_devanning_plan["trsp_instruction_id"] = trsp_instruction_id
    arv_vanning_plan["trsp_instruction_id"] = trsp_instruction_id
    arv_devanning_plan["status"] = 1
    arv_vanning_plan["status"] = 1
    arv_devanning_plan["is_bl_need"] = 0
    arv_vanning_plan["is_bl_need"] = 1
    arv_devanning_plan["is_departure_mh"] = 0
    arv_vanning_plan["is_departure_mh"] = 0
    arv_devanning_plan["shipper_cid"] = shipper_cid
    arv_vanning_plan["shipper_cid"] = shipper_cid
    # キャリアのデータなので着MHはデバンニングのみ
    arv_devanning_plan["req_from_time"] = aped_devan_from_datetime.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    arv_devanning_plan["req_to_time"] = aped_devan_to_datetime.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    arv_devanning_plan["tractor_giai"] = tractor_giai
    # 更新したデータを保存
    ## 出発MH
    vanning.save_plan(
        "devanning_plan", departure_mh, trsp_instruction_id, dep_devanning_plan
    )
    vanning.save_plan(
        "vanning_plan", departure_mh, trsp_instruction_id, dep_vanning_plan
    )
    ## 到着MH
    vanning.save_plan(
        "devanning_plan", arrival_mh, trsp_instruction_id, arv_devanning_plan
    )
    vanning.save_plan(
        "vanning_plan", arrival_mh, trsp_instruction_id, arv_vanning_plan
    )


@operation_plans_api_ns.route("/<string:operation_id>")
@operation_plans_api_ns.param("operation_id", "運行計画ID")
class OperationPlansApi(Resource):
    post_request_model = create_restx_model_usingSchema(
        "OperationPlanDataUpdateRequestModel",
        operation_plans_api_ns,
        OperationPlanSchema,
        exclude_fields=["id"],
    )
    post_response_data = operation_plans_api_ns.clone(
        "OperationPlanDataUpdateResponseData",
        post_request_model,
        {
            "trsp_instruction_id": fields.String(
                example="12345678901234567890",
                description="運送依頼番号",
                required=True,
            ),
            "shipper_cid": fields.String(
                example="490000001", description="依頼元の事業者ID", required=True
            ),
            "carrier_cid": fields.String(
                example="490000002",
                description="依頼先(申し込みを受ける側・回答する側)の事業者ID",
                required=True,
            ),
            "departure_mh": fields.String(
                example="490000000100", description="出発MHのGLN", required=True
            ),
            "departure_mh_space_list": fields.String(
                example="1", description="出発MHの駐車枠の配列", required=True
            ),
            "arrival_mh": fields.String(
                example="490000000200", description="到着MHのGLN", required=True
            ),
            "arrival_mh_space_list": fields.String(
                example="2", description="到着MHの駐車枠の配列", required=True
            ),
            "tractor_giai": fields.String(
                example="8004990000001000000000000000000001",
                description="トラクターのGIAI",
                required=True,
            ),
            "req_from_time": fields.String(
                example="2015-01-02 13:00:00",
                description="MH作業希望時間(From)",
                required=True,
            ),
            "req_to_time": fields.String(
                example="2015-01-02 13:10:00",
                description="MH作業希望時間(To)",
                required=True,
            ),
        },
    )
    post_response_model = create_response_model(
        "OperationPlanDataUpdateResponseModel",
        operation_plans_api_ns,
        "operation_plans",
        post_response_data,
    )

    @operation_plans_api_ns.doc(
        description=("API-042 運行計画更新 <br/>" "- サプライ・サイドからのみ利用可"),
        params={
            "trsp_instruction_id": "trsp_instruction_id(required)",
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "departure_mh": "出発MHのGLN(required)",
            "departure_mh_space_list": "出発MHの駐車枠の配列(required)",
            "arrival_mh": "到着MHのGLN(required)",
            "arrival_mh_space_list": "到着MHの駐車枠の配列(required)",
            "tractor_giai": "トラクターのGIAI(required)",
            "req_from_time": "MH作業希望時間(From)(required)",
            "req_to_time": "MH作業希望時間(To)(required)",
        },
    )
    def put(self, operation_id):
        query_params = request.args.to_dict()
        logger.debug(f"API-042 運行計画更新 Start query_params={query_params}")
        try:
            no_key = []
            for key in [
                "trsp_instruction_id",
                "shipper_cid",
                "carrier_cid",
                "departure_mh",
                "departure_mh_space_list",
                "arrival_mh",
                "arrival_mh_space_list",
                "tractor_giai",
                "dep_req_from_time",
                "dep_req_to_time",
                "arv_req_from_time",
                "arv_req_to_time",
            ]:
                if key not in query_params:
                    no_key.append(key)
            if len(no_key) > 0:
                no_keys = ",".join(no_key)
                raise ValueError(f"Parameters missing:{no_keys}")
            for p in [
                "shipper_cid",
                "carrier_cid",
            ]:
                if query_params[p] not in COMPANY_INFOS:
                    raise ValueError(f"{p}:{query_params[p]} is not valid cid.")
            trsp_instruction_id = query_params["trsp_instruction_id"]
            shipper_cid = query_params["shipper_cid"]
            carrier_cid = query_params["carrier_cid"]
            departure_mh = query_params["departure_mh"]
            departure_mh_space_list = query_params["departure_mh_space_list"].split(",")
            arrival_mh = query_params["arrival_mh"]
            arrival_mh_space_list = query_params["arrival_mh_space_list"].split(",")
            tractor_giai = query_params["tractor_giai"]
            dep_req_from_time = query_params["dep_req_from_time"]
            dep_req_to_time = query_params["dep_req_to_time"]
            arv_req_from_time = query_params["arv_req_from_time"]
            arv_req_to_time = query_params["arv_req_to_time"]
            logger.debug(f"API-042 運行計画更新 CID:{shipper_cid}")
            data = request.get_json()
            logger.debug(f"API-042 運行計画更新 data={data}")
            # バンニング、デバンニング計画更新
            update_devanning_vanning_plan(
                trsp_instruction_id,
                shipper_cid,
                carrier_cid,
                departure_mh,
                departure_mh_space_list,
                arrival_mh,
                arrival_mh_space_list,
                tractor_giai,
                dep_req_from_time,
                dep_req_to_time,
                arv_req_from_time,
                arv_req_to_time,
            )
            ret = {
                "operation_plans": {
                    "trsp_instruction_id": trsp_instruction_id,
                    "shipper_cid": shipper_cid,
                    "carrier_cid": carrier_cid,
                    "departure_mh": departure_mh,
                    "departure_mh_space_list": departure_mh_space_list,
                    "arrival_mh": arrival_mh,
                    "arrival_mh_space_list": arrival_mh_space_list,
                    "tractor_giai": tractor_giai,
                    "dep_req_from_time": dep_req_from_time,
                    "dep_req_to_time": dep_req_to_time,
                    "arv_req_from_time": arv_req_from_time,
                    "arv_req_to_time": arv_req_to_time,
                },
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {"operation_plans": {}, "result": False, "error_msg": "error"}
            status = 400
        except Exception as e:
            logger.debug(
                f"API-042 運行計画更新: {e.args[0]}", exc_info=True, stack_info=True
            )
            ret = {
                "operation_plans": {},
                "result": False,
                "error_msg": str(e.args[0]),
            }
            status = 500
        logger.debug(f"API-042 運行計画更新 End Status={status}")
        return ret, status


@operation_plans_api_ns.route("/")
class OperationPlansListApi(Resource):
    @operation_plans_api_ns.doc(
        description=(
            "API-040 運行計画登録（車両割付）<br/>" "- サプライ・サイドからのみ利用可"
        ),
        params={
            "trsp_instruction_id": "trsp_instruction_id(required)",
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "departure_mh": "出発MHのGLN(required)",
            "departure_mh_space_list": "出発MHの駐車枠の配列(required)",
            "arrival_mh": "到着MHのGLN(required)",
            "arrival_mh_space_list": "到着MHの駐車枠の配列(required)",
            "tractor_giai": "トラクターのGIAI(required)",
            "dep_req_from_time": "発MH作業希望時間(From)(required)",
            "dep_req_to_time": "発MH作業希望時間(To)(required)",
            "arv_req_from_time": "着MH作業希望時間(From)(required)",
            "arv_req_to_time": "着MH作業希望時間(To)(required)",
        },
    )
    def post(self):
        query_params = request.args.to_dict()
        logger.debug(f"API-040 運行計画登録（車両割付）Start query_params={query_params}")
        try:
            no_key = []
            for key in [
                "trsp_instruction_id",
                "shipper_cid",
                "carrier_cid",
                "departure_mh",
                "departure_mh_space_list",
                "arrival_mh",
                "arrival_mh_space_list",
                "tractor_giai",
                "dep_req_from_time",
                "dep_req_to_time",
                "arv_req_from_time",
                "arv_req_to_time",
            ]:
                if key not in query_params:
                    no_key.append(key)
            if len(no_key) > 0:
                no_keys = ",".join(no_key)
                raise ValueError(f"Parameters missing:{no_keys}")
            for p in [
                "shipper_cid",
                "carrier_cid",
            ]:
                if query_params[p] not in COMPANY_INFOS:
                    raise ValueError(f"{p}:{query_params[p]} is not valid cid.")
            trsp_instruction_id = query_params["trsp_instruction_id"]
            shipper_cid = query_params["shipper_cid"]
            carrier_cid = query_params["carrier_cid"]
            departure_mh = query_params["departure_mh"]
            departure_mh_space_list = query_params["departure_mh_space_list"].split(",")
            arrival_mh = query_params["arrival_mh"]
            arrival_mh_space_list = query_params["arrival_mh_space_list"].split(",")
            tractor_giai = query_params["tractor_giai"]
            dep_req_from_time = query_params["dep_req_from_time"]
            dep_req_to_time = query_params["dep_req_to_time"]
            arv_req_from_time = query_params["arv_req_from_time"]
            arv_req_to_time = query_params["arv_req_to_time"]
            logger.debug(f"API-040 運行計画登録（車両割付）CID:{shipper_cid}")
            data = request.get_json()
            logger.debug(f"API-040 運行計画登録（車両割付）data={data}")
            # バンニング、デバンニング計画更新
            update_devanning_vanning_plan(
                trsp_instruction_id,
                shipper_cid,
                carrier_cid,
                departure_mh,
                departure_mh_space_list,
                arrival_mh,
                arrival_mh_space_list,
                tractor_giai,
                dep_req_from_time,
                dep_req_to_time,
                arv_req_from_time,
                arv_req_to_time,
            )
            ret = {
                "operation_plans": {
                    "trsp_instruction_id": trsp_instruction_id,
                    "shipper_cid": shipper_cid,
                    "carrier_cid": carrier_cid,
                    "departure_mh": departure_mh,
                    "departure_mh_space_list": departure_mh_space_list,
                    "arrival_mh": arrival_mh,
                    "arrival_mh_space_list": arrival_mh_space_list,
                    "tractor_giai": tractor_giai,
                    "dep_req_from_time": dep_req_from_time,
                    "dep_req_to_time": dep_req_to_time,
                    "arv_req_from_time": arv_req_from_time,
                    "arv_req_to_time": arv_req_to_time,
                },
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {"operation_plans": {}, "result": False, "error_msg": "error"}
            status = 400
        except Exception as e:
            logger.debug(
                f"API-040 運行計画登録: {e.args[0]}", exc_info=True, stack_info=True
            )
            ret = {
                "operation_plans": {},
                "result": False,
                "error_msg": str(e.args[0]),
            }
            status = 500
        logger.debug(f"API-040 運行計画登録 End Status={status}")
        return ret, status



@operation_plans_api_ns.route("/<string:operation_id>/notify")
@operation_plans_api_ns.param("operation_id", "運行計画ID")
class OperationPlanNotifyApi(Resource):
    post_request_model = create_restx_model_usingSchema(
        "OperationPlanNotifyPostRequestModel",
        operation_plans_api_ns,
        TrspAbilityLineItemSchema,
    )
    post_response_data = operation_plans_api_ns.clone(
        "OperationPlanNotifyPostResponse",
        post_request_model,
        {
            "shipper_cid": fields.String(
                example="490000001", description="依頼元の事業者ID", required=True
            ),
            "carrier_cid": fields.String(
                example="490000002",
                description="依頼先(申し込みを受ける側・回答する側)の事業者ID",
                required=True,
            ),
        },
    )
    post_response_model = create_response_model(
        "OperationPlansResponseModel",
        operation_plans_api_ns,
        "operation_plan",
        post_response_data,
    )

    @operation_plans_api_ns.doc(
        description=(
            "API-043 運行実施確認通知<br/>" "- サプライ・サイドからのみ利用可<br/>"
        ),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
        },
    )
    @operation_plans_api_ns.response(200, "Success", post_response_model)
    @operation_plans_api_ns.response(400, "HTTP400エラー")
    @operation_plans_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id):
        query_params = request.args.to_dict()
        logger.debug(f"API-043 運行実施確認通知 Start query_params={query_params}")
        cid_key = "shipper_cid"
        if cid_key in query_params:
            cid = query_params[cid_key]
        else:
            cid = None
        logger.debug(f"API-043 運行実施確認通知 CID:{cid}")
        data = request.get_json()
        logger.debug(f"API-043 運行実施確認通知 data:{data}")
        if cid is not None:
            url = urljoin(
                Config.CONNECTOR_PRIVATE_ENDPOINT,
                f"operation_plans/{operation_id}/notify",
            )
            endpoint = get_endpoint_from_cid(cid)
            logger.debug(f"API-043 運行実施確認通知 CONNECT cid:{url} / {endpoint}")
            headers = {"X-ENDPOINT": endpoint}
            try:
                response = requests.post(
                    url,
                    json=data,
                    params=query_params,
                    verify=False,
                    proxies={"no_proxy": "co_logi_connector"},
                    headers=headers,
                )
                logger.debug(f"API-043 運行実施確認通知 Response Code: {response.status_code}")
                if response.status_code != 200:
                    raise ValueError("BACKEND ERROR")
                response.encoding = response.apparent_encoding
                operation_plan_data = response.json()
                ret = {
                    "result": True,
                    "error_msg": "",
                }
                status = 200
            except Exception as e:
                logger.error(
                    f"API-043 運行実施確認通知 {e.args[0]}",
                    exc_info=True,
                    stack_info=True,
                )
                ret = {
                    "result": False,
                    "error_msg": f"error:{e}",
                }
                status = 500
        else:
            logger.debug(f"API-043 運行実施確認通知 {cid_key}はNullです。")
            ret = {
                "result": False,
                "error_msg": f"{cid_key}はNullです。",
            }
            status = 400
        logger.debug(f"API-043 運行実施確認通知  End Status={status}")
        return ret, status
