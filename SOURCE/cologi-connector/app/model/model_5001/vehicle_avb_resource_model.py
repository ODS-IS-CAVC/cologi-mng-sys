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
from model.model_5001.cut_off_info_model import CutOffInfo
from model.model_5001.free_time_info_model import FreeTimeInfo


class VehicleAvbResource(db.Model):
    __tablename__ = "vehicle_avb_resource"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )
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
    clb_area_txt = db.Column(db.String(40), nullable=True, doc="集荷地域")
    trms_of_clb_area_cd = db.Column(db.String(5), nullable=True, doc="集荷地域コード")
    avb_date_cll_date = db.Column(db.String(8), nullable=True, doc="集荷予定日")
    avb_from_time_of_cll_time = db.Column(
        db.String(4), nullable=True, doc="集荷開始時間"
    )
    avb_to_time_of_cll_time = db.Column(db.String(4), nullable=True, doc="集荷終了時間")
    delb_area_txt = db.Column(db.String(40), nullable=True, doc="配達地域")
    trms_of_delb_area_cd = db.Column(db.String(5), nullable=True, doc="配達地域コード")
    esti_del_date_prfm_dttm = db.Column(db.String(8), nullable=True, doc="配達予定日")
    avb_from_time_of_del_time = db.Column(
        db.String(4), nullable=True, doc="配達開始時間"
    )
    avb_to_time_of_del_time = db.Column(db.String(4), nullable=True, doc="配達終了時間")
    avb_load_cp_of_car_meas = db.Column(
        db.Numeric(precision=14, scale=3), nullable=True, doc="積載可能重量(kg)"
    )
    avb_load_vol_of_car_meas = db.Column(
        db.Numeric(precision=11, scale=4), nullable=True, doc="積載可能容積"
    )
    pcke_frm_cd = db.Column(
        CHAR(3), nullable=True, doc="荷姿コード\n 物流情報標準項目コード: "
    )
    avb_num_of_retb_cntn_of_car_quan = db.Column(
        db.Integer, nullable=True, doc="積載可能輸送容器数"
    )
    trk_bed_stas_txt = db.Column(db.String(200), nullable=True, doc="荷室状況")
    cut_off_Info_id = db.Column(
        db.Integer,
        db.ForeignKey("cut_off_Info.id"),
        nullable=False,
        doc="The unique id．",
    )
    cut_off_Info = db.relationship(CutOffInfo, backref="VehicleAvbResource", lazy=True)
    free_time_Info_id = db.Column(
        db.Integer,
        db.ForeignKey("free_time_Info.id"),
        nullable=False,
        doc="The unique id．",
    )
    free_time_Info = db.relationship(
        FreeTimeInfo, backref="VehicleAvbResource", lazy=True
    )


class VehicleAvbResourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VehicleAvbResource
        load_instance = True
        exclude = ("id",)

    cut_off_Info = ma.List(
        ma.Nested(
            "model.model_5001.cut_off_info_model.CutOffInfoSchema",
            metadata={"description": ""},
        )
    )

    free_time_Info = ma.List(
        ma.Nested(
            "model.model_5001.free_time_info_model.FreeTimeInfoSchema",
            metadata={"description": ""},
        )
    )

    id = ma.auto_field(
        metadata={"description": VehicleAvbResource.__table__.c.id.doc, "max_length": 5}
    )
    trsp_op_strt_area_line_one_txt = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trsp_op_strt_area_line_one_txt.doc,
            "max_length": 20,
            "example": "12345678901234567890",
        },
        validate=[validate.Length(max=20)],
    )
    trsp_op_strt_area_cty_jis_cd = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trsp_op_strt_area_cty_jis_cd.doc,
            "max_length": 5,
        },
        validate=[validate.Length(max=5)],
    )
    trsp_op_date_trm_strt_date = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trsp_op_date_trm_strt_date.doc,
            "max_length": 8,
            "example": "20241024",
        },
        validate=[validate.Length(max=8)],
    )
    trsp_op_plan_date_trm_strt_time = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trsp_op_plan_date_trm_strt_time.doc,
            "max_length": 4,
            "example": "1416",
        },
        validate=[validate.Length(max=4)],
    )
    trsp_op_end_area_line_one_txt = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trsp_op_end_area_line_one_txt.doc,
            "max_length": 40,
            "example": "12345678901234567890",
        },
        validate=[validate.Length(max=40)],
    )
    trsp_op_end_area_cty_jis_cd = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trsp_op_end_area_cty_jis_cd.doc,
            "max_length": 5,
        },
        validate=[validate.Length(max=5)],
    )
    trsp_op_date_trm_end_date = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trsp_op_date_trm_end_date.doc,
            "max_length": 8,
            "example": "20241025",
        },
        validate=[validate.Length(max=8)],
    )
    trsp_op_plan_date_trm_end_time = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trsp_op_plan_date_trm_end_time.doc,
            "max_length": 4,
            "example": "1416",
        },
        validate=[validate.Length(max=4)],
    )
    clb_area_txt = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.clb_area_txt.doc,
            "max_length": 40,
        },
        validate=[validate.Length(max=40)],
    )
    trms_of_clb_area_cd = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trms_of_clb_area_cd.doc,
            "max_length": 5,
        },
        validate=[validate.Length(max=5)],
    )
    avb_date_cll_date = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.avb_date_cll_date.doc,
            "max_length": 8,
        },
        validate=[validate.Length(max=8)],
    )
    avb_from_time_of_cll_time = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.avb_from_time_of_cll_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    avb_to_time_of_cll_time = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.avb_to_time_of_cll_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    delb_area_txt = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.delb_area_txt.doc,
            "max_length": 40,
        },
        validate=[validate.Length(max=40)],
    )
    trms_of_delb_area_cd = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trms_of_delb_area_cd.doc,
            "max_length": 5,
        },
        validate=[validate.Length(max=5)],
    )
    esti_del_date_prfm_dttm = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.esti_del_date_prfm_dttm.doc,
            "max_length": 8,
        },
        validate=[validate.Length(max=8)],
    )
    avb_from_time_of_del_time = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.avb_from_time_of_del_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    avb_to_time_of_del_time = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.avb_to_time_of_del_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    avb_load_cp_of_car_meas = fields.Decimal(
        as_string=True,
        metadata={
            "description": VehicleAvbResource.__table__.c.avb_load_cp_of_car_meas.doc,
            "precision": 14,
            "scale": 3,
        },
    )
    avb_load_vol_of_car_meas = fields.Decimal(
        as_string=True,
        metadata={
            "description": VehicleAvbResource.__table__.c.avb_load_vol_of_car_meas.doc,
            "precision": 11,
            "scale": 4,
        },
    )
    pcke_frm_cd = fields.String(
        metadata={
            "description": VehicleAvbResource.__table__.c.pcke_frm_cd.doc,
            "max_length": 3,
            "example": "BA ",
        },
        validate=[
            validate.Length(equal=3),
        ],
    )
    avb_num_of_retb_cntn_of_car_quan = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.avb_num_of_retb_cntn_of_car_quan.doc
        }
    )
    trk_bed_stas_txt = ma.auto_field(
        metadata={
            "description": VehicleAvbResource.__table__.c.trk_bed_stas_txt.doc,
            "max_length": 200,
        },
        validate=[validate.Length(max=200)],
    )
