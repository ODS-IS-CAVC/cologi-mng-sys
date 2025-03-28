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

from marshmallow import fields, validate, ValidationError
from database import db, ma
from sqlalchemy.sql.sqltypes import CHAR


class ShipToPrtyRqrm(db.Model):
    __tablename__ = "ship_to_prty_rqrm_3012_op"
    id = db.Column(db.Integer, primary_key=True, doc="The unique id")
    trms_of_car_size_cd = db.Column(
        db.CHAR(1),
        nullable=False,
        doc="車輌種別'1：小型（2t・3t）、2：中型（4t）、3：大型（10t）、4：特大（25t）、5：軽貨物、9：その他",
    )
    trms_of_car_hght_meas = db.Column(db.String(5), nullable=False, doc="車輌高さ制限")
    trms_of_gtp_cert_txt = db.Column(
        db.String(100), nullable=True, doc="入門条件（漢字）"
    )
    trms_of_del_txt = db.Column(db.String(80), nullable=True, doc="荷届条件（漢字）")
    trms_of_gods_hnd_txt = db.Column(
        db.String(80), nullable=True, doc="荷扱指示（漢字）"
    )
    anc_wrk_of_del_txt = db.Column(
        db.String(80), nullable=True, doc="配達附帯作業（漢字）"
    )
    spcl_wrk_txt = db.Column(db.String(80), nullable=True, doc="特別作業内容（漢字）")


class ShipToPrtyRqrmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShipToPrtyRqrm
        load_instance = True
        exclude = ("id",)

    id = ma.auto_field(
        metadata={
            "description": ShipToPrtyRqrm.__table__.c.id.doc,
            "max_length": 5,
        },
        validate=[validate.Range(min=1, max=3)],
    )
    trms_of_car_size_cd = ma.auto_field(
        metadata={
            "description": ShipToPrtyRqrm.__table__.c.trms_of_car_size_cd.doc,
            "max_length": 1,
        },
        validate=[
            validate.Length(max=1),
        ],
    )
    trms_of_car_hght_meas = ma.auto_field(
        metadata={
            "description": ShipToPrtyRqrm.__table__.c.trms_of_car_hght_meas.doc,
            "max_length": 5,
        },
        validate=[
            validate.Length(max=5),
        ],
    )
    trms_of_gtp_cert_txt = ma.auto_field(
        metadata={
            "description": ShipToPrtyRqrm.__table__.c.trms_of_gtp_cert_txt.doc,
            "max_length": 100,
        },
        validate=[
            validate.Length(max=100),
        ],
    )
    trms_of_del_txt = ma.auto_field(
        metadata={
            "description": ShipToPrtyRqrm.__table__.c.trms_of_del_txt.doc,
            "max_length": 80,
        },
        validate=[
            validate.Length(max=80),
        ],
    )
    trms_of_gods_hnd_txt = ma.auto_field(
        metadata={
            "description": ShipToPrtyRqrm.__table__.c.trms_of_gods_hnd_txt.doc,
            "max_length": 80,
        },
        validate=[
            validate.Length(max=80),
        ],
    )
    anc_wrk_of_del_txt = ma.auto_field(
        metadata={
            "description": ShipToPrtyRqrm.__table__.c.anc_wrk_of_del_txt.doc,
            "max_length": 80,
        },
        validate=[
            validate.Length(max=80),
        ],
    )
    spcl_wrk_txt = ma.auto_field(
        metadata={
            "description": ShipToPrtyRqrm.__table__.c.spcl_wrk_txt.doc,
            "max_length": 80,
        },
        validate=[
            validate.Length(max=80),
        ],
    )
