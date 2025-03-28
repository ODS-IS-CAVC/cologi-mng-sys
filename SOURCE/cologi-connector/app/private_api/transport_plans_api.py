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
import json
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
from app.config import Config
from com.company_info import COMPANY_INFOS


transport_plans_api_ns = Namespace(
    "/private/api/transport_plans", description="輸送計画"
)

parser = transport_plans_api_ns.parser()
parser.add_argument("q", type=str, help="クエリ文字列", required=False, location="args")
parser.add_argument(
    "endpoint", type=str, help="相手のEndpoint", required=False, location="args"
)
parser.add_argument(
    "o", type=int, help="オフセット", default=0, required=False, location="args"
)
parser.add_argument(
    "n", type=int, help="取得数", default=100, required=False, location="args"
)
id_parser = transport_plans_api_ns.parser()
id_parser.add_argument("cid", type=str, help="事業者ID", required=True, location="args")

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
            "endpoint": "相手(キャリア)のEndpoint(required)",
        },
    )
    def put(self, trsp_instruction_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        # TODO: 今年度は処理なし
        endpoint = "MH"
        url = urljoin(endpoint, "")
        try:
            # logger.debug(f"CONNECT:{url}")
            # data = request.get_json()
            # logger.debug(data)
            # response = requests.put(
            #     url,
            #     json=data,
            #     params=query_params,
            #     verify=False,
            #     proxies={"no_proxy": "localhost"},
            # )
            # response.encoding = response.apparent_encoding
            # data = response.json()
            # logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
            ret = {
                "transport_plans": {},
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "transport_plans": {},
                "result": True,
                "error_msg": "",
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
            "cid": fields.String(example="490000001", description="事業者ID"),
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
            "endpoint": "相手(キャリア)のEndpoint(required)",
        },
    )
    @transport_plans_api_ns.response(200, "Success", post_response_model)
    @transport_plans_api_ns.response(400, "HTTP400エラー")
    @transport_plans_api_ns.response(500, "HTTP500エラー")
    def post(self, trsp_instruction_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(
            endpoint,
            f"transport_plans/{trsp_instruction_id}/notify",
        )
        try:
            logger.debug(f"CONNECT:{url}")
            data = request.get_json()
            logger.debug(data)
            response = requests.post(
                url,
                json=data,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "localhost"},
            )
            if response.status_code != 200:
                response.encoding = response.apparent_encoding
                data = response.json()
                ret = {
                    "transport_plans": {},
                    "result": False,
                    "error_msg": data["error_msg"],
                }
                status = response.status_code
            else:
                response.encoding = response.apparent_encoding
                data = response.json()
                logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
                ret = {
                    "transport_plans": data.get("transport_plans", []),
                    "result": True,
                    "error_msg": "",
                }
                status = 200
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "transport_plans": [],
                "result": False,
                "error_msg": str(e.args[0]),
            }
            status = 500
        return ret, status
