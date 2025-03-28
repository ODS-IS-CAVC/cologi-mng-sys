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

import os


class Config:
    # session管理用のRedis DBのURL
    SESSION_DB_URL = "redis://redis:6379"
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4".format(
            **{
                "user": os.getenv("COLOGI_DB_USER_NAME", "cologi"),
                "password": os.getenv("COLOGI_DB_USER_PASSWORD"),
                "host": "db",
                "database": os.getenv("COLOGI_DB_NAME", "cologidb"),
            }
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SERVER_ROLE = "supply"  # demand or supply or openapi
    BACKEND_ENDPOINT = "https://XXXXXXXXXX/api/v1/" # supply
    LOGFILE_NAME = "/log/debug.log"
    CONNECTOR_PRIVATE_ENDPOINT = "https://co_logi_connector/private/api/"
    MH_MNG_ENDPOINT = "http://XXXXXXXXXXX/mhapi/v1/"
    TRUST_MNG_ENDPOINT = "http://XXXXXXXXXXXXX/api/"


ConfigIns = Config()
