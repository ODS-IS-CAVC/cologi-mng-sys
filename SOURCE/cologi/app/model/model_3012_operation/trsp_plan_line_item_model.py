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
from model.model_3012_operation.trsp_isr_model import TrspIsr
from model.model_3012_operation.trsp_srvc_model import TrspSrvc
from model.model_3012_operation.trsp_vehicle_trms_model import TrspVehicleTrms
from model.model_3012_operation.del_info_model import DelInfo
from model.model_3012_operation.cns_model import Cns
from model.model_3012_operation.cns_line_item_model import CnsLineItem
from model.model_3012_operation.cnsg_prty_model import CnsgPrty
from model.model_3012_operation.trsp_rqr_prty_model import TrspRqrPrty
from model.model_3012_operation.cnee_prty_model import CneePrty
from model.model_3012_operation.logs_srvc_prv_model import LogsSrvcPrv
from model.model_3012_operation.road_carr_model import RoadCarr
from model.model_3012_operation.fret_clim_to_prty_model import FretClimToPrty
from model.model_3012_operation.ship_from_prty_model import ShipFromPrty
from model.model_3012_operation.ship_to_prty_model import ShipToPrty


class TrspPlanLineItem(db.Model):
    __tablename__ = "trsp_plan_line_item_3012_op"
    trsp_plan_line_item_id = db.Column(
        db.Integer, primary_key=True, doc="The primary key"
    )
    # foreign key referencing other models
    trsp_isr_id = db.Column(
        db.Integer,
        db.ForeignKey("trsp_isr_3012_op.trsp_instruction_id"),
        nullable=False,
        doc="The unique id．",
    )
    trsp_srvc_id = db.Column(
        db.Integer,
        db.ForeignKey("trsp_srvc_3012_op.trsp_srvc_id"),
        nullable=False,
        doc="The unique id．",
    )
    trsp_vehicle_trms_id = db.Column(
        db.Integer,
        db.ForeignKey("trsp_vehicle_trms_3012_op.trsp_vehicle_trms_id"),
        nullable=False,
        doc="The unique id．",
    )
    del_info_id = db.Column(
        db.Integer,
        db.ForeignKey("del_info_3012_op.del_info_id"),
        nullable=False,
        doc="The unique id．",
    )
    cns_id = db.Column(
        db.Integer,
        db.ForeignKey("cns_3012_op.cns_id"),
        nullable=False,
        doc="The unique id．",
    )
    cns_line_item_id = db.Column(
        db.Integer,
        db.ForeignKey("cns_line_item_3012_op.cns_line_item_id"),
        nullable=False,
        doc="The unique id．",
    )
    cnsg_prty_id = db.Column(
        db.Integer,
        db.ForeignKey("cnsg_prty_3012_op.cnsg_prty_id"),
        nullable=False,
        doc="The unique id．",
    )
    trsp_rqr_prty_id = db.Column(
        db.Integer,
        db.ForeignKey("trsp_rqr_prty_3012_op.trsp_rqr_prty_id"),
        nullable=False,
        doc="The unique id．",
    )
    cnee_prty_id = db.Column(
        db.Integer,
        db.ForeignKey("cnee_prty_3012_op.cnee_prty_id"),
        nullable=False,
        doc="The unique id．",
    )

    logs_srvc_prv_id = db.Column(
        db.Integer,
        db.ForeignKey("logs_srvc_prv_3012_op.logs_srvc_prv_id"),
        nullable=False,
        doc="The unique id．",
    )
    road_carr_id = db.Column(
        db.Integer,
        db.ForeignKey("road_carr_3012_op.road_carr_id"),
        nullable=False,
        doc="The unique id．",
    )
    fret_clim_to_prty_id = db.Column(
        db.Integer,
        db.ForeignKey("fret_clim_to_prty_3012_op.fret_clim_to_prty_id"),
        nullable=False,
        doc="The unique id．",
    )
    ship_from_prty_id = db.Column(
        db.Integer,
        db.ForeignKey("ship_from_prty_3012_op.ship_from_prty_id"),
        nullable=False,
        doc="The unique id．",
    )
    ship_to_prty_id = db.Column(
        db.Integer,
        db.ForeignKey("ship_to_prty_3012_op.ship_to_prty_id"),
        nullable=False,
        doc="The unique id．",
    )

    trsp_isr = db.relationship(TrspIsr, backref="TrspPlanLineItem", lazy=True)
    trsp_srvc = db.relationship(TrspSrvc, backref="TrspPlanLineItem", lazy=True)
    trsp_vehicle_trms = db.relationship(
        TrspVehicleTrms, backref="TrspPlanLineItem", lazy=True
    )
    del_info = db.relationship(DelInfo, backref="TrspPlanLineItem", lazy=True)
    cns = db.relationship(Cns, backref="TrspPlanLineItem", lazy=True)
    cns_line_item = db.relationship(CnsLineItem, backref="TrspPlanLineItem", lazy=True)
    cnsg_prty = db.relationship(CnsgPrty, backref="TrspPlanLineItem", lazy=True)
    trsp_rqr_prty = db.relationship(TrspRqrPrty, backref="TrspPlanLineItem", lazy=True)
    cnee_prty = db.relationship(CneePrty, backref="TrspPlanLineItem", lazy=True)
    cns_line_item = db.relationship(CnsLineItem, backref="TrspPlanLineItem", lazy=True)
    logs_srvc_prv = db.relationship(LogsSrvcPrv, backref="TrspPlanLineItem", lazy=True)
    road_carr = db.relationship(RoadCarr, backref="TrspPlanLineItem", lazy=True)
    fret_clim_to_prty = db.relationship(
        FretClimToPrty, backref="TrspPlanLineItem", lazy=True
    )
    ship_from_prty = db.relationship(
        ShipFromPrty, backref="TrspPlanLineItem", lazy=True
    )
    ship_to_prty = db.relationship(ShipToPrty, backref="TrspPlanLineItem", lazy=True)


class TrspPlanLineItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrspPlanLineItem
        load_instance = True
        include_fk = True
        exclude = (
            "trsp_plan_line_item_id",
            "trsp_isr_id",
            "trsp_srvc_id",
            "trsp_vehicle_trms_id",
            "del_info_id",
            "cns_id",
            "cns_line_item_id",
            "cnsg_prty_id",
            "trsp_rqr_prty_id",
            "cnee_prty_id",
            "logs_srvc_prv_id",
            "road_carr_id",
            "fret_clim_to_prty_id",
            "ship_from_prty_id",
            "ship_to_prty_id",
        )

    trsp_isr = ma.Nested(
        "model.model_3012_operation.trsp_isr_model.TrspIsrSchema",
        metadata={"description": ""},
    )

    trsp_srvc = ma.Nested(
        "model.model_3012_operation.trsp_srvc_model.TrspSrvcSchema",
        metadata={"description": ""},
    )

    trsp_vehicle_trms = ma.Nested(
        "model.model_3012_operation.trsp_vehicle_trms_model.TrspVehicleTrmsSchema",
        metadata={"description": ""},
    )

    del_info = ma.Nested(
        "model.model_3012_operation.del_info_model.DelInfoSchema",
        metadata={"description": ""},
    )

    cns = ma.Nested(
        "model.model_3012_operation.cns_model.CnsSchema",
        metadata={"description": ""},
    )

    cns_line_item = ma.Nested(
        "model.model_3012_operation.cns_line_item_model.CnsLineItemSchema",
        metadata={"description": ""},
    )

    cnsg_prty = ma.Nested(
        "model.model_3012_operation.cnsg_prty_model.CnsgPrtySchema",
        metadata={"description": ""},
    )

    trsp_rqr_prty = ma.Nested(
        "model.model_3012_operation.trsp_rqr_prty_model.TrspRqrPrtySchema",
        metadata={"description": ""},
    )

    cnee_prty = ma.Nested(
        "model.model_3012_operation.cnee_prty_model.CneePrtySchema",
        metadata={"description": ""},
    )

    logs_srvc_prv = ma.Nested(
        "model.model_3012_operation.logs_srvc_prv_model.LogsSrvcPrvSchema",
        metadata={"description": ""},
    )

    road_carr = ma.Nested(
        "model.model_3012_operation.road_carr_model.RoadCarrSchema",
        metadata={"description": ""},
    )

    fret_clim_to_prty = ma.Nested(
        "model.model_3012_operation.fret_clim_to_prty_model.FretClimToPrtySchema",
        metadata={"description": ""},
    )

    ship_from_prty = ma.Nested(
        "model.model_3012_operation.ship_from_prty_model.ShipFromPrtySchema",
        metadata={"description": ""},
    )

    ship_to_prty = ma.Nested(
        "model.model_3012_operation.ship_to_prty_model.ShipToPrtySchema",
        metadata={"description": ""},
    )

    trsp_plan_line_item_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.trsp_plan_line_item_id.doc
        }
    )

    trsp_isr_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.trsp_isr_id.doc,
            "max_length": 5,
        },
    )

    trsp_srvc_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.trsp_srvc_id.doc,
            "max_length": 5,
        },
    )

    trsp_vehicle_trms_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.trsp_vehicle_trms_id.doc,
            "max_length": 5,
        },
    )

    del_info_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.del_info_id.doc,
            "max_length": 5,
        },
    )

    cns_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.cns_id.doc,
            "max_length": 5,
        },
    )

    cns_line_item_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.cns_line_item_id.doc,
            "max_length": 5,
        },
    )

    cnsg_prty_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.cnsg_prty_id.doc,
            "max_length": 5,
        },
    )

    trsp_rqr_prty_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.trsp_rqr_prty_id.doc,
            "max_length": 5,
        },
    )

    cnee_prty_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.cnee_prty_id.doc,
            "max_length": 5,
        },
    )

    logs_srvc_prv_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.logs_srvc_prv_id.doc,
            "max_length": 5,
        },
    )

    road_carr_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.road_carr_id.doc,
            "max_length": 5,
        },
    )

    fret_clim_to_prty_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.fret_clim_to_prty_id.doc,
            "max_length": 5,
        },
    )

    ship_from_prty_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.ship_from_prty_id.doc,
            "max_length": 5,
        },
    )

    ship_to_prty_id = ma.auto_field(
        metadata={
            "description": TrspPlanLineItem.__table__.c.ship_to_prty_id.doc,
            "max_length": 5,
        },
    )
