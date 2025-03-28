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


class RoadCarr(db.Model):
    __tablename__ = "road_carr"
    road_carr_id = db.Column(db.Integer, primary_key=True, doc="The unique id")
    trsp_cli_prty_head_off_id = db.Column(db.String(13), nullable=True, doc="運送事業者コード（本社）")
    trsp_cli_prty_brnc_off_id = db.Column(db.String(17), nullable=True, doc="運送事業者コード（事業所）")
    trsp_cli_prty_name_txt = db.Column(db.String(640), nullable=True, doc="運送事業者名（漢字）")
    road_carr_depa_sped_org_id = db.Column(db.String(12), nullable=True, doc="運送事業者発店コード")
    road_carr_depa_sped_org_name_txt = db.Column(db.String(640), nullable=True, doc="運送事業者発店名（漢字）")
    trsp_cli_tel_cmm_cmp_num_txt = db.Column(db.String(20), nullable=True, doc="運送事業者電話番号")
    road_carr_arr_sped_org_id = db.Column(db.String(12), nullable=True, doc="運送事業者着店コード")
    road_carr_arr_sped_org_name_txt = db.Column(db.String(640), nullable=True, doc="運送事業者着店名（漢字）")




class RoadCarrSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoadCarr
        load_instance = True

    road_carr_id=ma.auto_field(metadata={'description': RoadCarr.__table__.c.road_carr_id.doc, 'max_length':5}, validate=[validate.Range(min=1, max=99999)])
    trsp_cli_prty_head_off_id = ma.auto_field(metadata={"description": RoadCarr.__table__.c.trsp_cli_prty_head_off_id.doc, 'max_length':13}, validate=[validate.Length(max=13)])
    trsp_cli_prty_brnc_off_id = ma.auto_field(metadata={"description": RoadCarr.__table__.c.trsp_cli_prty_brnc_off_id.doc, 'max_length':17}, validate=[validate.Length(max=17)])
    trsp_cli_prty_name_txt = ma.auto_field(metadata={"description": RoadCarr.__table__.c.trsp_cli_prty_name_txt.doc, 'max_length':640}, validate=[validate.Length(max=640)])
    road_carr_depa_sped_org_id = ma.auto_field(metadata={"description": RoadCarr.__table__.c.road_carr_depa_sped_org_id.doc, 'max_length':12}, validate=[validate.Length(max=12)])
    road_carr_depa_sped_org_name_txt = ma.auto_field(metadata={"description": RoadCarr.__table__.c.road_carr_depa_sped_org_name_txt.doc, 'max_length':640}, validate=[validate.Length(max=640)])
    trsp_cli_tel_cmm_cmp_num_txt = ma.auto_field(metadata={"description": RoadCarr.__table__.c.trsp_cli_tel_cmm_cmp_num_txt.doc, 'max_length':20}, validate=[validate.Length(max=20)])
    road_carr_arr_sped_org_id = ma.auto_field(metadata={"description": RoadCarr.__table__.c.road_carr_arr_sped_org_id.doc, 'max_length':12}, validate=[validate.Length(max=12)])
    road_carr_arr_sped_org_name_txt = ma.auto_field(metadata={"description": RoadCarr.__table__.c.road_carr_arr_sped_org_name_txt.doc, 'max_length':640}, validate=[validate.Length(max=640)])
