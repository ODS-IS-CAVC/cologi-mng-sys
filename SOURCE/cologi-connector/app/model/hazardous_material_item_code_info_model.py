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
from sqlalchemy.sql.sqltypes import CHAR

class hazardous_material_item_code_info(db.Model):
    __tablename__= "hazardous_material_item_code_info"
    hazardous_material_item_code_info_id = db.Column(db.Integer, primary_key=True, nullable=False, doc="危険物積載物品名コード ID")
    hazardous_material_item_code = db.Column(CHAR(2), nullable=True, doc="危険物積載物品名コード")
    hazardous_material_text_info = db.Column(CHAR(1), nullable=True, doc="危険物文字情報")

class hazardous_material_item_code_info_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = hazardous_material_item_code_info
        load_instance = True
    hazardous_material_item_code_info_id = ma.auto_field(metadata={
        'description': hazardous_material_item_code_info.__table__.c.hazardous_material_item_code_info_id.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),])
    hazardous_material_item_code = fields.String(metadata={
        'description': hazardous_material_item_code_info.__table__.c.hazardous_material_item_code.doc,
        'max_length':2,
        'example':"01"},
        validate=[validate.Length(equal=2),])
    hazardous_material_text_info = fields.String(metadata={
        'description': hazardous_material_item_code_info.__table__.c.hazardous_material_text_info.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
