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

import sys
import os
import time
import redis
from flask import (
    Flask,
    session,
    request,
    redirect,
    url_for,
    send_from_directory,
    has_request_context,
)
from flask_session import Session
from flask_restx import reqparse, abort, Api, Resource
from flask_cors import CORS
import logging
from flask.logging import default_handler

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.config import ConfigIns
from app.database import init_db

app = Flask(__name__)
CORS(app)
# セッション管理
app.secret_key = "COLOGI_SECRET_KEY_XXXXXXX"
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.from_url(ConfigIns.SESSION_DB_URL)
server_session = Session(app)
# ログ設定
app.logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler(ConfigIns.LOGFILE_NAME)
log_handler.setLevel(logging.DEBUG)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


formatter = RequestFormatter("[%(asctime)s] %(levelname)s : %(module)s: %(message)s")

default_handler.setFormatter(formatter)
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)
app.logger.info("自動運転支援道：共同輸送システムコネクタ Server start")
logger = logging.getLogger("app.flask")
logger.setLevel(logging.getLevelNamesMapping()[os.environ.get("LOGLEVEL", "DEBUG")])
log_handler = logging.FileHandler(ConfigIns.LOGFILE_NAME)
log_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] %(levelname)s : %(module)s / %(filename)s:%(lineno)d %(funcName)s: %(message)s"
    )
)
logger.addHandler(log_handler)

init_db(app)

# 各API登録
from app.private_api import private_api_blueprint
from app.public_api import public_api_blueprint

app.register_blueprint(private_api_blueprint, url_prefix="/private/api")
app.register_blueprint(public_api_blueprint, url_prefix="/public/api")


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    # リクエスト単位のセッションの終了時の処理があれば
    pass


@app.route("/healthcheck")
def healthcheck():
    return "healthcheck OK"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=81)
