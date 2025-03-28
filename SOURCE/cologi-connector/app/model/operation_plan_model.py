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
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import db, ma


class OperationPlan(db.Model):
    __tablename__ = "operation_plan"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )  # created to have a primary key
    operation_id = db.Column(db.String(36), nullable=True, doc="運行計画ID")
    trsp_op_strt_area_line_one_txt = db.Column(
        db.String(40), nullable=False, doc="運行開始地域"
    )
    trsp_op_strt_area_cty_jis_cd = db.Column(
        db.String(5), nullable=True, doc="運行開始地域コード"
    )
    trsp_op_date_trm_strt_date = db.Column(
        db.String(8), nullable=False, doc="運行開始日"
    )
    trsp_op_plan_date_trm_strt_time = db.Column(
        db.String(4), nullable=False, doc="運行開始希望時刻"
    )
    trsp_op_end_area_line_one_txt = db.Column(
        db.String(40), nullable=False, doc="運行終了地域"
    )
    trsp_op_end_area_cty_jis_cd = db.Column(
        db.String(5), nullable=True, doc="運行終了地域コード"
    )
    trsp_op_date_trm_end_date = db.Column(
        db.String(8), nullable=False, doc="運行終了日"
    )
    trsp_op_plan_date_trm_end_time = db.Column(
        db.String(4), nullable=False, doc="運行終了希望時刻"
    )


class OperationPlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        model = OperationPlan
        load_instance = True
        exclude = ("id",)

    id = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.id.doc,
            "max_length": 5,
        }
    )
    operation_id = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.operation_id.doc,
            "max_length": 36,
            "example": "00112233-4455-6677-8899-aabbccddeeff",
        },
        validate=[validate.Length(max=36)],
    )
    trsp_op_strt_area_line_one_txt = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.trsp_op_strt_area_line_one_txt.doc,
            "max_length": 20,
            "example": "12345678901234567890",
        },
        validate=[validate.Length(max=20)],
    )
    trsp_op_strt_area_cty_jis_cd = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.trsp_op_strt_area_cty_jis_cd.doc,
            "max_length": 5,
            "example": "01101",
        },
        validate=[validate.Length(max=5)],
    )
    trsp_op_date_trm_strt_date = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.trsp_op_date_trm_strt_date.doc,
            "max_length": 8,
            "example": "20241024",
        },
        validate=[validate.Length(max=8)],
    )
    trsp_op_plan_date_trm_strt_time = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.trsp_op_plan_date_trm_strt_time.doc,
            "max_length": 4,
            "example": "1416",
        },
        validate=[validate.Length(max=4)],
    )
    trsp_op_end_area_line_one_txt = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.trsp_op_end_area_line_one_txt.doc,
            "max_length": 40,
            "example": "12345678901234567890",
        },
        validate=[validate.Length(max=40)],
    )
    trsp_op_end_area_cty_jis_cd = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.trsp_op_end_area_cty_jis_cd.doc,
            "max_length": 5,
            "example": "01102",
        },
        validate=[validate.Length(max=5)],
    )
    trsp_op_date_trm_end_date = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.trsp_op_date_trm_end_date.doc,
            "max_length": 8,
            "example": "20241025",
        },
        validate=[validate.Length(max=8)],
    )
    trsp_op_plan_date_trm_end_time = ma.auto_field(
        metadata={
            "description": OperationPlan.__table__.c.trsp_op_plan_date_trm_end_time.doc,
            "max_length": 4,
            "example": "1416",
        },
        validate=[validate.Length(max=4)],
    )
