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
from model.operation_plan_model import OperationPlanSchema
from model.model_5001.trsp_ability_line_item_model import TrspAbilityLineItemSchema
from model.model_3012_operation.trsp_plan_line_item_model import TrspPlanLineItemSchema
from model.model_3012_operation.trsp_plan_model import TrspPlanSchema
from model.model_3012_operation.msg_info_model import MsgInfoSchema
from app.config import Config
from com.company_info import COMPANY_INFOS


operation_plans_api_ns = Namespace(
    "/private/api/operation_plans", description="運行計画"
)

parser = operation_plans_api_ns.parser()
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
id_parser = operation_plans_api_ns.parser()
id_parser.add_argument("cid", type=str, help="事業者ID", required=True, location="args")

query_parser = create_query_parser(operation_plans_api_ns)


@operation_plans_api_ns.route("/<string:operation_id>")
@operation_plans_api_ns.param("operation_id", "運行計画ID")
class OperationPlansApi(Resource):
    post_request_model = create_restx_model_usingSchema(
        "OperationPlanDataUpdateRequestModel",
        operation_plans_api_ns,
        OperationPlanSchema,
        exclude_fields=["id"],
    )
    post_response_model = create_response_model(
        "OperationPlanDataUpdateResponseModel",
        operation_plans_api_ns,
        "operation_plans",
        post_request_model,
    )

    @operation_plans_api_ns.doc(
        description=("API-042 運行計画更新<br/>" "- サプライ・サイドからのみ利用可"),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "endpoint": "相手(荷主)のEndpoint(required)",
        },
    )
    def put(self, operation_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(endpoint, "shipper_operations")
        try:
            logger.debug(f"CONNECT:{url}")
            data = request.get_json()
            logger.debug(data)
            response = requests.put(
                url,
                json=data,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "localhost"},
            )
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
            ret = {
                "operation_notify": data.get("shipper_operations_list", []),
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_notify": [],
                "result": False,
                "error_msg": "Error",
            }
        return ret, 200


@operation_plans_api_ns.route("/")
class OperationPlansListApi(Resource):
    post_request_model = create_restx_model_usingSchema(
        "OperationPlanDataPostRequestModel",
        operation_plans_api_ns,
        OperationPlanSchema,
        exclude_fields=["id"],
    )
    post_response_model = create_response_model(
        "OperationPlanDataPostResponseModel",
        operation_plans_api_ns,
        "operation_plans",
        post_request_model,
    )

    @operation_plans_api_ns.doc(
        description=(
            "API-040 運行計画登録（車両割付）<br/>" "- サプライ・サイドからのみ利用可"
        ),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "endpoint": "相手(荷主)のEndpoint(required)",
        },
    )
    def post(self):
        query_params = request.args.to_dict()
        logger.debug(f"API-040 運行計画登録（車両割付）(Private) Start query_params={query_params}")
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(endpoint, "operation_plans")
        try:
            logger.debug(f"API-040 運行計画登録（車両割付）(Private)  CONNECT:{url}")
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
                raise ValueError(f"Backend Error response.status_code = {response.status_code}")
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"API-040 運行計画登録（車両割付）(Private)  CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
            ret = {
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.debug("API-040 運行計画登録（車両割付）(Private) Backend Error")
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "error_msg": "Backend Error",
            }
            status = 400
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "error_msg": "error",
            }
            status = 500
        logger.debug(f"API-040 運行計画登録（車両割付）(Private) End status={status}")
        return ret, status


@operation_plans_api_ns.route("/<string:operation_id>/notify")
@operation_plans_api_ns.param("operation_id", "運行計画ID")
class OperationPlanNotifyApi(Resource):
    put_request_model = create_restx_model_usingSchema(
        "OperationPlanNotifyPutRequestModel",
        operation_plans_api_ns,
        TrspAbilityLineItemSchema,
    )
    put_response_data = operation_plans_api_ns.clone(
        "OperationPlanNotifyPutResponse",
        put_request_model,
        {
            "cid": fields.String(example="490000001", description="事業者ID"),
        },
    )
    put_response_model = create_response_model(
        "OperationPlansResponseModel",
        operation_plans_api_ns,
        "operation_plan",
        put_response_data,
    )

    @operation_plans_api_ns.doc(
        description=(
            "API-045 運行実施（確認）通知<br/>" "- サプライ・サイドからのみ利用可<br/>"
        ),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "endpoint": "相手(荷主)のEndpoint(required)",
        },
    )
    @operation_plans_api_ns.response(200, "Success", put_response_model)
    @operation_plans_api_ns.response(400, "HTTP400エラー")
    @operation_plans_api_ns.response(500, "HTTP500エラー")
    def put(self, operation_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        # TODO:  今年度は呼び出し先無し
        # endpoint = request.headers.get("X-ENDPOINT")
        # url = urljoin(endpoint, "")
        try:
        #     logger.debug(f"CONNECT:{url}")
        #     data = request.get_json()
        #     logger.debug(data)
        #     response = requests.put(
        #         url,
        #         json=data,
        #         params=query_params,
        #         verify=False,
        #         proxies={"no_proxy": "localhost"},
        #     )
        #     response.encoding = response.apparent_encoding
        #     data = response.json()
        #     logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
            ret = {
                "operation_plans": {},
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_plans": {},
                "result": False,
                "error_msg": "error",
            }
        return ret, 200


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
        logger.debug(f"API-043 運行実施確認通知(Private) Start ={query_params}")
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(
            endpoint,
            f"operation_plans/{operation_id}/notify",
        )
        try:
            logger.debug(f"API-043 運行実施確認通知(Private) CONNECT:{url}")
            data = request.get_json()
            logger.debug(f"API-043 運行実施確認通知(Private) data={data}")
            response = requests.post(
                url,
                json=data,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "localhost"},
            )
            if response.status_code != 200:
                raise ValueError("Backend Error")
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
            ret = {
                "operation_plan": data.get("operation_plan", []),
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_plans": [],
                "result": False,
                "error_msg": "Backend Error",
            }
            status = 400
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_plans": [],
                "result": False,
                "error_msg": "error",
            }
            status = 500
        logger.debug(f"API-043 運行実施確認通知(Private) END status={status}")
        return ret, status
