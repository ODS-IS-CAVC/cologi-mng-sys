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
import requests
from flask import request
import logging

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from com.helper import create_restx_model_usingSchema, create_response_model
from model.reserve_model import ReserveSchema
from com.backend_api import BackendApi

reserve_api_ns = Namespace(
    "/public/api/reserve", description="予約（荷主向け運行申し込み）"
)


@reserve_api_ns.route("/")
@reserve_api_ns.doc(
    params={"cid": "事業者ID(required)", "endpoint": "相手のEndpoint(required)"}
)
class ReserveListApi(Resource):
    post_request_model = reserve_api_ns.model(
        "ReserveDataPostRequestModel",
        {
            "trsp_plan_id": fields.String(
                example="12345678901234567890",
                description="運送依頼番号",
                required=False,
            ),
            "operation_id": fields.String(
                example="12345678901234567890",
                description="システム内部の運送能力管理ID",
                required=True,
            ),
            "service_no": fields.String(
                example="123456789012345678901234",
                description="便・ダイヤ番号",
                required=False,
            ),
            "trsp_op_date_trm_strt_date": fields.String(
                example="20241024", description="運行開始日", required=True
            ),
            "trsp_op_trailer_id": fields.String(
                example="20241024",
                description="システム内部のトレーラID",
                required=False,
            ),
            "giai_number": fields.String(
                example="20241024", description="GIAI番号", required=False
            ),
            "trsp_op_plan_date_trm_strt_time": fields.String(
                example="1416", description="運行開始希望時刻", required=True
            ),
            "req_avb_from_time_of_cll_time": fields.String(
                example="null", description="申し込み集荷開始時間", required=False
            ),
            "req_avb_to_time_of_cll_time": fields.String(
                example="null", description="申し込み集荷終了時間", required=False
            ),
            "req_freight_rate": fields.String(
                example="1234567890", description="申し込み希望運賃", required=False
            ),
        },
    )
    post_data_model = reserve_api_ns.model(
        "ReserveDataPostModel",
        {
            "shipper_cid": fields.String(
                example="490000001", description="荷主の事業者ID"
            ),
            "carrier_cid": fields.String(
                example="491000002", description="キャリアの事業者ID"
            ),
            "propose_id": fields.String(
                example="4588193884384389349834934", description="提案ID"
            ),
        },
    )

    post_response_model = create_response_model(
        "ReserveDataPostResponseModel", reserve_api_ns, "reserve", post_data_model
    )

    @reserve_api_ns.doc(
        description=(
            "API-021 荷主向け運行申し込み登録<br/>"
            "- デマンド・サイドからのみ利用可<br/>"
        ),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
        },
    )
    @reserve_api_ns.response(200, "Success", post_response_model)
    @reserve_api_ns.response(400, "HTTP400エラー")
    @reserve_api_ns.response(500, "HTTP500エラー")
    def post(self):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        api = "shipper_operation_plans/propose"
        logger.debug(f"CONNECT BACKEND:{api}")
        try:
            data = request.get_json()
            logger.debug(data)
            backend_api = BackendApi()
            response = backend_api.call_api(
                api,
                method="POST",
                data=data,
                param=None,
            )
            if response is False:
                raise ValueError("Backend error")
            logger.debug(f"BACKEND RESPONSE: {response}")
            ret = {
                "reserve": response,
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "error_msg": "errror",
                "reserve": {},
            }
        return ret, 200


@reserve_api_ns.route("/<string:operation_id>/propose/<string:propose_id>/reply")
@reserve_api_ns.param("operation_id", "運行計画ID")
@reserve_api_ns.param("propose_id", "提案ID")
class ReserveNotifyApi(Resource):
    post_request_model = reserve_api_ns.model(
        "ReserveNotifyRequestModel",
        {
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
    post_response_data = reserve_api_ns.clone(
        "ReserveNotifyResponse",
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
        "ReserveNotifyResponseModel",
        reserve_api_ns,
        "reserve",
        post_response_data,
    )

    @reserve_api_ns.doc(
        description=(
            "API-024 荷主向け運行申し込み諾否回答通知<br/>"
            "- サプライ・サイドからのみ利用可<br/>"
        ),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "endpoint": "相手(荷主)のEndpoint(required)",
        },
    )
    @reserve_api_ns.response(200, "Success", post_response_model)
    @reserve_api_ns.response(400, "HTTP400エラー")
    @reserve_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        api = f"shipper_operation_plans/{operation_id}/propose/{propose_id}/reply"
        logger.debug(f"CONNECT BACKEND(Shipper):{api}")
        try:
            data = request.get_json()
            logger.debug(data)
            backend_api = BackendApi()
            response = backend_api.call_api(
                api,
                method="POST",
                data=data,
                param=query_params,
                is_shipper=True,
            )
            if response is False:
                raise ValueError("Backend error")
            logger.debug(f"BACKEND RESPONSE: {response}")
            ret = {
                "reserve": response,
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "reserve": {},
                "result": False,
                "error_msg": "error",
            }
        return ret, 200


@reserve_api_ns.route("/<string:operation_id>/propose/<string:propose_id>/notify")
@reserve_api_ns.param("operation_id", "運行計画ID")
@reserve_api_ns.param("propose_id", "提案ID")
class ReserveUpdateNotifyApi(Resource):
    post_request_model = reserve_api_ns.model(
        "ReserveUpdateNotifyPostData",
        {
            "trsp_op_date_id": fields.String(
                example="4588193884384389349834934",
                description="内部の運送能力管理ID",
                required=True,
            ),
            "service_no": fields.String(
                example="123456789012345678901234",
                description="便・ダイヤ番号",
                required=False,
            ),
            "trsp_op_date_trm_strt_date": fields.String(
                example="20241024", description="運行開始日", required=True
            ),
            "trsp_op_plan_date_trm_strt_time": fields.String(
                example="1416", description="運行開始希望時刻", required=True
            ),
            "req_avb_from_time_of_cll_time": fields.String(
                example="null", description="申し込み集荷開始時間", required=False
            ),
            "req_avb_to_time_of_cll_time": fields.String(
                example="null", description="申し込み集荷終了時間", required=False
            ),
            "req_freight_rate": fields.String(
                example="1234567890", description="申し込み希望運賃", required=False
            ),
        },
    )
    post_response_data = reserve_api_ns.clone(
        "ReserveUpdateNotifyPostResponseData",
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
        "ReserveUpdateResponseModel",
        reserve_api_ns,
        "reserve",
        post_response_data,
    )

    @reserve_api_ns.doc(
        description=(
            "API-026 荷主向け再提案情報登録通知<br/>"
            "- サプライ・サイドからのみ利用可<br/>"
        ),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
            "endpoint": "相手(荷主)のEndpoint(required)",
        },
    )
    @reserve_api_ns.response(200, "Success", post_response_model)
    @reserve_api_ns.response(400, "HTTP400エラー")
    @reserve_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        api = f"shipper_operation_plans/{operation_id}/propose/{propose_id}"
        logger.debug(f"CONNECT BACKEND(Shipper):{api}")
        try:
            data = request.get_json()
            logger.debug(data)
            backend_api = BackendApi()
            response = backend_api.call_api(
                api,
                method="PUT",
                data=data,
                param=query_params,
                is_shipper=True,
            )
            if response is False:
                raise ValueError("Backend error")
            logger.debug(f"BACKEND RESPONSE: {response}")
            ret = {
                "reserve": response,
                "result": True,
                "error_msg": "",
            }
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "reserve": {},
                "result": False,
                "error_msg": "error",
            }
        return ret, 200
