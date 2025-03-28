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
from model.operation_request_model import OperationRequestSchema
from model.model_3012_operation.trsp_plan_line_item_model import TrspPlanLineItemSchema
from app.config import Config
from com.company_info import COMPANY_INFOS

operation_request_api_ns = Namespace(
    "/private/api/operation_request", description="キャリア向け運行依頼"
)

parser = operation_request_api_ns.parser()
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
id_parser = operation_request_api_ns.parser()
id_parser.add_argument(
    "cid", type=str, help="事業者ID", required=False, location="args"
)

quer_parser = create_query_parser(operation_request_api_ns)


@operation_request_api_ns.route("/")
class OperationRequestListApi(Resource):
    get_list_data_model = create_restx_model_usingSchema(
        "OperationRequestDataListGetModel",
        operation_request_api_ns,
        TrspPlanLineItemSchema,
    )
    operation_request_attribute_model = operation_request_api_ns.model(
        "OperationRequestListResponseModel",
        {
            "cid": fields.String(example="490000001", description="事業者ID"),
            "trsp_plan_line_item": fields.List(fields.Nested(get_list_data_model)),
        },
    )
    get_list_response_model = create_response_model(
        "OperationRequestDataGetListResponseModel",
        operation_request_api_ns,
        "operation_request_list",
        operation_request_attribute_model,
        list_type=True,
    )

    @operation_request_api_ns.doc(
        description=(
            "API-030 キャリア向け運行依頼検索・取得<br/>"
            "- サプライ・サイドからのみ利用可<br/>"
            "- cid（事業者）を指定しない場合には全事業者の検索を実施する"
        )
    )
    @operation_request_api_ns.response(200, "Success", get_list_response_model)
    @operation_request_api_ns.response(400, "HTTP400エラー")
    @operation_request_api_ns.response(500, "HTTP500エラー")
    def get(self):
        query_params = request.args.to_dict()
        logger.debug(
            f"API-030 キャリア向け運行依頼検索・取得(Private) get:{query_params}"
        )
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(endpoint, "operation_request")
        try:
            logger.debug(
                f"API-030 キャリア向け運行依頼検索・取得(Private) CONNECT:{url}"
            )
            response = requests.get(
                url,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "localhost"},
            )
            if response.status_code != 200:
                raise ValueError("Backend Error")
            response.encoding = response.apparent_encoding
            data = response.json()
            ret = {
                "operation_request_list": data.get("operation_request_list", []),
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_request_list": [],
                "result": False,
                "error_msg": "Backend Error",
            }
            status = 400
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_request_list": [],
                "result": False,
                "error_msg": "error",
            }
            status = 500
        logger.debug(
            f"API-030 キャリア向け運行依頼検索・取得(Private) End status= {status}"
        )
        return ret, status


@operation_request_api_ns.route("/propose")
class OperationRequestProposeListApi(Resource):
    post_request_model = operation_request_api_ns.model(
        "OperationRequestProposalRequestModel",
        {
            "trsp_plan_id": fields.String(
                example="12345678901234567890",
                description="運送依頼番号",
                required=True,
            ),
            "operation_id": fields.String(
                example="12345678901234567890",
                description="システム内部の運送能力管理ID",
                required=True,
            ),
            "service_no": fields.String(
                example="123456789012345678901234",
                description="便・ダイヤ番号",
                required=True,
            ),
            "trsp_op_date_trm_strt_date": fields.String(
                example="20241024", description="運行開始日", required=True
            ),
            "trsp_op_plan_date_trm_strt_time": fields.String(
                example="1416", description="運行開始希望時刻", required=True
            ),
            "trsp_op_date_trm_end_date": fields.String(
                example="20241024", description="トラックの運行終了日", required=False
            ),
            "trsp_op_plan_date_trm_end_time": fields.String(
                example="1730", description="トラックの運行終了可能時刻", required=False
            ),
            "trsp_op_trailer_id": fields.String(
                example="20241024",
                description="システム内部のトレーラID",
                required=False,
            ),
            "giai_number": fields.String(
                example="202410242222", description="GIAI番号", required=False
            ),
            "req_freight_rate": fields.String(
                example="1234567890", description="申し込み希望運賃", required=False
            ),
        },
    )
    post_response_data = operation_request_api_ns.model(
        "OperationRequestProposalResponse",
        {
            "from_cid": fields.String(
                example="490000001", description="依頼元の事業者ID"
            ),
            "to_cid": fields.String(
                example="490000002",
                description="依頼先(申し込みを受ける側・回答する側)の事業者ID",
            ),
            "propose_id": fields.String(
                example="4588193884384389349834934", description="提案ID"
            ),
        },
    )
    post_response_model = create_response_model(
        "OperationRequestProposeListDataPostResponseModel",
        operation_request_api_ns,
        "operation_request",
        post_response_data,
    )

    @operation_request_api_ns.doc(
        description=(
            "API-031 キャリア向け運行申し込み登録<br/>"
            "- サプライ・サイドからのみ利用可<br/>"
        ),
        params={
            "from_cid": "依頼元の事業者ID(required)",
            "to_cid": "依頼先の事業者ID(required)",
        },
    )
    @operation_request_api_ns.response(200, "Success", post_response_model)
    @operation_request_api_ns.response(400, "HTTP400エラー")
    @operation_request_api_ns.response(500, "HTTP500エラー")
    def post(self):
        query_params = request.args.to_dict()
        logger.debug(
            f"API-031 キャリア向け運行申し込み登録(Private) Start query_params={query_params}"
        )
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(endpoint, "operation_request/propose")
        try:
            logger.debug(f"API-031 キャリア向け運行申し込み登録(Private) CONNECT:{url}")
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
                raise ValueError("Backend Error")
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
            ret = {
                "operation_request": data.get("operation_request", []),
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_request": [],
                "result": False,
                "error_msg": "Backend Error",
            }
            status = 400
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_request": {},
                "result": False,
                "error_msg": "error",
            }
            status = 500
        logger.debug(
            f"API-031 キャリア向け運行申し込み登録(Private) END status={status}"
        )
        return ret, 200


