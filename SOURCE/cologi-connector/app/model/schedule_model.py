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


class ScheduleItem(db.Model):
    __tablename__ = "schedule_item"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )  # created to have a primary key
    service_no = db.Column(db.String(20), nullable=False, doc="便・ダイヤ番号")
    service_name = db.Column(db.String(48), nullable=False, doc="便・ダイヤ名称")
    service_strt_date = db.Column(db.String(8), nullable=False, doc="便の運行日")
    service_strt_time = db.Column(db.String(4), nullable=False, doc="便の運行時刻")
    service_end_date = db.Column(db.String(8), nullable=True, doc="便の運行終了日")
    service_end_time = db.Column(db.String(4), nullable=True, doc="便の運行終了時刻")
    provider_id = db.Column(db.String(48), nullable=True, doc="プロバイダー識別子")



class ScheduleItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        model = ScheduleItem
        load_instance = True
        exclude = ("id",)

    id = ma.auto_field(
        metadata={"description": ScheduleItem.__table__.c.id.doc, "max_length": 5}
    )
    service_no = ma.auto_field(
        metadata={
            "description": ScheduleItem.__table__.c.service_no.doc,
            "max_length": 20,
            "example": "123456789012345678901234",
        },
        validate=[validate.Length(max=20)],
    )
    service_name = ma.auto_field(
        metadata={
            "description": ScheduleItem.__table__.c.service_name.doc,
            "max_length": 48,
            "example": "東京～青森００１便",
        },
        validate=[validate.Length(max=48)],
    )
    service_strt_date = ma.auto_field(
        metadata={
            "description": ScheduleItem.__table__.c.service_strt_date.doc,
            "max_length": 8,
            "example": "20220101",
        },
        validate=[validate.Length(max=8)],
    )
    service_strt_time = ma.auto_field(
        metadata={
            "description": ScheduleItem.__table__.c.service_strt_time.doc,
            "max_length": 4,
            "example": "1030",
        },
        validate=[validate.Length(max=6)],
    )
    service_end_date = ma.auto_field(
        metadata={
            "description": ScheduleItem.__table__.c.service_end_date.doc,
            "max_length": 8,
            "example": "20220105",
        },
        validate=[validate.Length(max=8)],
    )
    service_end_time = ma.auto_field(
        metadata={
            "description": ScheduleItem.__table__.c.service_end_time.doc,
            "max_length": 6,
            "example": "1130",
        },
        validate=[validate.Length(max=6)],
    )
    provider_id = ma.auto_field(
        metadata={
            "description": ScheduleItem.__table__.c.provider_id.doc,
            "max_length": 48,
            "example": "AAAAAA",
        },
        validate=[validate.Length(max=48)],
    )
