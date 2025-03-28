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
from marshmallow import fields, validate
from sqlalchemy.sql.sqltypes import CHAR
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import db, ma
from model.model_5001.drv_avb_time_model import DrvAvbTime


class DrvInfo(db.Model):
    __tablename__ = "drv_info"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )
    drv_ctrl_num_id = db.Column(db.String(12), nullable=True, doc="運転手管理コード")
    drv_cls_of_drvg_license_cd = db.Column(
        CHAR(15), nullable=True, doc="免許種類コード\n 物流情報標準項目コード: "
    )
    drv_cls_of_fkl_license_exst_cd = db.Column(
        CHAR(1), nullable=True, doc="フォークリフト免許\n 物流情報標準項目コード: "
    )
    drv_rmk_about_drv_txt = db.Column(
        db.String(40), nullable=True, doc="その他リソース情報"
    )
    drv_cmpn_name_of_gtp_crtf_exst_txt = db.Column(
        db.String(200), nullable=True, doc="運転手入門証保有"
    )
    drv_avb_time_id = db.Column(
        db.Integer,
        db.ForeignKey("drv_avb_time.id"),
        nullable=False,
        doc="The unique id．",
    )
    drv_avb_time = db.relationship(DrvAvbTime, backref="DrvInfo", lazy=True)


class DrvInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DrvInfo
        load_instance = True
        exclude = ("id", "drv_avb_time_id")

    drv_avb_time = ma.List(
        ma.Nested(
            "model.model_5001.drv_avb_time_model.DrvAvbTimeSchema",
            metadata={
                "description": "the drv avb time for the drv info in trsp ability line item"
            },
        )
    )

    id = ma.auto_field(
        metadata={"description": DrvInfo.__table__.c.id.doc, "max_length": 5}
    )
    drv_ctrl_num_id = ma.auto_field(
        metadata={
            "description": DrvInfo.__table__.c.drv_ctrl_num_id.doc,
            "max_length": 12,
        },
        validate=[
            validate.Length(max=12),
        ],
    )
    drv_cls_of_drvg_license_cd = fields.String(
        metadata={
            "description": DrvInfo.__table__.c.drv_cls_of_drvg_license_cd.doc,
            "max_length": 15,
            "example": "100000000000000",
        },
        validate=[
            validate.Length(equal=15),
        ],
    )
    drv_cls_of_fkl_license_exst_cd = fields.String(
        metadata={
            "description": DrvInfo.__table__.c.drv_cls_of_fkl_license_exst_cd.doc,
            "max_length": 1,
            "example": "1",
        },
        validate=[
            validate.Length(equal=1),
        ],
    )
    drv_rmk_about_drv_txt = ma.auto_field(
        metadata={
            "description": DrvInfo.__table__.c.drv_rmk_about_drv_txt.doc,
            "max_length": 40,
        },
        validate=[
            validate.Length(max=40),
        ],
    )
    drv_cmpn_name_of_gtp_crtf_exst_txt = ma.auto_field(
        metadata={
            "description": DrvInfo.__table__.c.drv_cmpn_name_of_gtp_crtf_exst_txt.doc,
            "max_length": 200,
        },
        validate=[
            validate.Length(max=200),
        ],
    )
    drv_avb_time_id = ma.auto_field(
        metadata={
            "description": DrvInfo.__table__.c.drv_avb_time_id.doc,
            "max_length": 5,
        },
    )
    drv_avb_time_id = ma.auto_field(
        metadata={
            "description": DrvInfo.__table__.c.drv_avb_time_id.doc,
            "max_length": 5,
        },
    )