@operation_request_api_ns.route("/<string:operation_id>/propose/<string:propose_id>")
@operation_request_api_ns.param("operation_id", "運行計画ID")
@operation_request_api_ns.param("propose_id", "提案ID")
class OperationRequestProposeApi(Resource):
    post_request_model = operation_request_api_ns.model(
        "OperationRequestProposalPutRequestModel",
        {
            "trsp_plan_id": fields.String(
                example="12345678901234567890",
                description="運送依頼番号",
                required=True,
            ),
            "operation_id": fields.String(
                example="12345678901234567890",
                description="システム内部の運送能力管理ID",
                required=True,
            ),
            "service_no": fields.String(
                example="123456789012345678901234",
                description="便・ダイヤ番号",
                required=True,
            ),
            "trsp_op_date_trm_strt_date": fields.String(
                example="20241024", description="運行開始日", required=True
            ),
            "trsp_op_plan_date_trm_strt_time": fields.String(
                example="1416", description="運行開始希望時刻", required=True
            ),
            "trsp_op_date_trm_end_date": fields.String(
                example="20241024", description="トラックの運行終了日", required=False
            ),
            "trsp_op_plan_date_trm_end_time": fields.String(
                example="1730", description="トラックの運行終了可能時刻", required=False
            ),
            "trsp_op_trailer_id": fields.String(
                example="20241024",
                description="システム内部のトレーラID",
                required=False,
            ),
            "giai_number": fields.String(
                example="202410242222", description="GIAI番号", required=False
            ),
            "req_freight_rate": fields.String(
                example="1234567890", description="申し込み希望運賃", required=False
            ),
        },
    )
    post_response_data = operation_request_api_ns.clone(
        "OperationRequestProposalPutResponse",
        post_request_model,
        {
            "from_cid": fields.String(
                example="490000001", description="依頼元の事業者ID"
            ),
            "to_cid": fields.String(
                example="490000002",
                description="依頼先(申し込みを受ける側・回答する側)の事業者ID",
            ),
        },
    )
    post_response_model = create_response_model(
        "OperationRequestProposeDataPutResponseModel",
        operation_request_api_ns,
        "operation_request",
        post_response_data,
    )

    @operation_request_api_ns.doc(
        description=(
            "API-032 キャリア向け運行申し込み更新<br/>"
            "- サプライ・サイドからのみ利用可<br/>"
        ),
        params={
            "from_cid": "依頼元の事業者ID(required)",
            "to_cid": "依頼先の事業者ID(required)",
            "to_endpoint": "相手(依頼先)のEndpoint(required)",
        },
    )
    @operation_request_api_ns.response(200, "Success", post_response_model)
    @operation_request_api_ns.response(400, "HTTP400エラー")
    @operation_request_api_ns.response(500, "HTTP500エラー")
    def put(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(
            endpoint,
            f"operation_request/{operation_id}/propose/{propose_id}",
        )
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
                "operation_request": data.get("operation_request", []),
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_request": {},
                "result": False,
                "error_msg": "error",
            }
        return ret, 200


