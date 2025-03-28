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
from model.model_5001.vehicle_avb_resource_model import VehicleAvbResource


class CarInfo(db.Model):
    __tablename__ = "car_info"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )
    service_no = db.Column(db.String(20), nullable=False, doc="便・ダイヤ番号")
    service_name = db.Column(db.String(48), nullable=False, doc="便・ダイヤ名称")
    service_strt_date = db.Column(db.String(8), nullable=False, doc="便の運行日")
    service_strt_time = db.Column(db.String(4), nullable=False, doc="便の運行時刻")
    service_end_date = db.Column(db.String(4), nullable=False, doc="便の運行終了日")
    service_end_time = db.Column(db.String(4), nullable=False, doc="便の運行終了時刻")
    freight_rate = db.Column(db.String(10), nullable=False, doc="希望運賃")
    car_ctrl_num_id = db.Column(db.String(20), nullable=True, doc="車輌番号")
    car_license_plt_num_id = db.Column(
        db.String(48), nullable=True, doc="自動車登録番号"
    )
    car_body_num_cd = db.Column(db.String(42), nullable=True, doc="車台番号")
    car_cls_of_size_cd = db.Column(
        CHAR(1), nullable=True, doc="車輌種別\n物流情報標準項目コード: "
    )
    tractor_idcr = db.Column(
        CHAR(1), nullable=True, doc="トラクタ（けん引車）\n 物流情報標準項目コード: "
    )
    trailer_license_plt_num_id = db.Column(
        db.String(48), nullable=True, doc="トレーラ（被けん引車）"
    )
    car_weig_meas = db.Column(db.Integer, nullable=True, doc="車輌重量")
    car_lngh_meas = db.Column(db.Integer, nullable=True, doc="車輌長さ")
    car_wid_meas = db.Column(db.Integer, nullable=True, doc="車輌幅")
    car_hght_meas = db.Column(db.Integer, nullable=True, doc="車輌高さ")
    car_max_load_capacity1_meas = db.Column(
        db.Integer, nullable=False, doc="最大積載量1"
    )
    car_max_load_capacity2_meas = db.Column(
        db.Integer, nullable=True, doc="最大積載量2"
    )
    car_vol_of_hzd_item_meas = db.Column(db.Integer, nullable=True, doc="危険物容積")
    car_spc_grv_of_hzd_item_meas = db.Column(
        db.Numeric(precision=5, scale=3), nullable=True, doc="危険物比重"
    )
    car_trk_bed_hght_meas = db.Column(db.Integer, nullable=True, doc="荷室高さ")
    car_trk_bed_wid_meas = db.Column(db.Integer, nullable=True, doc="荷室全幅")
    car_trk_bed_lngh_meas = db.Column(db.Integer, nullable=True, doc="荷室長さ")
    car_trk_bed_grnd_hght_meas = db.Column(db.Integer, nullable=True, doc="荷台高さ")
    car_max_load_vol_meas = db.Column(
        db.Numeric(precision=11, scale=4), nullable=True, doc="最大積載容量"
    )
    pcke_frm_cd = db.Column(
        CHAR(3), nullable=True, doc="荷姿コード\n 物流情報標準項目コード: "
    )
    pcke_frm_name_cd = db.Column(db.String(40), nullable=True, doc="荷姿名（漢字）")
    car_max_untl_cp_quan = db.Column(db.Integer, nullable=True, doc="最大積載数")
    car_cls_of_shp_cd = db.Column(
        CHAR(1), nullable=True, doc="平ボディ/バンボディ\n 物流情報標準項目コード: "
    )
    car_cls_of_tlg_lftr_exst_cd = db.Column(
        CHAR(1), nullable=True, doc="パワーゲート有無"
    )
    car_cls_of_wing_body_exst_cd = db.Column(
        CHAR(1), nullable=True, doc="ウィング有無\n 物流情報標準項目コード: "
    )
    car_cls_of_rfg_exst_cd = db.Column(
        CHAR(1), nullable=True, doc="冷凍・冷蔵設備\n 物流情報標準項目コード: "
    )
    trms_of_lwr_tmp_meas = db.Column(
        db.Numeric(precision=5, scale=2), nullable=True, doc="温度範囲（下限）"
    )
    trms_of_upp_tmp_meas = db.Column(
        db.Numeric(precision=5, scale=2), nullable=True, doc="温度範囲（上限）"
    )
    car_cls_of_crn_exst_cd = db.Column(
        CHAR(1), nullable=True, doc="クレーン付\n 物流情報標準項目コード: "
    )
    car_rmk_about_eqpm_txt = db.Column(
        db.String(200), nullable=True, doc="車輌設備補足"
    )
    car_cmpn_name_of_gtp_crtf_exst_txt = db.Column(
        db.String(200), nullable=True, doc="車輌入門証保有"
    )
    vehicle_avb_resource_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicle_avb_resource.id"),
        nullable=False,
        doc="The unique id．",
    )
    vehicle_avb_resource = db.relationship(
        VehicleAvbResource, backref="CarInfo", lazy=True
    )


class CarInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CarInfo
        load_instance = True
        exclude = ("id","vehicle_avb_resource_id")

    vehicle_avb_resource = ma.List(
        ma.Nested(
            "model.model_5001.vehicle_avb_resource_model.VehicleAvbResourceSchema",
            metadata={
                "description": "the vehicle avb resource for the car info in trsp ability line item"
            },
        )
    )
    id = ma.auto_field(
        metadata={"description": CarInfo.__table__.c.id.doc, "max_length": 5}
    )
    service_no = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.service_no.doc,
            "max_length": 20,
            "example": "12345678901234567890",
        },
        validate=[validate.Length(max=20)],
    )
    service_name = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.service_name.doc,
            "max_length": 48,
            "example": "サービス１",
        },
        validate=[validate.Length(max=48)],
    )
    service_strt_date = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.service_strt_date.doc,
            "max_length": 8,
            "example": "20220101",
        },
        validate=[validate.Length(max=8)],
    )
    service_strt_time = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.service_strt_time.doc,
            "max_length": 4,
            "example": "0000",
        },
        validate=[validate.Length(max=4)],
    )
    service_end_date = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.service_end_date.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    service_end_time = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.service_end_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    freight_rate = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.freight_rate.doc,
            "max_length": 10,
            "example": "1234567890",
        },
        validate=[validate.Length(max=10)],
    )
    car_ctrl_num_id = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_ctrl_num_id.doc,
            "max_length": 20,
            "example": "2345",
        },
        validate=[validate.Length(max=20)],
    )
    car_license_plt_num_id = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_license_plt_num_id.doc,
            "max_length": 48,
            "example": "3360",
        },
        validate=[validate.Length(max=48)],
    )
    car_body_num_cd = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_body_num_cd.doc,
            "max_length": 42,
            "example": "1000045",
        },
        validate=[validate.Length(max=42)],
    )
    car_cls_of_size_cd = fields.String(
        metadata={
            "description": CarInfo.__table__.c.car_cls_of_size_cd.doc,
            "max_length": 1,
            "example": "5",
        },
        validate=[
            validate.Length(equal=1),
        ],
    )
    tractor_idcr = fields.String(
        metadata={
            "description": CarInfo.__table__.c.tractor_idcr.doc,
            "max_length": 1,
            "example": "1",
        },
        validate=[
            validate.Length(equal=1),
        ],
    )
    trailer_license_plt_num_id = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.trailer_license_plt_num_id.doc,
            "max_length": 48,
            "example": "1",
        },
        validate=[validate.Length(max=48)],
    )
    car_weig_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_weig_meas.doc,
            "example": "1",
        }
    )
    car_lngh_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_lngh_meas.doc,
            "example": "1",
        }
    )
    car_wid_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_wid_meas.doc,
            "example": "1",
        }
    )
    car_hght_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_hght_meas.doc,
            "example": "1",
        }
    )
    car_max_load_capacity1_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_max_load_capacity1_meas.doc,
            "example": "1",
        }
    )
    car_max_load_capacity2_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_max_load_capacity2_meas.doc,
            "example": "1",
        }
    )
    car_vol_of_hzd_item_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_vol_of_hzd_item_meas.doc,
            "example": "1",
        }
    )
    car_spc_grv_of_hzd_item_meas = fields.Decimal(
        as_string=True,
        metadata={
            "description": CarInfo.__table__.c.car_spc_grv_of_hzd_item_meas.doc,
            "precision": 5,
            "scale": 3,
            "example": "1",
        },
    )
    car_trk_bed_hght_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_trk_bed_hght_meas.doc,
            "example": "1",
        }
    )
    car_trk_bed_wid_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_trk_bed_wid_meas.doc,
            "example": "1",
        }
    )
    car_trk_bed_lngh_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_trk_bed_lngh_meas.doc,
            "example": "1",
        }
    )
    car_trk_bed_grnd_hght_meas = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_trk_bed_grnd_hght_meas.doc,
            "example": "1",
        }
    )
    car_max_load_vol_meas = fields.Decimal(
        as_string=True,
        metadata={
            "description": CarInfo.__table__.c.car_max_load_vol_meas.doc,
            "precision": 11,
            "scale": 4,
            "example": "1",
        },
    )
    pcke_frm_cd = fields.String(
        metadata={
            "description": CarInfo.__table__.c.pcke_frm_cd.doc,
            "max_length": 3,
            "example": "BA ",
        },
        validate=[
            validate.Length(equal=3),
        ],
    )
    pcke_frm_name_cd = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.pcke_frm_name_cd.doc,
            "max_length": 40,
            "example": "1",
        },
        validate=[validate.Length(max=40)],
    )
    car_max_untl_cp_quan = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_max_untl_cp_quan.doc,
            "example": "1",
        }
    )
    car_cls_of_shp_cd = fields.String(
        metadata={
            "description": CarInfo.__table__.c.car_cls_of_shp_cd.doc,
            "max_length": 1,
            "example": "1",
        },
        validate=[
            validate.Length(equal=1),
        ],
    )
    car_cls_of_tlg_lftr_exst_cd = fields.String(
        metadata={
            "description": CarInfo.__table__.c.car_cls_of_tlg_lftr_exst_cd.doc,
            "max_length": 1,
            "example": "1",
        },
        validate=[
            validate.Length(equal=1),
        ],
    )
    car_cls_of_wing_body_exst_cd = fields.String(
        metadata={
            "description": CarInfo.__table__.c.car_cls_of_wing_body_exst_cd.doc,
            "max_length": 1,
            "example": "1",
        },
        validate=[
            validate.Length(equal=1),
        ],
    )
    car_cls_of_rfg_exst_cd = fields.String(
        metadata={
            "description": CarInfo.__table__.c.car_cls_of_rfg_exst_cd.doc,
            "max_length": 1,
            "example": "1",
        },
        validate=[
            validate.Length(equal=1),
        ],
    )
    trms_of_lwr_tmp_meas = fields.Decimal(
        as_string=True,
        metadata={
            "description": CarInfo.__table__.c.trms_of_lwr_tmp_meas.doc,
            "precision": 5,
            "scale": 2,
            "example": "1",
        },
    )
    trms_of_upp_tmp_meas = fields.Decimal(
        as_string=True,
        metadata={
            "description": CarInfo.__table__.c.trms_of_upp_tmp_meas.doc,
            "precision": 5,
            "scale": 2,
            "example": "1",
        },
    )
    car_cls_of_crn_exst_cd = fields.String(
        metadata={
            "description": CarInfo.__table__.c.car_cls_of_crn_exst_cd.doc,
            "max_length": 1,
            "example": "1",
        },
        validate=[
            validate.Length(equal=1),
        ],
    )
    car_rmk_about_eqpm_txt = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_rmk_about_eqpm_txt.doc,
            "max_length": 200,
            "example": "1",
        },
        validate=[validate.Length(max=200)],
    )
    car_cmpn_name_of_gtp_crtf_exst_txt = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.car_cmpn_name_of_gtp_crtf_exst_txt.doc,
            "max_length": 200,
            "example": "1",
        },
        validate=[validate.Length(max=200)],
    )
    vehicle_avb_resource_id = ma.auto_field(
        metadata={
            "description": CarInfo.__table__.c.vehicle_avb_resource_id.doc,
            "max_length": 5,
            "example": "1",
        },
    )
