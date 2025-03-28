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
import urllib
from flask import request
import requests
from urllib.parse import urljoin
import logging
import dateutil.parser

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from com.helper import (
    create_restx_model_usingSchema,
    create_response_model,
)
from model.transportation_plan_model import TransportationPlanSchema
from model.model_3012_transport.trsp_plan_line_item_model import TrspPlanLineItemSchema
from model.model_3012_transport.msg_info_model import MsgInfoSchema
from app.config import Config
from com.company_info import get_endpoint_from_cid
from com.vanning import Vanning


transport_plans_api_ns = Namespace("/webapi/v1/transport_plans", description="輸送計画")

parser = transport_plans_api_ns.parser()
parser.add_argument("q", type=str, help="クエリ文字列", required=False, location="args")
parser.add_argument(
    "o", type=int, help="オフセット", default=0, required=False, location="args"
)
parser.add_argument(
    "n", type=int, help="取得数", default=100, required=False, location="args"
)
id_parser = transport_plans_api_ns.parser()
id_parser.add_argument("cid", type=str, help="事業者ID", required=True, location="args")


@transport_plans_api_ns.route("/<string:trsp_instruction_id>")
@transport_plans_api_ns.param("trsp_instruction_id", "運送依頼番号")
class TransportPlanApi(Resource):
    post_request_model = create_restx_model_usingSchema(
        "TransportPlanRequestModel",
        transport_plans_api_ns,
        TransportationPlanSchema,
        exclude_fields=["id"],
    )
    post_response_data = transport_plans_api_ns.clone(
        "TransportPlanPostResponse",
        post_request_model,
        {
            "is_shipper": fields.String(
                example=True, description="荷主の場合にはtrue、荷受け人の場合にはfalse"
            ),
            "shipper_cid": fields.String(
                example="490000001", description="荷主の事業者ID"
            ),
            "recipient_cid": fields.String(
                example="490000003", description="荷受け人の事業者ID"
            ),
            "carrier_cid": fields.String(
                example="491000002", description="キャリアの事業者ID"
            ),
            "tractor_giai": fields.String(
                example="8004991000001000000000000000000001",
                description="使用するトラクターのGIAI",
            ),
            "trailer_giai_list": fields.String(
                example=[
                    "8004992000001000000000000000000001",
                    "8004992000001000000000000000000002",
                ],
                description="使用するトレーラーのGIAIのリスト(is_shipper=trueの時はrequired)",
            ),
            "req_from_time": fields.String(
                example="2015-01-02 13:00:00", description="MH作業希望時間(From)"
            ),
            "req_to_time": fields.String(
                example="2015-01-02 13:10:00", description="MH作業希望時間(To)"
            ),
        },
    )
    post_response_model = create_response_model(
        "TransportPlanResponseModel",
        transport_plans_api_ns,
        "transport_plans",
        post_response_data,
    )
    updated_post_rsp_model = transport_plans_api_ns.clone(
        "TransportPlanUpdatedPostResponse",
        post_response_model,
        {
            "mh": fields.String(
                example="8004993000001000000000000000000001", description="MHのGLN"
            ),
            "mh_space_list": fields.String(
                example=["1", "2"], description="mh_space_list"
            ),
        },
    )

    @transport_plans_api_ns.doc(
        description=(
            "API-050 輸送計画登録（車両割り付け）<br/>"
            "- デマンド・サイドからのみ利用可<br/>"
            "- 荷主又は荷受け人が使用するAPI"
        ),
        params={
            "is_shipper": "荷主の場合にはtrue、荷受け人の場合にはfalse(required)",
            "shipper_cid": "荷主の事業者ID(required)",
            "recipient_cid": "荷受け人の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "tractor_giai": "使用するトラクターのGIAI(required)",
            "trailer_giai_list": "使用するトレーラーのGIAIのリスト(is_shipper=trueの時はrequired)",
            "req_from_time": "MH作業希望時間(From)(required)",
            "req_to_time": "MH作業希望時間(To)(required)",
            "mh": "MHのGLN(is_shipper=trueの時は発MH、falseの時は着MH)(required)",
        },
    )
    def post(self, trsp_instruction_id):
        query_params = request.args.to_dict()
        logger.debug(f"API-050 輸送計画登録（車両割り付け）Start {query_params}")
        try:
            no_key = []
            for key in [
                "is_shipper",
                "shipper_cid",
                "recipient_cid",
                "carrier_cid",
                "tractor_giai",
                "req_from_time",
                "req_to_time",
                "mh",
            ]:
                if key not in query_params:
                    no_key.append(key)
            if len(no_key) > 0:
                no_keys = ",".join(no_key)
                raise ValueError(f"Parameters missing:{no_keys}")
            is_shipper = (
                True
                if query_params["is_shipper"] == "true"
                or query_params["is_shipper"] == "1"
                else False
            )
            shipper_cid = query_params["shipper_cid"]
            recipient_cid = query_params["recipient_cid"]
            carrier_cid = query_params["carrier_cid"]
            tractor_giai = query_params["tractor_giai"]
            mh = query_params["mh"]
            trailer_giai_list = query_params.get("trailer_giai_list", None)
            if trailer_giai_list is None:
                trailer_giai_list = []
            else:
                trailer_giai_list = trailer_giai_list.split(",")
            req_from_time = urllib.parse.unquote(query_params["req_from_time"])
            req_to_time = urllib.parse.unquote(query_params["req_to_time"])
            # バンニング、デバンニング計画更新
            self.update_devanning_vanning_plan(
                is_shipper,
                trsp_instruction_id,
                shipper_cid,
                recipient_cid,
                tractor_giai,
                trailer_giai_list,
                req_from_time,
                req_to_time,
            )
            ret = {
                "transport_plans": {
                    "trsp_instruction_id": trsp_instruction_id,
                    "is_shipper": is_shipper,
                    "shipper_cid": shipper_cid,
                    "recipient_cid": recipient_cid,
                    "carrier_cid": carrier_cid,
                    "tractor_giai": tractor_giai,
                    "trailer_giai_list": trailer_giai_list,
                    "req_from_time": req_from_time,
                    "req_to_time": req_to_time,
                    "mh": mh,
                },
                "result": True,
                "error_msg": "",
            }
            status = 200
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {"transport_plans": {}, "result": False, "error_msg": "error"}
            status = 400
        except Exception as e:
            logger.debug(e, exc_info=True, stack_info=True)
            ret = {
                "transport_plans": {},
                "result": False,
                "error_msg": str(e.args[0]),
            }
            status = 400
        logger.debug(f"API-050 輸送計画登録（車両割り付け）END status={status}")
        return ret, status

    def update_devanning_vanning_plan(
        self,
        is_shipper,
        trsp_instruction_id,
        shipper_cid,
        recipient_cid,
        tractor_giai,
        trailer_giai_list,
        req_from_time,
        req_to_time,
    ):
        # 前の情報があれば取得、無ければ初期データ取得
        vanning = Vanning()
        ## 出発MH
        dep_devanning_plan = vanning.search_plan(
            is_departure_mh=1, trsp_instruction_id=trsp_instruction_id, is_vanning=0
        )
        dep_vanning_plan = vanning.search_plan(
            is_departure_mh=1, trsp_instruction_id=trsp_instruction_id, is_vanning=1
        )
        ## 到着MH
        arv_devanning_plan = vanning.search_plan(
            is_departure_mh=0, trsp_instruction_id=trsp_instruction_id, is_vanning=0
        )
        arv_vanning_plan = vanning.search_plan(
            is_departure_mh=0, trsp_instruction_id=trsp_instruction_id, is_vanning=1
        )
        if (
            dep_devanning_plan is None
            or dep_vanning_plan is None
            or arv_devanning_plan is None
            or arv_vanning_plan is None
        ):
            raise ValueError(
                f"バンニング・デバンニング計画が登録されてません trsp_instruction_id={trsp_instruction_id}"
            )
        # 必要なデータの更新
        if is_shipper is False:
            # 荷受け人
            aped_devan_from_datetime = dateutil.parser.parse(req_from_time)
            aped_devan_to_datetime = dateutil.parser.parse(req_to_time)
            arv_vanning_plan["tractor_giai"] = tractor_giai
            arv_vanning_plan["req_from_time"] = aped_devan_from_datetime.strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
            arv_vanning_plan["req_to_time"] = aped_devan_to_datetime.strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
            arv_vanning_plan["status"] = 1
            arv_vanning_plan["is_bl_need"] = 1
            arv_vanning_plan["is_departure_mh"] = 0

        else:
            # 荷主
            ## 出発MH
            ### データ
            dep_devanning_plan["shipper_cid"] = shipper_cid
            dep_vanning_plan["shipper_cid"] = shipper_cid
            dep_devanning_plan["recipient_cid"] = recipient_cid
            dep_vanning_plan["recipient_cid"] = recipient_cid
            dep_devanning_plan["trsp_instruction_id"] = trsp_instruction_id
            dep_vanning_plan["trsp_instruction_id"] = trsp_instruction_id
            dep_devanning_plan["status"] = 1
            dep_vanning_plan["status"] = 1
            dep_devanning_plan["is_bl_need"] = 0
            dep_vanning_plan["is_bl_need"] = 0
            dep_devanning_plan["is_departure_mh"] = 1
            dep_vanning_plan["is_departure_mh"] = 1
            dep_devan_from_datetime = dateutil.parser.parse(req_from_time)
            dep_devan_to_datetime = dateutil.parser.parse(req_to_time)
            dep_devanning_plan["tractor_giai"] = tractor_giai
            dep_devanning_plan["req_from_time"] = dep_devan_from_datetime.strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
            dep_devanning_plan["req_to_time"] = dep_devan_to_datetime.strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
            dep_devanning_plan["trailer_giai_list"] = trailer_giai_list
            dep_vanning_plan["trailer_giai_list"] = trailer_giai_list

            ## 到着MH
            ### データ
            arv_devanning_plan["trsp_instruction_id"] = trsp_instruction_id
            arv_vanning_plan["trsp_instruction_id"] = trsp_instruction_id
            arv_devanning_plan["shipper_cid"] = shipper_cid
            arv_vanning_plan["shipper_cid"] = shipper_cid
            arv_devanning_plan["recipient_cid"] = recipient_cid
            arv_vanning_plan["recipient_cid"] = recipient_cid
            arv_devanning_plan["status"] = 1
            arv_vanning_plan["status"] = 1
            arv_devanning_plan["is_bl_need"] = 0
            arv_vanning_plan["is_bl_need"] = 1
            arv_devanning_plan["is_departure_mh"] = 0
            arv_vanning_plan["is_departure_mh"] = 0
            arv_vanning_plan["trailer_giai_list"] = trailer_giai_list
            arv_devanning_plan["trailer_giai_list"] = trailer_giai_list

        # 更新したデータを保存
        if is_shipper is True:
            # 荷主
            ## 出発MH
            vanning.save_plan(
                "devanning_plan",
                dep_devanning_plan["mh"],
                trsp_instruction_id,
                dep_devanning_plan,
            )
            vanning.save_plan(
                "vanning_plan",
                dep_vanning_plan["mh"],
                trsp_instruction_id,
                dep_vanning_plan,
            )
            ## 到着MH
            vanning.save_plan(
                "devanning_plan",
                arv_devanning_plan["mh"],
                trsp_instruction_id,
                arv_devanning_plan,
            )

        vanning.save_plan(
            "vanning_plan",
            arv_vanning_plan["mh"],
            trsp_instruction_id,
            arv_vanning_plan,
        )

    @transport_plans_api_ns.doc(
        description=(
            "API-053 輸送計画更新<br/>"
            "- デマンド・サイドからのみ利用可<br/>"
            "- 荷主又は荷受け人が使用するAPI"
        ),
        params={
            "is_shipper": "荷主の場合にはtrue、荷受け人の場合にはfalse(required)",
            "shipper_cid": "荷主の事業者ID(required)",
            "recipient_cid": "荷受け人の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "tractor_giai": "使用するトラクターのGIAI(required)",
            "trailer_giai_list": "使用するトレーラーのGIAIのリスト(is_shipper=trueの時はrequired)",
            "req_from_time": "MH作業希望時間(From)(required)",
            "req_to_time": "MH作業希望時間(To)(required)",
            "mh": "MHのGLN(is_shipper=trueの時は発MH、falseの時は着MH)(required)",
        },
    )
    def put(self, trsp_instruction_id):
        # PUt/POSTは同一処理
        return self.post(trsp_instruction_id)


