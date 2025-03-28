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
from model.model_3012_transport.ship_from_prty_rqrm_model import ShipFromPrtyRqrm


class ShipFromPrty(db.Model):
    __tablename__ = "ship_from_prty"
    ship_from_prty_id = db.Column(db.Integer, primary_key=True, doc="The unique id")
    ship_from_prty_head_off_id = db.Column(
        db.String(13), nullable=True, doc="出荷場所コード（本社）"
    )
    ship_from_prty_brnc_off_id = db.Column(
        db.String(17), nullable=True, doc="出荷場所コード（事業所）"
    )
    ship_from_prty_name_txt = db.Column(
        db.String(640), nullable=True, doc="出荷場所名（漢字）"
    )
    ship_from_sct_id = db.Column(db.String(12), nullable=True, doc="出荷場所部門コード")
    ship_from_sct_name_txt = db.Column(
        db.String(200), nullable=True, doc="出荷場所部門名（漢字）"
    )
    ship_from_tel_cmm_cmp_num_txt = db.Column(
        db.String(20), nullable=True, doc="出荷場所電話番号"
    )
    ship_from_pstl_adrs_cty_id = db.Column(
        db.String(5), nullable=True, doc="出荷場所市区町村コード"
    )
    ship_from_pstl_adrs_id = db.Column(
        db.String(20), nullable=True, doc="出荷場所住所コード"
    )
    ship_from_pstl_adrs_line_one_txt = db.Column(
        db.String(1000), nullable=True, doc="出荷場所住所（漢字）"
    )
    ship_from_pstc_cd = db.Column(db.String(7), nullable=True, doc="出荷場所郵便番号")
    plc_cd_prty_id = db.Column(db.String(4), nullable=True, doc="場所コード")
    gln_prty_id = db.Column(db.String(13), nullable=True, doc="GLNコード")
    jpn_uplc_cd = db.Column(db.String(16), nullable=True, doc="位置情報コード")
    jpn_van_srvc_cd = db.Column(db.String(2), nullable=True, doc="サービス識別コード")
    jpn_van_vans_cd = db.Column(db.String(12), nullable=True, doc="個別管理コード")
    ship_from_prty_rqrm_id = db.Column(
        db.Integer,
        db.ForeignKey("ship_from_prty_rqrm.id"),
        nullable=False,
        doc="The unique id．",
    )
    ship_from_prty_rqrm = db.relationship(
        ShipFromPrtyRqrm, backref="ShipFromPrty", lazy=True
    )


class ShipFromPrtySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShipFromPrty
        load_instance = True
        exclude = ("ship_from_prty_id",)

    ship_from_prty_rqrm = ma.List(
        ma.Nested(
            "model.model_3012_transport.ship_from_prty_rqrm_model.ShipFromPrtyRqrmSchema",
            metadata={"description": ""},
        )
    )

    ship_from_prty_id = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_prty_id.doc,
            "max_length": 5,
        },
        validate=[validate.Range(min=1, max=99999)],
    )
    ship_from_prty_head_off_id = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_prty_head_off_id.doc,
            "max_length": 13,
        },
        validate=[validate.Length(max=13)],
    )
    ship_from_prty_brnc_off_id = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_prty_brnc_off_id.doc,
            "max_length": 17,
        },
        validate=[validate.Length(max=17)],
    )
    ship_from_prty_name_txt = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_prty_name_txt.doc,
            "max_length": 640,
        },
        validate=[validate.Length(max=640)],
    )
    ship_from_sct_id = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_sct_id.doc,
            "max_length": 12,
        },
        validate=[validate.Length(max=12)],
    )
    ship_from_sct_name_txt = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_sct_name_txt.doc,
            "max_length": 200,
        },
        validate=[validate.Length(max=200)],
    )
    ship_from_tel_cmm_cmp_num_txt = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_tel_cmm_cmp_num_txt.doc,
            "max_length": 20,
        },
        validate=[validate.Length(max=20)],
    )
    ship_from_pstl_adrs_cty_id = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_pstl_adrs_cty_id.doc,
            "max_length": 5,
        },
        validate=[validate.Length(max=5)],
    )
    ship_from_pstl_adrs_id = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_pstl_adrs_id.doc,
            "max_length": 20,
        },
        validate=[validate.Length(max=20)],
    )
    ship_from_pstl_adrs_line_one_txt = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_pstl_adrs_line_one_txt.doc,
            "max_length": 1000,
        },
        validate=[validate.Length(max=1000)],
    )
    ship_from_pstc_cd = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.ship_from_pstc_cd.doc,
            "max_length": 7,
        },
        validate=[validate.Length(max=7)],
    )
    plc_cd_prty_id = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.plc_cd_prty_id.doc,
            "max_length": 4,
        },
        validate=[validate.Length(max=4)],
    )
    gln_prty_id = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.gln_prty_id.doc,
            "max_length": 13,
        },
        validate=[validate.Length(max=13)],
    )
    jpn_uplc_cd = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.jpn_uplc_cd.doc,
            "max_length": 16,
        },
        validate=[validate.Length(max=16)],
    )
    jpn_van_srvc_cd = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.jpn_van_srvc_cd.doc,
            "max_length": 2,
        },
        validate=[validate.Length(max=2)],
    )
    jpn_van_vans_cd = ma.auto_field(
        metadata={
            "description": ShipFromPrty.__table__.c.jpn_van_vans_cd.doc,
            "max_length": 12,
        },
        validate=[validate.Length(max=12)],
    )
