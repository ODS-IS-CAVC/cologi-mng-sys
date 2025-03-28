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
import json
from flask import request
import requests
from urllib.parse import urljoin
import logging

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from com.helper import (
    create_restx_model_usingSchema,
    create_response_model,
    create_query_parser,
)
from model.transportation_plan_model import TransportationPlanSchema
from model.model_3012_transport.trsp_plan_line_item_model import TrspPlanLineItemSchema
from model.model_3012_transport.msg_info_model import MsgInfoSchema
from com.backend_api import BackendApi
from model.ebl_model import EblJson
from app.config import Config
from com.company_info import (
    get_address_from_cid,
    get_name_from_cid,
    get_recipient_tractor,
    get_shipper_tractor,
)
from com.mobility_hub import get_name_by_gln

transport_plans_api_ns = Namespace(
    "/public/api/transport_plans", description="輸送計画"
)

parser = transport_plans_api_ns.parser()
parser.add_argument("q", type=str, help="クエリ文字列", required=False, location="args")
parser.add_argument(
    "source_endpoint",
    type=str,
    help="呼出し元のEndpoint",
    required=False,
    location="args",
)
parser.add_argument(
    "o", type=int, help="オフセット", default=0, required=False, location="args"
)
parser.add_argument(
    "n", type=int, help="取得数", default=100, required=False, location="args"
)
id_parser = transport_plans_api_ns.parser()
id_parser.add_argument(
    "source_cid", type=str, help="事業者ID", required=True, location="args"
)

query_parser = create_query_parser(transport_plans_api_ns)


