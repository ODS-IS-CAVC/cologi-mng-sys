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

from flask import Blueprint
from flask_restx import Api
import os
import logging
from app.config import ConfigIns


web_api_blueprint = Blueprint("web_api", __name__)
web_api = Api(
    web_api_blueprint,
    title="COLOGI Web API",
    version="1.0",
    description="Web APIs for COLOGI",
    doc="/swagger/",
)

from .shipper_operations_api import shipper_operations_api_ns
from .reserve_api import reserve_api_ns
from .transport_plans_api import transport_plans_api_ns
from .operation_plans_api import operation_plans_api_ns
from .operation_request_api import operation_request_api_ns

web_api.add_namespace(shipper_operations_api_ns, path="/shipper_operations")
web_api.add_namespace(reserve_api_ns, path="/reserve")
web_api.add_namespace(transport_plans_api_ns, path="/transport_plans")
web_api.add_namespace(operation_plans_api_ns, path="/operation_plans")
web_api.add_namespace(operation_request_api_ns, path="/operation_request")
