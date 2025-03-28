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
from database import db, ma
from sqlalchemy.sql.sqltypes import CHAR


class TrspSrvc(db.Model):
    __tablename__ = "trsp_srvc_3012_op"
    trsp_srvc_id = db.Column(
        db.Integer, primary_key=True, nullable=False, doc="The Primary Key"
    )
    service_no = db.Column(
        db.String(20),
        nullable=False,
        doc="当該輸送を行う輸送サービスを定義する番号・記号",
    )
    service_name = db.Column(
        db.String(48), nullable=False, doc="当該輸送を行う輸送サービスを定義する名前"
    )
    service_strt_date = db.Column(db.String(8), nullable=False, doc="便の運行日")
    service_strt_time = db.Column(db.String(4), nullable=False, doc="便の運行時刻")
    service_end_date = db.Column(db.String(4), nullable=False, doc="便の運行終了日")
    service_end_time = db.Column(db.String(4), nullable=False, doc="便の運行終了時刻")
    freight_rate = db.Column(db.String(10), nullable=False, doc="希望運賃")
    trsp_means_typ_cd = db.Column(
        db.String(2),
        nullable=True,
        doc="当該運送に使用する輸送機関（ﾄﾗｯｸ、鉄道、海運、航空等）を表すコード",
    )
    trsp_srvc_typ_cd = db.Column(
        db.String(2), nullable=True, doc="当該運送における附帯サービスを表すコード"
    )
    road_carr_srvc_typ_cd = db.Column(
        db.String(9), nullable=True, doc="運送事業者が個別に定める運送サービスコード"
    )
    trsp_root_prio_cd = db.Column(
        db.String(50), nullable=True, doc="運送の経路を表すコード"
    )
    car_cls_prio_cd = db.Column(
        db.String(3), nullable=True, doc="当該運送に使用する車輌の種別を示すコード"
    )
    cls_of_carg_in_srvc_rqrm_cd = db.Column(
        db.CHAR(1), nullable=True, doc="持込みか集荷かを表すコード"
    )
    cls_of_pkg_up_srvc_rqrm_cd = db.Column(
        db.CHAR(1), nullable=True, doc="引取りか配達かを表すコード"
    )
    pyr_cls_srvc_rqrm_cd = db.Column(
        db.String(2), nullable=True, doc="運賃料金の支払方法を識別するコード"
    )
    trms_of_mix_load_cnd_cd = db.Column(
        db.CHAR(1),
        nullable=True,
        doc="複数の荷送人の貨物についての共同運送可否を示すコード",
    )
    dsed_cll_from_date = db.Column(
        db.String(8), nullable=True, doc="荷送人が集荷を希望する最も早い日付"
    )
    dsed_cll_to_date = db.Column(
        db.String(8), nullable=True, doc="荷送人が集荷を希望する最も遅い日付"
    )
    dsed_cll_from_time = db.Column(
        db.String(4), nullable=True, doc="荷送人が集荷を希望する最も早い時刻"
    )
    dsed_cll_to_time = db.Column(
        db.String(4), nullable=True, doc="荷送人が集荷を希望する最も遅い時刻"
    )
    dsed_cll_time_trms_srvc_rqrm_cd = db.Column(
        db.String(2), nullable=True, doc="荷送人が集荷を希望する時間帯（AM/PM)"
    )
    aped_arr_from_date = db.Column(
        db.String(8), nullable=True, doc="荷送人が指定する最も早い着荷日"
    )
    aped_arr_to_date = db.Column(
        db.String(8), nullable=True, doc="荷送人が指定する最も遅い着荷日"
    )
    aped_arr_from_time_prfm_dttm = db.Column(
        db.String(4), nullable=True, doc="荷送人が指定する最も早い着荷時刻"
    )
    aped_arr_to_time_prfm_dttm = db.Column(
        db.String(4), nullable=True, doc="荷送人が指定する最も遅い着荷時刻"
    )
    aped_arr_time_trms_srvc_rqrm_cd = db.Column(
        db.String(2), nullable=True, doc="荷送人が指定する着荷時間帯（AM/PM)"
    )
    trms_of_mix_load_txt = db.Column(
        db.String(200),
        nullable=True,
        doc="危険物、匂いの有無、匂い物との共存可否、混載する場合の要件等",
    )
    trsp_srvc_note_one_txt = db.Column(
        db.String(1000),
        nullable=True,
        doc="運送サービスに関する備考1（例：附帯作業、代引、特殊輸送など）",
    )
    trsp_srvc_note_two_txt = db.Column(
        db.String(1000),
        nullable=True,
        doc="運送サービスに関する備考2（例：附帯作業、代引、特殊輸送など）",
    )


class TrspSrvcSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrspSrvc
        load_instance = True
        exclude = ("trsp_srvc_id",)

    trsp_srvc_id = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.trsp_srvc_id.doc,
            "max_length": 5,
        },
        validate=[
            validate.Range(min=1, max=99999),
        ],
    )
    service_no = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.service_no.doc,
            "max_length": 20,
            "example": "12345678901234567890",
        },
        validate=[
            validate.Length(max=20),
        ],
    )
    service_name = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.service_name.doc,
            "max_length": 48,
            "example": "123456789012345678901234",
        },
        validate=[
            validate.Length(max=48),
        ],
    )
    service_strt_date = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.service_strt_date.doc,
            "max_length": 8,
            "example": "20220101",
        },
        validate=[validate.Length(max=8)],
    )
    service_strt_time = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.service_strt_time.doc,
            "max_length": 4,
            "example": "0000",
        },
        validate=[validate.Length(max=4)],
    )
    service_end_date = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.service_end_date.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    service_end_time = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.service_end_time.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    freight_rate = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.freight_rate.doc,
            "max_length": 10,
            "example": "1234567890",
        },
        validate=[validate.Length(max=10)],
    )
    trsp_means_typ_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.trsp_means_typ_cd.doc,
            "max_length": 2,
        },
        validate=[
            validate.Length(max=2),
        ],
    )
    trsp_srvc_typ_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.trsp_srvc_typ_cd.doc,
            "max_length": 2,
        },
        validate=[
            validate.Length(max=2),
        ],
    )
    road_carr_srvc_typ_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.road_carr_srvc_typ_cd.doc,
            "max_length": 9,
        },
        validate=[
            validate.Length(max=9),
        ],
    )
    trsp_root_prio_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.trsp_root_prio_cd.doc,
            "max_length": 50,
        },
        validate=[
            validate.Length(max=50),
        ],
    )
    car_cls_prio_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.car_cls_prio_cd.doc,
            "max_length": 3,
        },
        validate=[
            validate.Length(max=3),
        ],
    )
    cls_of_carg_in_srvc_rqrm_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.cls_of_carg_in_srvc_rqrm_cd.doc,
            "max_length": 1,
        },
        validate=[
            validate.Length(max=1),
        ],
    )
    cls_of_pkg_up_srvc_rqrm_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.cls_of_pkg_up_srvc_rqrm_cd.doc,
            "max_length": 1,
        },
        validate=[
            validate.Length(max=1),
        ],
    )
    pyr_cls_srvc_rqrm_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.pyr_cls_srvc_rqrm_cd.doc,
            "max_length": 2,
        },
        validate=[
            validate.Length(max=2),
        ],
    )
    trms_of_mix_load_cnd_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.trms_of_mix_load_cnd_cd.doc,
            "max_length": 1,
        },
        validate=[
            validate.Length(max=1),
        ],
    )
    dsed_cll_from_date = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.dsed_cll_from_date.doc,
            "max_length": 8,
        },
        validate=[
            validate.Length(max=8),
        ],
    )
    dsed_cll_to_date = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.dsed_cll_to_date.doc,
            "max_length": 8,
        },
        validate=[
            validate.Length(max=8),
        ],
    )
    dsed_cll_from_time = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.dsed_cll_from_time.doc,
            "max_length": 4,
        },
        validate=[
            validate.Length(max=4),
        ],
    )
    dsed_cll_to_time = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.dsed_cll_to_time.doc,
            "max_length": 4,
        },
        validate=[
            validate.Length(max=4),
        ],
    )
    dsed_cll_time_trms_srvc_rqrm_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.dsed_cll_time_trms_srvc_rqrm_cd.doc,
            "max_length": 2,
        },
        validate=[
            validate.Length(max=2),
        ],
    )
    aped_arr_from_date = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.aped_arr_from_date.doc,
            "max_length": 8,
        },
        validate=[
            validate.Length(max=8),
        ],
    )
    aped_arr_to_date = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.aped_arr_to_date.doc,
            "max_length": 8,
        },
        validate=[
            validate.Length(max=8),
        ],
    )
    aped_arr_from_time_prfm_dttm = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.aped_arr_from_time_prfm_dttm.doc,
            "max_length": 4,
        },
        validate=[
            validate.Length(max=4),
        ],
    )
    aped_arr_time_trms_srvc_rqrm_cd = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.aped_arr_time_trms_srvc_rqrm_cd.doc,
            "max_length": 4,
        },
        validate=[
            validate.Length(max=4),
        ],
    )
    aped_arr_to_time_prfm_dttm = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.aped_arr_to_time_prfm_dttm.doc,
            "max_length": 4,
        },
        validate=[
            validate.Length(max=4),
        ],
    )
    trms_of_mix_load_txt = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.trms_of_mix_load_txt.doc,
            "max_length": 200,
        },
        validate=[
            validate.Length(max=200),
        ],
    )
    trsp_srvc_note_one_txt = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.trsp_srvc_note_one_txt.doc,
            "max_length": 1000,
        },
        validate=[
            validate.Length(max=1000),
        ],
    )
    trsp_srvc_note_two_txt = ma.auto_field(
        metadata={
            "description": TrspSrvc.__table__.c.trsp_srvc_note_two_txt.doc,
            "max_length": 1000,
        },
        validate=[
            validate.Length(max=1000),
        ],
    )
