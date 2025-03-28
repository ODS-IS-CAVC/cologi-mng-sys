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
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import db, ma

# from trsp_ability_line_item_model import TrspAbilityLineItemSchema


class LogsSrvcPrv(db.Model):
    __tablename__ = "logs_srvc_prv_5001"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )  # created to have a primary key
    logs_srvc_prv_prty_head_off_id = db.Column(
        db.String(13), nullable=True, doc="物流サービス提供者コード（本社）"
    )
    logs_srvc_prv_prty_brnc_off_id = db.Column(
        db.String(17), nullable=True, doc="物流サービス提供者コード（事業所）"
    )
    logs_srvc_prv_prty_name_txt = db.Column(
        db.String(640), nullable=True, doc="物流サービス提供者名（漢字）"
    )
    logs_srvc_prv_sct_sped_org_id = db.Column(
        db.String(12), nullable=True, doc="物流サービス提供者部門コード"
    )
    logs_srvc_prv_sct_sped_org_name_txt = db.Column(
        db.String(200), nullable=True, doc="物流サービス提供者部門名（漢字）"
    )
    logs_srvc_prv_sct_prim_cnt_pers_name_txt = db.Column(
        db.String(40), nullable=True, doc="物流サービス提供者担当者名（漢字）"
    )
    logs_srvc_prv_sct_tel_cmm_cmp_num_txt = db.Column(
        db.String(20), nullable=True, doc="物流サービス提供者電話番号"
    )


class LogsSrvcPrvSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LogsSrvcPrv
        load_instance = True
        exclude = ("id",)

    id = ma.auto_field(
        metadata={"description": LogsSrvcPrv.__table__.c.id.doc, "max_length": 5}
    )
    logs_srvc_prv_prty_head_off_id = ma.auto_field(
        metadata={
            "description": LogsSrvcPrv.__table__.c.logs_srvc_prv_prty_head_off_id.doc,
            "max_length": 13,
        },
        validate=[validate.Length(max=13)],
    )
    logs_srvc_prv_prty_brnc_off_id = ma.auto_field(
        metadata={
            "description": LogsSrvcPrv.__table__.c.logs_srvc_prv_prty_brnc_off_id.doc,
            "max_length": 17,
        },
        validate=[validate.Length(max=17)],
    )
    logs_srvc_prv_prty_name_txt = ma.auto_field(
        metadata={
            "description": LogsSrvcPrv.__table__.c.logs_srvc_prv_prty_name_txt.doc,
            "max_length": 13,
        },
        validate=[validate.Length(max=640)],
    )
    logs_srvc_prv_sct_sped_org_id = ma.auto_field(
        metadata={
            "description": LogsSrvcPrv.__table__.c.logs_srvc_prv_sct_sped_org_id.doc,
            "max_length": 13,
        },
        validate=[validate.Length(max=12)],
    )
    logs_srvc_prv_sct_sped_org_name_txt = ma.auto_field(
        metadata={
            "description": LogsSrvcPrv.__table__.c.logs_srvc_prv_sct_sped_org_name_txt.doc,
            "max_length": 13,
        },
        validate=[validate.Length(max=200)],
    )
    logs_srvc_prv_sct_prim_cnt_pers_name_txt = ma.auto_field(
        metadata={
            "description": LogsSrvcPrv.__table__.c.logs_srvc_prv_sct_prim_cnt_pers_name_txt.doc,
            "max_length": 13,
        },
        validate=[validate.Length(max=40)],
    )
    logs_srvc_prv_sct_tel_cmm_cmp_num_txt = ma.auto_field(
        metadata={
            "description": LogsSrvcPrv.__table__.c.logs_srvc_prv_sct_tel_cmm_cmp_num_txt.doc,
            "max_length": 13,
        },
        validate=[validate.Length(max=20)],
    )
