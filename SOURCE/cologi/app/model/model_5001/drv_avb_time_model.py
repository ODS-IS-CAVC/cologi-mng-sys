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
from marshmallow import validate
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import db, ma


class DrvAvbTime(db.Model):
    __tablename__ = "drv_avb_time"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )
    drv_avb_from_date = db.Column(db.String(8), nullable=False, doc="稼働開始予定日")
    drv_avb_from_time_of_wrkg_time = db.Column(
        db.String(4), nullable=False, doc="稼働開始予定時間"
    )
    drv_avb_to_date = db.Column(db.String(8), nullable=False, doc="稼働終了予定日")
    drv_avb_to_time_of_wrkg_time = db.Column(
        db.String(4), nullable=False, doc="稼働終了予定時間"
    )
    drv_wrkg_trms_txt = db.Column(db.String(40), nullable=False, doc="その他稼働条件")
    drv_frmr_optg_date = db.Column(db.String(8), nullable=False, doc="直前運行日")
    drv_frmr_op_end_time = db.Column(
        db.String(4), nullable=False, doc="直前運行終了時間"
    )


class DrvAvbTimeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DrvAvbTime
        load_instance = True
        exclude = ("id",)

    id = ma.auto_field(
        metadata={"description": DrvAvbTime.__table__.c.id.doc, "max_length": 5}
    )
    drv_avb_from_date = ma.auto_field(
        metadata={
            "description": DrvAvbTime.__table__.c.drv_avb_from_date.doc,
            "max_length": 8,
        },
        validate=[validate.Length(max=8)],
    )
    drv_avb_from_time_of_wrkg_time = ma.auto_field(
        metadata={
            "description": DrvAvbTime.__table__.c.drv_avb_from_time_of_wrkg_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    drv_avb_to_date = ma.auto_field(
        metadata={
            "description": DrvAvbTime.__table__.c.drv_avb_to_date.doc,
            "max_length": 8,
        },
        validate=[validate.Length(max=8)],
    )
    drv_avb_to_time_of_wrkg_time = ma.auto_field(
        metadata={
            "description": DrvAvbTime.__table__.c.drv_avb_to_time_of_wrkg_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    drv_wrkg_trms_txt = ma.auto_field(
        metadata={
            "description": DrvAvbTime.__table__.c.drv_wrkg_trms_txt.doc,
            "max_length": 40,
        },
        validate=[validate.Length(max=40)],
    )
    drv_frmr_optg_date = ma.auto_field(
        metadata={
            "description": DrvAvbTime.__table__.c.drv_frmr_optg_date.doc,
            "max_length": 8,
        },
        validate=[validate.Length(max=8)],
    )
    drv_frmr_op_end_time = ma.auto_field(
        metadata={
            "description": DrvAvbTime.__table__.c.drv_frmr_op_end_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
