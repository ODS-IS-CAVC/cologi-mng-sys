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

from marshmallow import fields,validate,ValidationError
from database import db,ma
from sqlalchemy.sql.sqltypes import CHAR

class TrspVehicleTrms(db.Model):
    __tablename__="trsp_vehicle_trms"
    trsp_vehicle_trms_id=db.Column(db.Integer, primary_key=True, doc="The primary key")
    car_cls_of_size_cd= db.Column(db.CHAR(1), nullable=True, doc="小型（2t・3t）、中型（4t）、大型（10t）、特大(25t）")
    car_cls_of_shp_cd= db.Column(db.CHAR(1), nullable=True, doc="荷台の種類")
    car_cls_of_tlg_lftr_exst_cd= db.Column(db.CHAR(1), nullable=True, doc="パワーゲート有無")
    car_cls_of_wing_body_exst_cd= db.Column(db.CHAR(1), nullable=True, doc="ウィング有無")
    car_cls_of_rfg_exst_cd= db.Column(db.CHAR(1), nullable=True, doc="冷凍・冷蔵設備有無")
    trms_of_lwr_tmp_meas= db.Column(db.Numeric(precision=5, scale=2), nullable=True, doc="冷凍・冷蔵設備の指定温度範囲の下限（℃）")
    trms_of_upp_tmp_meas= db.Column(db.Numeric(precision=5, scale=2), nullable=True, doc="冷凍・冷蔵設備の指定温度範囲の上限（℃）")
    car_cls_of_crn_exst_cd= db.Column(db.CHAR(1), nullable=True, doc="クレーン付属の有無")
    car_rmk_about_eqpm_txt= db.Column(db.String(200), nullable=True, doc="車輌設備に関する補足（漢字）")

class TrspVehicleTrmsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrspVehicleTrms
        load_instance= True
    trsp_vehicle_trms_id= ma.auto_field(metadata={'description': TrspVehicleTrms.__table__.c.trsp_vehicle_trms_id.doc, 'max_length': 5}, validate=[validate.Range(min=1, max=99999),])
    car_cls_of_size_cd= ma.auto_field(metadata={'description': TrspVehicleTrms.__table__.c.car_cls_of_size_cd.doc, 'max_length': 1}, validate=[validate.Length(max=1),])
    car_cls_of_shp_cd= ma.auto_field(metadata={'description': TrspVehicleTrms.__table__.c.car_cls_of_shp_cd.doc, 'max_length': 1}, validate=[validate.Length(max=1),])
    car_cls_of_tlg_lftr_exst_cd= ma.auto_field(metadata={'description': TrspVehicleTrms.__table__.c.car_cls_of_tlg_lftr_exst_cd.doc, 'max_length': 1}, validate=[validate.Length(max=1),])
    car_cls_of_wing_body_exst_cd= ma.auto_field(metadata={'description': TrspVehicleTrms.__table__.c.car_cls_of_wing_body_exst_cd.doc, 'max_length': 1}, validate=[validate.Length(max=1),])
    car_cls_of_rfg_exst_cd= ma.auto_field(metadata={'description': TrspVehicleTrms.__table__.c.car_cls_of_rfg_exst_cd.doc, 'max_length': 1}, validate=[validate.Length(max=1),])
    trms_of_lwr_tmp_meas= fields.Decimal(as_string=True, metadata={'description': TrspVehicleTrms.__table__.c.trms_of_lwr_tmp_meas.doc, 'precision':14,'scale':3})
    trms_of_upp_tmp_meas= fields.Decimal(as_string=True, metadata={'description': TrspVehicleTrms.__table__.c.trms_of_upp_tmp_meas.doc, 'precision':14,'scale':3})
    car_cls_of_crn_exst_cd= ma.auto_field(metadata={'description': TrspVehicleTrms.__table__.c.car_cls_of_crn_exst_cd.doc, 'max_length': 1}, validate=[validate.Length(max=1),])
    car_rmk_about_eqpm_txt= ma.auto_field(metadata={'description': TrspVehicleTrms.__table__.c.car_rmk_about_eqpm_txt.doc, 'max_length': 200}, validate=[validate.Length(max=200),])
    