@operation_request_api_ns.route(
    "/<string:operation_id>/propose/<string:propose_id>/reply"
)
@operation_request_api_ns.param("operation_id", "運行計画ID")
@operation_request_api_ns.param("propose_id", "提案ID")
class OperationRequestReplyApi(Resource):
    post_request_model = operation_request_api_ns.model(
        "OperationRequestReplyRequestModel",
        {
            "trsp_plan_id": fields.String(
                example="12345678901234567890",
                description="運送依頼番号",
                required=False,
            ),
            "operation_id": fields.String(
                example="12345678901234567890",
                description="運行計画ID",
                required=True,
                max_length=20,
            ),
            "approval": fields.Boolean(
                example=True, description="承認", required=True
            ),  # description added by myself as not provided
        },
    )
    post_response_data = operation_request_api_ns.clone(
        "OperationRequestReplyResponse",
        post_request_model,
        {
            "from_cid": fields.String(
                example="490000001", description="依頼元の事業者ID"
            ),
            "to_cid": fields.String(
                example="490000002",
                description="依頼先(申し込みを受ける側・回答する側)の事業者ID",
            ),
        },
    )
    post_response_model = create_response_model(
        "OperationRequestResponseModel",
        operation_request_api_ns,
        "operation_request_reply",
        post_response_data,
    )

    @operation_request_api_ns.doc(
        description=(
            "API-033 キャリア向け運行申し込み更新（諾否回答）<br/>"
            "- サプライ・サイドからのみ利用可<br/>"
        ),
        params={
            "from_cid": "依頼元の事業者ID(required)",
            "to_cid": "依頼先(申し込みを受ける側・回答する側)の事業者ID(required)",
            "to_endpoint": "相手(依頼先)のEndpoint(required)",
            "replay": "回答(required) true/false",
        },
    )
    @operation_request_api_ns.response(200, "Success", post_response_model)
    @operation_request_api_ns.response(400, "HTTP400エラー")
    @operation_request_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(
            f"API-033 キャリア向け運行申し込み更新（諾否回答）(Private) Start query_params={query_params}"
        )
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(
            endpoint,
            f"operation_request/{operation_id}/propose/{propose_id}/reply",
        )
        try:
            logger.debug(
                f"API-033 キャリア向け運行申し込み更新（諾否回答）(Private) CONNECT:{url}"
            )
            data = request.get_json()
            logger.debug(data)
            response = requests.post(
                url,
                json=data,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "localhost"},
            )
            try:
                response.encoding = response.apparent_encoding
                data = response.json()
            except Exception:
                data = {"error_msg": "Backend Error"}
            if response.status_code != 200:
                raise ValueError(data["error_msg"])
            logger.debug(
                f"API-033 キャリア向け運行申し込み更新（諾否回答）(Private) CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}"
            )
            ret = {
                "operation_request_reply": data.get("operation_request_reply", []),
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.error(e)
            ret = {
                "operation_request_reply": {},
                "result": False,
                "error_msg": str(e.args[0]),
            }
            status = 400
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_request_reply": {},
                "result": False,
                "error_msg": "error",
            }
            status = 500
        logger.debug(
            f"API-033 キャリア向け運行申し込み更新（諾否回答）(Private) END status={status}"
        )
        return ret, status


