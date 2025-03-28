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
from urllib.parse import urljoin
import logging
import json

logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from com.helper import create_restx_model_usingSchema, create_response_model
from model.reserve_model import ReserveSchema
from app.config import Config
from com.company_info import COMPANY_INFOS, get_endpoint_from_cid


reserve_api_ns = Namespace(
    "/webapi/v1/reserve", description="予約（荷主向け運行申し込み）"
)


@reserve_api_ns.route("/")
@reserve_api_ns.doc(params={"cid": "事業者ID(required)"})
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
        logger.debug(f"API-021 荷主向け運行申し込み登録 query_params={query_params}")
        carrier_cid = query_params.get("carrier_cid", None)
        shipper_cid = query_params.get("shipper_cid", None)
        logger.debug(f"API-021 荷主向け運行申し込み登録 carrier_cid:{carrier_cid}/shipper_cid{shipper_cid}")
        data = request.get_json()
        logger.debug(f"API-021 荷主向け運行申し込み登録 data={data}")
        try:
            if carrier_cid is None or shipper_cid is None:
                raise ValueError("carrier_cid/shipper_cid ared required")
            url = urljoin(Config.CONNECTOR_PRIVATE_ENDPOINT, "reserve")
            endpoint = get_endpoint_from_cid(carrier_cid)
            logger.debug(f"API-021 荷主向け運行申し込み登録 CONNECT cid:{url} / {endpoint}")
            headers = {"X-ENDPOINT": endpoint}
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
            reserve_data = response.json()
            ret = {
                "reserve": reserve_data.get("reserve", []),
                "result": True,
                "error_msg": "",
            }
            status = 200
        except requests.exceptions.RequestException as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "error_msg": "errror",
                "reserve": {},
            }
            status = 500
        except Exception as e:
            logger.debug(f"API-021 荷主向け運行申し込み登録 {str(e.args[0])}")
            ret = {
                "result": False,
                "error_msg": str(e.arg[0]),
                "reserve": {},
            }
            status = 400
        logger.debug(f"API-021 荷主向け運行申し込み登録 END status={status}")
        return ret, status


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
        },
    )
    @reserve_api_ns.response(200, "Success", post_response_model)
    @reserve_api_ns.response(400, "HTTP400エラー")
    @reserve_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        shipper_cid = query_params.get("shipper_cid",None)
        carrier_cid = query_params.get("carrier_cid",None)
        logger.debug(f"API-024 荷主向け運行申し込み諾否回答通知 shipper_cid:{shipper_cid}/carrier_cid:{carrier_cid}")
        data = request.get_json()
        logger.debug(f"API-024 荷主向け運行申し込み諾否回答通知 data={data}")
        try:
            if shipper_cid is None or carrier_cid is None:
                raise ValueError("shipper_cid/carrier_cidare required")
            url = urljoin(
                Config.CONNECTOR_PRIVATE_ENDPOINT,
                f"reserve/{operation_id}/propose/{propose_id}/reply",
            )
            endpoint = get_endpoint_from_cid(shipper_cid)
            logger.debug(f"CONNECT cid:{url} / {endpoint}")
            headers = {"X-ENDPOINT": endpoint}
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
            reserve_data = response.json()
            ret = {
                "result": True,
                "error_msg": "",
                "reserve": reserve_data.get("reserve", []),
            }
            status = 200
        except ValueError as e:
            ret = {
                "result": False,
                "error_msg": str(e.args[0]),
                "reserve": {},
            }
            status = 400
        except Exception as e:
            logger.error(e, exc_info=True, stack_info=True)
            ret = {
                "result": False,
                "error_msg": str(e.args[0]),
                "reserve": {},
            }
            status = 500
        logger.debug(f"API-024 荷主向け運行申し込み諾否回答通知 END status={status}")
        return ret, status


@reserve_api_ns.route("/<string:operation_id>/propose/<string:propose_id>")
@reserve_api_ns.param("operation_id", "運行計画ID")
@reserve_api_ns.param("propose_id", "提案ID")
class ReserveUpdateNotifyApi(Resource):
    post_request_model = reserve_api_ns.model(
        "ReserveUpdateNotifyPostData",
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
            "API-023 荷主向け運行申し込み更新通知（再提案登録）<br/>"
            "- サプライ・サイドからのみ利用可<br/>"
        ),
        params={
            "shipper_cid": "荷主の事業者ID(required)",
            "carrier_cid": "キャリアの事業者ID(required)",
        },
    )
    @reserve_api_ns.response(200, "Success", post_response_model)
    @reserve_api_ns.response(400, "HTTP400エラー")
    @reserve_api_ns.response(500, "HTTP500エラー")
    def put(self, operation_id, propose_id):
        test = {
            "result": True,
            "error_msg": "",
            "reserve": {
                "shipper_cid": "490000001",
                "carrier_cid": "491000002",
                "trsp_op_date_id": "4588193884384389349834934",
                "service_no": "123456789012345678901234",
                "trsp_op_date_trm_strt_date": "20241024",
                "trsp_op_plan_date_trm_strt_time": "1416",
                "req_avb_from_time_of_cll_time": "null",
                "req_avb_to_time_of_cll_time": "null",
                "req_freight_rate": "1234567890",
            },
        }
        return test, 200


@reserve_api_ns.route("/<string:operation_id>/propose/<string:propose_id>/notify")
@reserve_api_ns.param("operation_id", "運行計画ID")
@reserve_api_ns.param("propose_id", "提案ID")
class ReserveRequestNotifyApi(Resource):
    post_request_model = reserve_api_ns.model(
        "ReserveNotifyDataPostRequestModel",
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
    post_response_data = reserve_api_ns.clone(
        "ReserveRequestNotifyPostResponse",
        post_request_model,
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
        "ReserveRequestNotifyModel",
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
        },
    )
    @reserve_api_ns.response(200, "Success", post_response_model)
    @reserve_api_ns.response(400, "HTTP400エラー")
    @reserve_api_ns.response(500, "HTTP500エラー")
    def post(self, operation_id, propose_id):
        query_params = request.args.to_dict()
        logger.debug(query_params)
        cid_key = "shipper_cid"
        if cid_key in query_params:
            cid = query_params[cid_key]
        else:
            cid = None
        logger.debug(f"API-026 荷主向け再提案情報登録通知 CID:{cid}")
        data = request.get_json()
        logger.debug(f"API-026 荷主向け再提案情報登録通知 data={data}")
        if cid is not None:
            url = urljoin(
                Config.CONNECTOR_PRIVATE_ENDPOINT,
                f"reserve/{operation_id}/propose/{propose_id}/notify",
            )
            endpoint = get_endpoint_from_cid(cid)
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
                reserve_data = response.json()
                logger.debug(f"CONNECTOR RESPONSE:{json.dumps(reserve_data, indent=4)}")
                ret = {
                    "reserve": reserve_data.get("reserve", []),
                    "result": True,
                    "error_msg": "",
                }
            except requests.exceptions.RequestException as e:
                logger.error(e, exc_info=True, stack_info=True)
                ret = {
                    "result": False,
                    "error_msg": "error",
                    "reserve": {},
                }
        else:
            logger.debug(f"API-026 荷主向け再提案情報登録通知 {cid_key}はNullです。")
            ret = {
                "result": False,
                "error_msg": f"{cid_key}はNullです。",
                "reserve": {},
            }
        return ret, 200
