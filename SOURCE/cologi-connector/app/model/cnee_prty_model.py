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

from marshmallow import fields,validate
from database import db,ma


class CneePrty(db.Model):
    __tablename__ = "cnee_prty"
    cnee_prty_id = db.Column(db.Integer, primary_key=True, doc="The unique id")
    cnee_prty_head_off_id = db.Column(db.String(13), nullable=True, doc="荷受人コード（本社）")
    cnee_prty_brnc_off_id = db.Column(db.String(17), nullable=True, doc="荷受人コード（事業所）")
    cnee_prty_name_txt = db.Column(db.String(640), nullable=True, doc="荷受人名（漢字）")
    cnee_sct_id = db.Column(db.String(12), nullable=True, doc="荷受人部門コード")
    cnee_sct_name_txt = db.Column(db.String(200), nullable=True, doc="荷受人部門名（漢字）")
    cnee_prim_cnt_pers_name_txt = db.Column(db.String(20), nullable=True, doc="荷受人担当者名（漢字）")
    cnee_tel_cmm_cmp_num_txt = db.Column(db.String(20), nullable=True, doc="荷受人電話番号")
    cnee_pstl_adrs_line_one_txt = db.Column(db.String(1000), nullable=True, doc="荷受人住所（漢字）")
    cnee_pstc_cd = db.Column(db.String(7), nullable=True, doc="荷受人郵便番号")        




class CneePrtySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CneePrty
        load_instance = True

    cnee_prty_id = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_prty_id.doc, 'max_length':5}, validate=[validate.Range(min=1,max=99999),])
    cnee_prty_head_off_id = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_prty_head_off_id.doc, 'max_length':13}, validate=[validate.Length(max=13)])
    cnee_prty_brnc_off_id = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_prty_brnc_off_id.doc, 'max_length':17}, validate=[validate.Length(max=17)])
    cnee_prty_name_txt = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_prty_name_txt.doc, 'max_length':640}, validate=[validate.Length(max=640)])
    cnee_sct_id = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_sct_id.doc, 'max_length':12}, validate=[validate.Length(max=12)])
    cnee_sct_name_txt = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_sct_name_txt.doc, 'max_length':200}, validate=[validate.Length(max=200)])
    cnee_prim_cnt_pers_name_txt = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_prim_cnt_pers_name_txt.doc, 'max_length':20}, validate=[validate.Length(max=20)])
    cnee_tel_cmm_cmp_num_txt = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_tel_cmm_cmp_num_txt.doc, 'max_length':20}, validate=[validate.Length(max=20)])
    cnee_pstl_adrs_line_one_txt = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_pstl_adrs_line_one_txt.doc, 'max_length':1000}, validate=[validate.Length(max=1000)])
    cnee_pstc_cd = ma.auto_field(metadata={"description": CneePrty.__table__.c.cnee_pstc_cd.doc, 'max_length':7}, validate=[validate.Length(max=7)])
