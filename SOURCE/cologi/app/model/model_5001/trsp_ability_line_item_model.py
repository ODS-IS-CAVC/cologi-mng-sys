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
from model.model_5001.road_carr_model import RoadCarr
from model.model_5001.logs_srvc_prv_model import LogsSrvcPrv
from model.model_5001.car_info_model import CarInfo
from model.model_5001.drv_info_model import DrvInfo


class TrspAbilityLineItem(db.Model):
    __tablename__ = "trsp_ability_line_item"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id．", autoincrement=True
    )
    # foreign key referencing other models
    road_carr_id = db.Column(
        db.Integer,
        db.ForeignKey("road_carr_5001.id"),
        nullable=False,
        doc="The unique id．",
    )
    logs_srvc_prv_id = db.Column(
        db.Integer,
        db.ForeignKey("logs_srvc_prv_5001.id"),
        nullable=False,
        doc="The unique id．",
    )
    car_info_id = db.Column(
        db.Integer, db.ForeignKey("car_info.id"), nullable=False, doc="The unique id．"
    )
    drv_info_id = db.Column(
        db.Integer, db.ForeignKey("drv_info.id"), nullable=False, doc="The unique id．"
    )

    road_carr = db.relationship(RoadCarr, backref="TrspAbilityLineItem", lazy=True)
    logs_srvc_prv = db.relationship(
        LogsSrvcPrv, backref="TrspAbilityLineItem", lazy=True
    )
    car_info = db.relationship(CarInfo, backref="TrspAbilityLineItem", lazy=True)
    drv_info = db.relationship(DrvInfo, backref="TrspAbilityLineItem", lazy=True)


class TrspAbilityLineItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrspAbilityLineItem
        load_instance = True
        include_fk = True
        exclude = (
            "id",
            "road_carr_id",
            "logs_srvc_prv_id",
            "car_info_id",
            "drv_info_id",
        )

    road_carr = ma.Nested(
        "model.model_5001.road_carr_model.RoadCarrSchema",
        metadata={"description": "the road carr for the trsp ability line item"},
    )
    logs_srvc_prv = ma.Nested(
        "model.model_5001.logs_srvc_prv_model.LogsSrvcPrvSchema",
        metadata={"description": "the logs srvc prv for the trsp ability line item"},
    )
    car_info = ma.List(
        ma.Nested(
            "model.model_5001.car_info_model.CarInfoSchema",
            metadata={"description": "the car info for the trsp ability line item"},
        )
    )
    drv_info = ma.List(
        ma.Nested(
            "model.model_5001.drv_info_model.DrvInfoSchema",
            metadata={"description": "the drv info for the trsp ability line item"},
        )
    )

    id = ma.auto_field(
        metadata={
            "description": TrspAbilityLineItem.__table__.c.id.doc,
            "max_length": 5,
        },
    )
    road_carr_id = ma.auto_field(
        metadata={
            "description": TrspAbilityLineItem.__table__.c.road_carr_id.doc,
            "max_length": 5,
        },
    )
    logs_srvc_prv_id = ma.auto_field(
        metadata={
            "description": TrspAbilityLineItem.__table__.c.logs_srvc_prv_id.doc,
            "max_length": 5,
        },
    )
    car_info_id = ma.auto_field(
        metadata={
            "description": TrspAbilityLineItem.__table__.c.car_info_id.doc,
            "max_length": 5,
        },
    )
    drv_info_id = ma.auto_field(
        metadata={
            "description": TrspAbilityLineItem.__table__.c.drv_info_id.doc,
            "max_length": 5,
        },
    )