@transport_plans_api_ns.route("/<string:trsp_instruction_id>")
@transport_plans_api_ns.param("trsp_instruction_id", "運送依頼番号")
class TransportPlanApi(Resource):
    post_request_model = create_restx_model_usingSchema(
        "TransportPlanDataUpdateRequestModel",
        transport_plans_api_ns,
        TransportationPlanSchema,
        exclude_fields=["id"],
    )
    put_request_model = create_restx_model_usingSchema(
        "TransportPlanDataUpdateRequestModel",
        transport_plans_api_ns,
        TransportationPlanSchema,
        exclude_fields=["id"],
    )
    put_response_model = create_response_model(
        "TransportPlanDataUpdateResponseModel",
        transport_plans_api_ns,
        "transport_plans",
        post_request_model,
    )

    @transport_plans_api_ns.doc(
        description=("API-053 輸送計画更新<br/>" "- デマンド・サイドからのみ利用可"),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "source_endpoint": "呼出し元のEndpoint(required)",
        },
    )
    def put(self, trsp_instruction_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        # TODO: 今年度は処理なし
        api = ""
        logger.debug(f"CONNECT BACKEND:{api}")
        try:
            # backend_api = BackendApi()
            # data = request.get_json()
            # logger.debug(data)
            # response = backend_api.call_api(
            #     api,
            #     method="PUT",
            #     data=data,
            #     param=query_params,
            # )
            # if response is False:
            #     raise ValueError("Backend error")
            # logger.debug(f"BACKEND RESPONSE: {response}")
            ret = {
                "transport_plans": {},
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "transport_plans": {},
                "result": False,
                "error_msg": "errror",
            }
        return ret, 200


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
            "source_cid": fields.String(example="490000001", description="事業者ID"),
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
            "source_endpoint": "呼出し元のEndpoint(required)",
        },
    )
    @transport_plans_api_ns.response(200, "Success", post_response_model)
    @transport_plans_api_ns.response(400, "HTTP400エラー")
    @transport_plans_api_ns.response(500, "HTTP500エラー")
    def post(self, trsp_instruction_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        # API-152 CALL
        api = f"transports/{trsp_instruction_id}/notify"
        logger.debug(f"CONNECT BACKEND:{api}")
        try:
            data = request.get_json()
            logger.debug(data)
            backend_api = BackendApi()
            response = backend_api.call_api(
                api,
                method="POST",
                data=data,
                param=query_params,
            )
            if response is False:
                raise ValueError(f"Backend error({api})")
            # 処理が正常ならEBL発行
            carrier_cid = query_params.get("carrier_cid", None)
            if carrier_cid is None:
                if "carrier_cid" not in data:
                    raise ValueError("carrier_cid is required")
                carrier_cid = data.get("carrier_cid")
            shipper_cid = query_params.get("shipper_cid", None)
            if shipper_cid is None:
                if "shipper_cid" not in data:
                    raise ValueError("shipper_cid is required")
                shipper_cid = data.get("shipper_cid")
            # TODO: 支払いチェック  今年度は常にOK
            is_payment_ok = True
            if is_payment_ok:
                self.save_ebl(data, trsp_instruction_id, carrier_cid, shipper_cid)
            else:
                logger.debug(f"支払いが完了するまでB/Lは発行しない")
            logger.debug(f"BACKEND RESPONSE: {response}")
            ret = {
                "transport_plans": response,
                "result": True,
                "error_msg": "",
            }
            status = 200
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "transport_plans": {},
                "result": True,
                "error_msg": str(e.args[0]),
            }
            status = 400
        return ret, status

    def save_ebl(
        self,
        data,
        trsp_instruction_id,
        carrier_cid,
        shipper_cid,
    ):
        file_path = os.path.join(
            os.environ.get("EBL_DIR"), f"{trsp_instruction_id}.json"
        )
        # もし同じファイルがあったら ファイルを削除
        if os.path.isfile(file_path):
            os.remove(file_path)
        ebl = EblJson()
        recipient_cid = None
        if "cnee_prty" in data:
            recipient_cid = data["cnee_prty"].get("cnee_prty_head_off_id", None)
        if recipient_cid is not None:
            recipient_name = get_name_from_cid(recipient_cid)
            ebl.set_recipient(recipient_cid, recipient_name)
        shipper_name = get_name_from_cid(shipper_cid)
        ebl.set_shipper(shipper_cid, shipper_name)
        departure_mh_gln = None
        if "ship_from_prty" in data:
            departure_mh_gln = data["ship_from_prty"].get("gln_prty_id", None)
        if departure_mh_gln != None:
            departure_mh_name = get_name_by_gln(departure_mh_gln)
            ebl.set_departure_mh(departure_mh_gln, departure_mh_name)
        arrival_mh_gln = None
        if "ship_to_prty" in data:
            arrival_mh_gln = data["ship_to_prty"].get("gln_prty_id", None)
        if arrival_mh_gln != None:
            arrival_mh_name = get_name_by_gln(arrival_mh_gln)
            ebl.set_arrival_mh(arrival_mh_gln, arrival_mh_name)
        # TODO: 今年度は入れない
        # ebl.set_trailers(trailer_list)
        # 今年度は設定値
        ebl.set_shipper_tractor(get_shipper_tractor(shipper_cid))
        ebl.set_recipient_tractor(get_recipient_tractor(recipient_cid))
        ebl_data = ebl.issue(carrier_cid)
        # B/L登録
        url = urljoin(
            Config.TRUST_MNG_ENDPOINT,
            "bl/register",
        )
        data = {
            "cid": carrier_cid,
            "bl_json": ebl_data,
        }
        logger.debug(f"B/L 登録： {url}")
        logger.debug(f"        ： {data}")
        response = requests.post(
            url,
            json=data,
            verify=False,
        )
        logger.debug(f"Response Code: {response.status_code}")
        if response.status_code != 200:
            logger.debug(response)
            raise ValueError("トラスト基盤 BL登録 ERROR")
        response.encoding = response.apparent_encoding
        bl_reg = response.json()
        bl_id = int(bl_reg.get("bl_id"))
        signed_bl = bl_reg.get("signed_bl")
        logger.debug(f"署名済みB/L： {signed_bl}")

        bl_file = {
            "signed_bl": signed_bl,
            "bl_id": bl_id,
            "current_owner": carrier_cid,
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(bl_file, f, indent=4, ensure_ascii=False)
        logger.debug(f"save EBL {file_path}")
        return True
