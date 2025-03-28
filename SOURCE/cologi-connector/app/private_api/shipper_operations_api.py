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
from model.model_5001.trsp_ability_line_item_model import TrspAbilityLineItemSchema
from model.model_5001.msg_info_model import MsgInfoSchema
from app.config import Config
from com.company_info import COMPANY_INFOS

shipper_operations_api_ns = Namespace(
    "/private/api/shipper_operations", description="ダイヤ（荷主向け運行案内）"
)

parser = shipper_operations_api_ns.parser()
parser.add_argument("cid", type=str, help="事業者ID", required=False, location="args")
parser.add_argument(
    "endpoint", type=str, help="相手のEndpoint", required=False, location="args"
)
parser.add_argument(
    "o", type=int, help="オフセット", default=0, required=False, location="args"
)
parser.add_argument(
    "n", type=int, help="取得数", default=1, required=False, location="args"
)
query_parser = create_query_parser(shipper_operations_api_ns)


@shipper_operations_api_ns.route("/")
class ShipperOperationsApi(Resource):
    get_trsp_list_data_model = create_restx_model_usingSchema(
        "ScheduleTrspDataListGetModel",
        shipper_operations_api_ns,
        TrspAbilityLineItemSchema,
    )
    get_msg_data_model = create_restx_model_usingSchema(
        "ScheduleMsgDataListGetModel", shipper_operations_api_ns, MsgInfoSchema
    )
    complete_shipper_operation_data_model = shipper_operations_api_ns.model(
        "CompleteShipperOperationDataModel",
        {
            "shipper_operations_list": fields.List(
                fields.Nested(get_trsp_list_data_model)
            ),
        },
    )
    get_list_response_model = create_response_model(
        "ScheduleDataGetListResponseModel",
        shipper_operations_api_ns,
        "shipper_operations_list",
        complete_shipper_operation_data_model,
        list_type=True,
    )

    @shipper_operations_api_ns.doc(
        description=(
            "API-020 荷主向け運行案件検索・取得<br/>"
            "- デマンド・サイドからのみ利用可<br/>"
            "- cid（事業者）を指定しない場合には全事業者の検索を実施する"
        )
    )
    @shipper_operations_api_ns.response(400, "HTTP400エラー")
    @shipper_operations_api_ns.response(500, "HTTP500エラー")
    def get(self):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(endpoint, "shipper_operations")
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
            ret = {
                "shipper_operations_list": data.get("shipper_operations_list", []),
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "shipper_operations_list": [],
                "result": False,
                "error_msg": "error",
            }
        return ret, 200
