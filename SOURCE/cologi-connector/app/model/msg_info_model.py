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
from marshmallow import fields, validate, ValidationError
from sqlalchemy.sql.sqltypes import CHAR
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import db, ma


class MsgInfo(db.Model):
    __tablename__ = "msg_info"
    msg_id = db.Column(db.Integer, primary_key=True, doc="データ処理ＮＯ．")
    msg_info_cls_typ_cd = db.Column(db.String(4), nullable=False, doc="情報区分コード")
    msg_date_iss_dttm = db.Column(db.String(8), nullable=True, doc="データ作成日")
    msg_time_iss_dttm = db.Column(db.Integer, nullable=True, doc="データ作成時刻")
    msg_fn_stas_cd = db.Column(
        CHAR(1), nullable=False, doc="訂正コード \n 1：新規、2：変更、3：取消"
    )
    note_dcpt_txt = db.Column(db.String(1000), nullable=True, doc="備考（漢字）")
    avb_load_cp_of_car_meas = db.Column(
        db.Numeric(precision=14, scale=3), nullable=True, doc="積載可能重量(kg)"
    )


class MsgInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MsgInfo
        load_instance = True

    msg_id = ma.auto_field(
        metadata={"description": MsgInfo.__table__.c.msg_id.doc, "max_length": 5},
        validate=[
            validate.Range(min=1, max=99999),
        ],
    )
    msg_info_cls_typ_cd = ma.auto_field(
        metadata={
            "description": MsgInfo.__table__.c.msg_info_cls_typ_cd.doc,
            "max_length": 4,
        },
        validate=[
            validate.Length(max=4),
        ],
    )
    msg_date_iss_dttm = ma.auto_field(
        metadata={
            "description": MsgInfo.__table__.c.msg_date_iss_dttm.doc,
            "max_length": 8,
            "example": "20241228",
        },
        validate=[
            validate.Length(max=8),
        ],
    )
    msg_time_iss_dttm = ma.auto_field(
        metadata={
            "description": MsgInfo.__table__.c.msg_time_iss_dttm.doc,
            "max_length": 6,
        },
        validate=[
            validate.Range(min=1, max=999999),
        ],
    )
    msg_fn_stas_cd = fields.String(
        metadata={
            "description": MsgInfo.__table__.c.msg_fn_stas_cd.doc,
            "max_length": 1,
            "example": "1",
        },
        validate=[
            validate.Length(equal=1),
        ],
    )
    note_dcpt_txt = ma.auto_field(
        metadata={
            "description": MsgInfo.__table__.c.note_dcpt_txt.doc,
            "max_length": 1000,
        },
        validate=[
            validate.Length(max=1000),
        ],
    )
    avb_load_cp_of_car_meas = fields.Decimal(
        as_string=True,
        metadata={
            "description": MsgInfo.__table__.c.avb_load_cp_of_car_meas.doc,
            "precision": 14,
            "scale": 3,
        },
    )
