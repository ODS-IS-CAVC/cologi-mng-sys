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

from datetime import datetime, date, time
from sqlalchemy.sql.sqltypes import CHAR
from marshmallow import fields, validate
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import db, ma


class FreeTimeInfo(db.Model):
    __tablename__ = "free_time_Info"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )
    free_time = db.Column(db.String(4), nullable=False, doc="フリータイム時間")
    free_time_fee = db.Column(db.String(4), nullable=True, doc="フリータイム料金")


class FreeTimeInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FreeTimeInfo
        load_instance = True
        exclude = ("id",)

    id = ma.auto_field(
        metadata={"description": FreeTimeInfo.__table__.c.id.doc, "max_length": 5}
    )
    free_time = ma.auto_field(
        metadata={
            "description": FreeTimeInfo.__table__.c.free_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    free_time_fee = ma.auto_field(
        metadata={
            "description": FreeTimeInfo.__table__.c.free_time_fee.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