@transport_plans_api_ns.route("/<string:trsp_instruction_id>/notify")
@transport_plans_api_ns.param("trsp_instruction_id", "運送依頼番号")
class TransportPlanNotifyApi(Resource):
    post_request_model = create_restx_model_usingSchema(
        "TransportPlanNotifyDataPostRequestModel",
        transport_plans_api_ns,
        TrspPlanLineItemSchema,
    )
    post_response_data = transport_plans_api_ns.clone(
        "TransportPlanNotifyPostResponse",
        post_request_model,
        {
            "shipper_cid": fields.String(
                example="490000001", description="荷主の事業者ID"
            ),
            "carrier_cid": fields.String(
                example="491000002", description="キャリアの事業者ID"
            ),
        },
    )
    post_response_model = create_response_model(
        "TransportPlanNotifyDataPostResponseModel",
        transport_plans_api_ns,
        "transport_plans",
        post_response_data,
    )

    @transport_plans_api_ns.doc(
        description=(
            "API-052 輸送実施（確認）通知<br/>" "- デマンド・サイドからのみ利用可<br/>"
        ),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
        },
    )
    @transport_plans_api_ns.response(200, "Success", post_response_model)
    @transport_plans_api_ns.response(400, "HTTP400エラー")
    @transport_plans_api_ns.response(500, "HTTP500エラー")
    def post(self, trsp_instruction_id):
        query_params = request.args.to_dict()
        logger.debug(f"API-052 輸送実施（確認）通知 Start query_params={query_params}")
        try:
            data = request.get_json()
            logger.debug(f"API-052 輸送実施（確認）通知 data={data}")
            carrier_cid = query_params.get("carrier_cid", None)
            shipper_cid = query_params.get("shipper_cid", None)
            recipient_cid = None
            if "cnee_prty" in data:
                if data["cnee_prty"]:
                    recipient_cid = data["cnee_prty"].get("cnee_prty_head_off_id", None)
            if carrier_cid is None or shipper_cid is None or recipient_cid is None:
                raise ValueError(
                    "carrier_cid/shipper_cid/cnee_prty.cnee_prty_head_off_id are Needed"
                )
            logger.debug(
                f"API-052 輸送実施（確認）通知 carrier_cid:{carrier_cid}"
                f"/shipper_cid:{shipper_cid}/recipient_cid:{recipient_cid}"
            )
            if carrier_cid is None or shipper_cid is None:
                raise ValueError("carrier_cid/shipper_cid is required")
            url = urljoin(
                Config.CONNECTOR_PRIVATE_ENDPOINT,
                f"transport_plans/{trsp_instruction_id}/notify",
            )
            endpoint = get_endpoint_from_cid(carrier_cid)
            logger.debug(f"API-052 輸送実施（確認）通知 CONNECT cid:{url} / {endpoint}")
            headers = {"X-ENDPOINT": endpoint}
            response = requests.post(
                url,
                json=data,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "co_logi_connector"},
                headers=headers,
            )
            logger.debug(
                f"API-052 輸送実施（確認）通知 Response Code: {response.status_code}"
            )
            if response.status_code != 200:
                raise ValueError("BACKEND ERROR")
            response.encoding = response.apparent_encoding
            transport_plans_data = response.json()
            transport_plans_data = transport_plans_data.get("transport_plans_data", {})
            ret = {
                "transport_plans": transport_plans_data,
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.debug(f"API-052 輸送実施（確認）通知{e.args[0]}")
            ret = {
                "result": False,
                "error_msg": f"error :{str(e.args[0])}",
                "transport_plans": {},
            }
            status = 400
        except Exception as e:
            logger.error(
                exc_info=True,
                stack_info=True,
            )
            ret = {
                "result": False,
                "error_msg": "error",
                "transport_plans": {},
            }
            status = 500
        logger.debug(f"API-052 輸送実施（確認）通知 End Status={status}")
        return ret, status
