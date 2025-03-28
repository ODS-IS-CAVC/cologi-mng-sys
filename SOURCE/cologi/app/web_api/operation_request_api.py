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
import dateutil.parser

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
from com.company_info import COMPANY_INFOS, get_endpoint_from_cid
from com.vanning import Vanning


operation_request_api_ns = Namespace(
    "/webapi/v1/operation_request", description="キャリア向け運行依頼"
)

parser = operation_request_api_ns.parser()
parser.add_argument("q", type=str, help="クエリ文字列", required=False, location="args")
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

query_parser = create_query_parser(operation_request_api_ns)


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
        logger.debug(query_params)
        cid_key = "cid"
        if cid_key in query_params:
            cid = query_params[cid_key]
        else:
            cid = None
        logger.debug(f"API-030 キャリア向け運行依頼検索・取得 CID:{cid}")
        if cid is not None:
            url = urljoin(Config.CONNECTOR_PRIVATE_ENDPOINT, "operation_request")
            endpoint = get_endpoint_from_cid(cid)
            if endpoint is None:
                ret = {
                    "operation_request_list": [],
                    "total_num": 0,
                    "offset": 0,
                    "num": 0,
                    "result": False,
                    "error_msg": f"{cid} is invalid",
                }
                return ret, 400
            logger.debug(
                f"API-030 キャリア向け運行依頼検索・取得 CONNECT cid:{url} / {endpoint}"
            )
            headers = {"X-ENDPOINT": endpoint}
            try:
                response = requests.get(
                    url,
                    params=query_params,
                    verify=False,
                    proxies={"no_proxy": "co_logi_connector"},
                    headers=headers,
                )
                logger.debug(f"Response Code: {response.status_code}")
                response.encoding = response.apparent_encoding
                operation_request_list = response.json()
                ret = {
                    "operation_request_list": operation_request_list,
                    "total_num": len(operation_request_list),
                    "offset": 0,
                    "num": len(operation_request_list),
                    "result": True,
                    "error_msg": "",
                }
                status = 200
            except Exception as e:
                logger.error(e, exc_info=True, stack_info=True)
                ret = {
                    "operation_request_list": [],
                    "total_num": 0,
                    "offset": 0,
                    "num": 0,
                    "result": False,
                    "error_msg": "error",
                }
                status = 500
            return ret, status
        else:
            operation_request_list = []
            endpoint = ""
            for cid in COMPANY_INFOS:
                company = COMPANY_INFOS[cid]
                if company["role"] == "carrier":
                    endpoint = get_endpoint_from_cid(cid)
                    break
            url = urljoin(Config.CONNECTOR_PRIVATE_ENDPOINT, "operation_request")
            logger.debug(
                f"API-030 キャリア向け運行依頼検索・取得 CONNECT carrier:{url} / endpoint = {endpoint}"
            )
            headers = {"X-ENDPOINT": endpoint}
            try:
                response = requests.get(
                    url,
                    params=query_params,
                    verify=False,
                    proxies={"no_proxy": "co_logi_connector"},
                    headers=headers,
                )
                response.encoding = response.apparent_encoding
                data = response.json()
                operation_request_list = data.get("operation_request_list", [])
                status = 200
            except Exception as e:
                logger.error(e, exc_info=True, stack_info=True)
                status = 500
            ret = {
                "operation_request_list": operation_request_list,
                "total_num": len(operation_request_list),
                "offset": 0,
                "num": len(operation_request_list),
                "result": True,
                "error_msg": "",
            }
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
        logger.debug(query_params)
        cid = query_params.get("to_cid", None)
        from_cid = query_params.get("from_cid", None)
        if cid is None or from_cid is None:
            ret = {
                "result": False,
                "error_msg": "to_cid/from_cidを指定してください。",
            }
            return ret, 400
        if cid not in COMPANY_INFOS or from_cid not in COMPANY_INFOS:
            ret = {
                "result": False,
                "error_msg": "to_cid/from_cid が間違っています。",
            }
            return ret, 400
        logger.debug(f"API-031 キャリア向け運行申し込み登録 CID:{cid}")
        data = request.get_json()
        logger.debug(f"API-031 キャリア向け運行申し込み登録 {data}")
        url = urljoin(Config.CONNECTOR_PRIVATE_ENDPOINT, "operation_request/propose")
        endpoint = get_endpoint_from_cid(cid)
        if endpoint is None:
            ret = {
                "result": False,
                "error_msg": f"{cid}は不正です。",
            }
            return ret, 400
        logger.debug(f"CONNECT cid:{url} / {endpoint}")
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
            logger.debug(f"Response Code: {response.status_code}")
            response.encoding = response.apparent_encoding
            operation_request_data = response.json()
            ret = {
                "operation_request": operation_request_data.get(
                    "operation_request", []
                ),
                "result": True,
                "error_msg": "",
            }
            status = 200
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {"operation_request": {}, "result": False, "error_msg": "error"}
            status = 400
        logger.debug(f"API-031 キャリア向け運行申し込み登録 END status ={status}")
        return ret, status


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
        },
    )
    @operation_request_api_ns.response(200, "Success", post_response_model)
    @operation_request_api_ns.response(400, "HTTP400エラー")
    @operation_request_api_ns.response(500, "HTTP500エラー")
    def put(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        from_cid = query_params.get("from_cid", None)
        to_cid = query_params.get("to_cid", None)
        logger.debug(
            f"API-032 キャリア向け運行申し込み更新 from_cid:{from_cid}/to_cid:{to_cid}"
        )
        data = request.get_json()
        logger.debug(data)
        if from_cid is None or to_cid is None:
            ret = {
                "result": False,
                "error_msg": "from_cid/to_cid are required.",
                "operation_request": {},
            }
            return ret, 400
        if from_cid not in COMPANY_INFOS or to_cid not in COMPANY_INFOS:
            ret = {
                "result": False,
                "error_msg": "from_cid/to_cid are not valid.",
                "operation_request": {},
            }
            return ret, 400
        url = urljoin(
            Config.CONNECTOR_PRIVATE_ENDPOINT,
            f"operation_request/{operation_id}/propose/{propose_id}",
        )
        endpoint = get_endpoint_from_cid(from_cid)
        logger.debug(
            f"API-032 キャリア向け運行申し込み更新 CONNECT cid:{url} / {endpoint}"
        )
        headers = {"X-ENDPOINT": endpoint}
        try:
            response = requests.put(
                url,
                json=data,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "co_logi_connector"},
                headers=headers,
            )
            logger.debug(f"Response Code: {response.status_code}")
            response.encoding = response.apparent_encoding
            operation_request_data = response.json()
            ret = {
                "operation_request": operation_request_data.get(
                    "operation_request", []
                ),
                "result": True,
                "error_msg": "",
            }
            status = 200
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {"operation_request": {}, "result": False, "error_msg": "error"}
            status = 500
        logger.debug(f"API-032 キャリア向け運行申し込み更新 END Status:{status}")
        return ret, status


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
            "replay": "回答(required) true/false",
        },
    )
    @operation_request_api_ns.response(200, "Success", post_response_model)
    @operation_request_api_ns.response(400, "HTTP400エラー")
    @operation_request_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(f"API-033 キャリア向け運行申し込み更新（諾否回答）Start query_params={query_params}")
        from_cid = query_params.get("from_cid", None)
        to_cid = query_params.get("to_cid", None)
        logger.debug(
            f"API-033 キャリア向け運行申し込み更新（諾否回答）from_cid:{from_cid}/to_cid:{to_cid}"
        )
        data = request.get_json()
        logger.debug(f"API-033 キャリア向け運行申し込み更新（諾否回答）data={data}")
        if from_cid is None or to_cid is None:
            ret = {
                "result": False,
                "error_msg": "from_cid/to_cid are required.",
                "operation_request_reply": {},
            }
            return ret, 400
        if from_cid not in COMPANY_INFOS or to_cid not in COMPANY_INFOS:
            ret = {
                "result": False,
                "error_msg": "from_cid/to_cid are not valid.",
                "operation_request_reply": {},
            }
            return ret, 400
        url = urljoin(
            Config.CONNECTOR_PRIVATE_ENDPOINT,
            f"operation_request/{operation_id}/propose/{propose_id}/reply",
        )
        endpoint = get_endpoint_from_cid(from_cid)
        logger.debug(
            f"API-033 キャリア向け運行申し込み更新（諾否回答）CONNECT cid:{url} / {endpoint}"
        )
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
            logger.debug(
                f"API-033 キャリア向け運行申し込み更新（諾否回答） Response Code: {response.status_code}"
            )
            try:
                response.encoding = response.apparent_encoding
                data = response.json()
            except Exception:
                data = {"error_msg": "Backend error"}
            if response.status_code != 200:
                raise ValueError(data["error_msg"])
            ret = {
                "operation_request_reply": data.get("operation_request_reply", {}),
                "result": data.get("result", False),
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.error(e, exc_info=True, stack_info=True)
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
            f"API-033 キャリア向け運行申し込み更新（諾否回答） END status={status}"
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
        logger.debug(f"API-034 キャリア向け運行依頼情報連絡 Start query_params={query_params}")
        # パラメータチェック
        try:
            from_cid = query_params.get("from_cid", None)
            to_cid = query_params.get("to_cid", None)
            departure_mh = query_params.get("departure_mh", None)
            departure_mh_space_list = query_params.get("departure_mh_space_list", None)
            arrival_mh = query_params.get("arrival_mh", None)
            arrival_mh_space_list = query_params.get("arrival_mh_space_list", None)
            trailer_giais = query_params.get("trailer_giais", None)
            if (
                from_cid is None
                or to_cid is None
                or departure_mh is None
                or departure_mh_space_list is None
                or arrival_mh is None
                or arrival_mh_space_list is None
                or trailer_giais is None
            ):
                raise ValueError("Parameterが不足してます")
            if from_cid not in COMPANY_INFOS or to_cid not in COMPANY_INFOS:
                raise ValueError("from_cid/to_cid is not valid")
            departure_mh_space_list = departure_mh_space_list.split(",")
            arrival_mh_space_list = arrival_mh_space_list.split(",")
            trailer_giais = trailer_giais.split(",")
            logger.debug(
                "API-034 キャリア向け運行依頼情報連絡 " +
                f"query_params:departure_mh_space_list={departure_mh_space_list}/" +
                f"arrival_mh_space_list={arrival_mh_space_list}/trailer_giais={trailer_giais}"
            )
            if (
                len(departure_mh_space_list) < 1
                or len(arrival_mh_space_list) < 1
                or len(trailer_giais) < 1
            ):
                raise ValueError(
                    "Parameterが不正です。,区切りのリストを設定してください"
                )
            data = request.get_json()
            if "trsp_isr" not in data:
                raise ValueError("trsp_isrが見つかりません")
            if "trsp_instruction_id" not in data["trsp_isr"]:
                raise ValueError("trsp_instruction_idが見つかりません")
            trsp_instruction_id = data["trsp_isr"]["trsp_instruction_id"]
            if "cnee_prty" not in data:
                raise ValueError("cnee_prtyが見つかりません")
            if "cnee_prty_head_off_id" not in data["cnee_prty"]:
                raise ValueError("cnee_prty_head_off_idが見つかりません")
            recipient_cid = data["cnee_prty"]["cnee_prty_head_off_id"]
            if "cnsg_prty" not in data:
                raise ValueError("cnsg_prtyが見つかりません")
            if "cnsg_prty_head_off_id" not in data["cnsg_prty"]:
                raise ValueError("cnsg_prty_head_off_idが見つかりません")
            shipper_cid = data["cnsg_prty"]["cnsg_prty_head_off_id"]
            if "trsp_srvc" not in data:
                raise ValueError("trsp_srvcが見つかりません")
            trsp_srvc = data["trsp_srvc"]
            logger.debug(f"API-034 キャリア向け運行依頼情報連絡 data={data}")
            url = urljoin(
                Config.CONNECTOR_PRIVATE_ENDPOINT,
                f"operation_request/{operation_id}/propose/{propose_id}/handover_info",
            )
            endpoint = get_endpoint_from_cid(to_cid)
            logger.debug(f"API-034 キャリア向け運行依頼情報連絡 CONNECT cid:{url} / {endpoint}")
            headers = {"X-ENDPOINT": endpoint}
            response = requests.post(
                url,
                json=data,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "co_logi_connector"},
                headers=headers,
            )
            if response.status_code != 200:
                raise ValueError("Backend Error")
            logger.debug(f"API-034 キャリア向け運行依頼情報連絡 Response Code: {response.status_code}")
            response.encoding = response.apparent_encoding
            operation_request_data = response.json()
            if operation_request_data["result"] is False:
                raise ValueError("Backend Response Error")
            # 呼出しに成功したのでMHの計画を更新する。
            self.update_devanning_vanning_plan(
                from_cid,
                to_cid,
                departure_mh,
                departure_mh_space_list,
                arrival_mh,
                arrival_mh_space_list,
                trailer_giais,
                trsp_instruction_id,
                shipper_cid,
                recipient_cid,
                trsp_srvc,
            )
            ret = {
                "operation_request": operation_request_data.get(
                    "operation_request", []
                ),
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "error_msg": str(e.args[0]),
                "operation_request": {},
            }
            status = 400
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "error_msg": str(e.args[0]),
                "operation_request": {},
            }
            status = 400
        logger.debug(f"API-034 キャリア向け運行依頼情報連絡 End Status={status}")
        return ret, status

    def update_devanning_vanning_plan(
        self,
        from_cid,
        to_cid,
        departure_mh,
        departure_mh_space_list,
        arrival_mh,
        arrival_mh_space_list,
        trailer_giais,
        trsp_instruction_id,
        shipper_cid,
        recipient_cid,
        trsp_srvc,
    ):
        # 元々のキャリア(from_cid)のデータを削除する。
        vanning = Vanning()
        ## 出発MH
        vanning.delete_plan("devanning_plan", departure_mh, trsp_instruction_id)
        vanning.delete_plan("vanning_plan", departure_mh, trsp_instruction_id)
        ## 到着MH
        vanning.delete_plan("devanning_plan", arrival_mh, trsp_instruction_id)
        vanning.delete_plan("vanning_plan", arrival_mh, trsp_instruction_id)


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
            "shipper_cid": fields.String(
                example="490000002", description="荷主の事業者ID"
            ),
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
        },
    )
    @operation_request_api_ns.response(200, "Success", post_response_model)
    @operation_request_api_ns.response(400, "HTTP400エラー")
    @operation_request_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(f"API-035 キャリア向け運行実施確認通知 Start query_params={query_params}")
        from_cid = query_params.get("from_cid", None)
        logger.debug(f"API-035 キャリア向け運行実施確認通知 CID:{from_cid}")
        data = request.get_json()
        logger.debug(f"API-035 キャリア向け運行実施確認通知 data={data}")
        try:
            if from_cid is None:
                raise ValueError("Need from_cid")
            url = urljoin(
                Config.CONNECTOR_PRIVATE_ENDPOINT,
                f"operation_request/{operation_id}/propose/{propose_id}/notify",
            )
            endpoint = get_endpoint_from_cid(from_cid)
            logger.debug(f"API-035 キャリア向け運行実施確認通知 CONNECT cid:{url} / {endpoint}")
            headers = {"X-ENDPOINT": endpoint}
            response = requests.post(
                url,
                json=data,
                params=query_params,
                verify=False,
                proxies={"no_proxy": "co_logi_connector"},
                headers=headers,
            )
            logger.debug(f"API-035 キャリア向け運行実施確認通知 Response Code: {response.status_code}")
            response.encoding = response.apparent_encoding
            operation_request_data = response.json()
            ret = {
                "result": True,
                "error_msg": "",
            }
            status = 200
        except ValueError as e:
            logger.debug(f"API-035 キャリア向け運行実施確認通知 {str(e.args[0])}")
            ret = {
                "result": False,
                "error_msg": str(e.args[0]),
                "operation_request": {},
            }
            status = 400
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "error_msg": f"Error",
                "operation_request": {},
            }
            status = 500
        logger.debug(f"API-034 キャリア向け運行依頼情報連絡 End Status={status}")
        return ret, status
