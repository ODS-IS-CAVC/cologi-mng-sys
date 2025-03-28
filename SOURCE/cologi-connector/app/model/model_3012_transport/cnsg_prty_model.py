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


class CnsgPrty(db.Model):
    __tablename__ = "cnsg_prty"
    cnsg_prty_id = db.Column(db.Integer, primary_key=True, doc="The unique id")
    cnsg_prty_head_off_id = db.Column(
        db.String(13), nullable=True, doc="荷送人コード（本社）"
    )
    cnsg_prty_brnc_off_id = db.Column(
        db.String(17), nullable=True, doc="荷送人コード（事業所）"
    )
    cnsg_prty_name_txt = db.Column(
        db.String(610), nullable=True, doc="荷送人名（漢字）"
    )
    cnsg_sct_sped_org_id = db.Column(
        db.String(12), nullable=True, doc="荷送人部門コード"
    )
    cnsg_sct_sped_org_name_txt = db.Column(
        db.String(200), nullable=True, doc="荷送人部門名（漢字）"
    )
    cnsg_tel_cmm_cmp_num_txt = db.Column(
        db.String(20), nullable=True, doc="荷送人電話番号"
    )
    cnsg_pstl_adrs_line_one_txt = db.Column(
        db.String(1000), nullable=True, doc="荷送人住所（漢字）"
    )
    cnsg_pstc_cd = db.Column(db.String(7), nullable=True, doc="荷送人郵便番号")


class CnsgPrtySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CnsgPrty
        load_instance = True
        exclude = ("cnsg_prty_id",)

    cnsg_prty_id = ma.auto_field(
        metadata={
            "description": CnsgPrty.__table__.c.cnsg_prty_id.doc,
            "max_length": 5,
        },
        validate=[validate.Range(min=1, max=99999)],
    )
    cnsg_prty_head_off_id = ma.auto_field(
        metadata={
            "description": CnsgPrty.__table__.c.cnsg_prty_head_off_id.doc,
            "max_length": 13,
        },
        validate=[validate.Length(max=13)],
    )
    cnsg_prty_brnc_off_id = ma.auto_field(
        metadata={
            "description": CnsgPrty.__table__.c.cnsg_prty_brnc_off_id.doc,
            "max_length": 17,
        },
        validate=[validate.Length(max=17)],
    )
    cnsg_prty_name_txt = ma.auto_field(
        metadata={
            "description": CnsgPrty.__table__.c.cnsg_prty_name_txt.doc,
            "max_length": 610,
        },
        validate=[validate.Length(max=610)],
    )
    cnsg_sct_sped_org_id = ma.auto_field(
        metadata={
            "description": CnsgPrty.__table__.c.cnsg_sct_sped_org_id.doc,
            "max_length": 12,
        },
        validate=[validate.Length(max=12)],
    )
    cnsg_sct_sped_org_name_txt = ma.auto_field(
        metadata={
            "description": CnsgPrty.__table__.c.cnsg_sct_sped_org_name_txt.doc,
            "max_length": 200,
        },
        validate=[validate.Length(max=200)],
    )
    cnsg_tel_cmm_cmp_num_txt = ma.auto_field(
        metadata={
            "description": CnsgPrty.__table__.c.cnsg_tel_cmm_cmp_num_txt.doc,
            "max_length": 20,
        },
        validate=[validate.Length(max=20)],
    )
    cnsg_pstl_adrs_line_one_txt = ma.auto_field(
        metadata={
            "description": CnsgPrty.__table__.c.cnsg_pstl_adrs_line_one_txt.doc,
            "max_length": 1000,
        },
        validate=[validate.Length(max=1000)],
    )
    cnsg_pstc_cd = ma.auto_field(
        metadata={
            "description": CnsgPrty.__table__.c.cnsg_pstc_cd.doc,
            "max_length": 7,
        },
        validate=[validate.Length(max=7)],
    )