@operation_request_api_ns.route(
    "/<string:operation_id>/propose/<string:propose_id>/handover_info"
)
@operation_request_api_ns.param("operation_id", "運行計画ID")
@operation_request_api_ns.param("propose_id", "提案ID")
class OperationRequestHandoverInfoApi(Resource):
    post_request_model = create_restx_model_usingSchema(
        "OperationRequestHandoverInfoPostRequestModel",
        operation_request_api_ns,
        TrspPlanLineItemSchema,
    )
    post_response_data = operation_request_api_ns.clone(
        "OperationRequestHandoverInfoPostResponse",
        post_request_model,
        {
            "from_cid": fields.String(
                example="490000001", description="依頼元の事業者ID"
            ),
            "to_cid": fields.String(
                example="490000002",
                description="依頼先(申し込みを受ける側・回答する側)の事業者ID",
            ),
            "propose_id": fields.String(
                example="4588193884384389349834934", description="提案ID"
            ),
        },
    )
    post_response_model = create_response_model(
        "OperationRequestHandoverInfoModel",
        operation_request_api_ns,
        "operation_request",
        post_response_data,
    )

    @operation_request_api_ns.doc(
        description=(
            "API-034 キャリア向け運行依頼情報連絡<br/>"
            "- サプライ・サイドからのみ利用可<br/>"
            "- MH情報、荷物の情報、トレーラー情報を依頼先のキャリアに連絡<br/>"
        ),
        params={
            "from_cid": "依頼元の事業者ID(required)",
            "to_cid": "依頼先(申し込みを受ける側・回答する側)の事業者ID(required)",
            "source_endpoint": "呼出し元のEndpoint(required)",
            "departure_mh": "出発MHのGLN(required)",
            "departure_mh_space_list": "出発MHの駐車枠の配列(required)",
            "arrival_mh": "到着MHのGLN(required)",
            "arrival_mh_space_list": "到着MHの駐車枠の配列(required)",
            "trailer_giais": "荷物のトレーラーのGIAIの配列(required)",
        },
    )
    @operation_request_api_ns.response(200, "Success", post_response_model)
    @operation_request_api_ns.response(400, "HTTP400エラー")
    @operation_request_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(
            f"API-034 キャリア向け運行依頼情報連絡(PRIVATE) query_params={query_params}"
        )
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(
            endpoint,
            f"operation_request/{operation_id}/propose/{propose_id}/handover_info",
        )
        logger.debug(
            f"API-034 キャリア向け運行依頼情報連絡(PRIVATE) CONNECT PUBLIC CONNECTOR:{url}"
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
                raise ValueError("Backend Error")
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
            ret = {
                "operation_request": data.get("operation_request", []),
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_request": [],
                "result": False,
                "error_msg": "Backend Error",
            }
            status = 400
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_request": [],
                "result": False,
                "error_msg": "errror",
            }
            status = 500
        logger.debug(
            f"API-034 キャリア向け運行依頼情報連絡(PRIVATE) END status={status}"
        )
        return ret, status


@operation_request_api_ns.route(
    "/<string:operation_id>/propose/<string:propose_id>/notify"
)
@operation_request_api_ns.param("operation_id", "運行計画ID")
@operation_request_api_ns.param("propose_id", "提案ID")
class OperationRequestNotifyApi(Resource):
    post_request_model = create_restx_model_usingSchema(
        "OperationRequestNotifyPostRequestModel",
        operation_request_api_ns,
        TrspPlanLineItemSchema,
    )
    post_response_data = operation_request_api_ns.clone(
        "OperationRequestNotifyPostResponse",
        post_request_model,
        {
            "from_cid": fields.String(
                example="490000001", description="依頼元の事業者ID"
            ),
            "to_cid": fields.String(
                example="490000002",
                description="依頼先(申し込みを受ける側・回答する側)の事業者ID",
            ),
            "propose_id": fields.String(
                example="4588193884384389349834934", description="提案ID"
            ),
        },
    )
    post_response_model = create_response_model(
        "OperationRequestNotifyModel",
        operation_request_api_ns,
        "operation_request",
        post_response_data,
    )

    @operation_request_api_ns.doc(
        description=(
            "API-035 キャリア向け運行実施確認通知<br/>"
            "- サプライ・サイドからのみ利用可<br/>"
            "- 基本的にAPI-043と同等だがキャリア間連携用<br/>"
        ),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "from_cid": "依頼元の事業者ID(required)",
            "to_cid": "依頼先(申し込みを受ける側・回答する側)の事業者ID(required)",
            "to_endpoint": "相手(依頼先)のEndpoint(required)",
        },
    )
    @operation_request_api_ns.response(200, "Success", post_response_model)
    @operation_request_api_ns.response(400, "HTTP400エラー")
    @operation_request_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        endpoint = request.headers.get("X-ENDPOINT")
        url = urljoin(
            endpoint,
            f"operation_request/{operation_id}/propose/{propose_id}/notify",
        )
        logger.debug(f"CONNECT PUBLIC CONNECTOR:{url}")
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
            response.encoding = response.apparent_encoding
            data = response.json()
            logger.debug(f"CONNECTOR RESOPNSE:{json.dumps(data, indent=4)}")
            ret = {
                "operation_request": data.get("operation_request", []),
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "operation_request": [],
                "result": False,
                "error_msg": "errror",
            }
        return ret, 200
