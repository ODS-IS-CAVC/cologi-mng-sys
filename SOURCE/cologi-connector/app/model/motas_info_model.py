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

class motas_info(db.Model):
    __tablename__= "motas_info"
    motas_info_id = db.Column(db.Integer, primary_key=True, doc="The motas_info id")
    max_payload_1=db.Column(db.Numeric(6), nullable=False, doc="自動車登録番号")
    max_payload_2=db.Column(db.Numeric(5), nullable=False, doc="自動車登録番号の例①の場合　品川")
    vehicle_weight=db.Column(db.Numeric(5), nullable=False, doc="自動車登録番号の例①の場合　５００")
    vehicle_length=db.Column(db.Numeric(4), nullable=False, doc="自動車登録番号の例①の場合　あ")
    vehicle_width=db.Column(db.Numeric(3), nullable=False, doc="自動車登録番号の例①の場合　１２３４")
    vehicle_height=db.Column(db.Numeric(3), nullable=False, doc="")    
    hazardous_material_volume=db.Column(db.Numeric(5), nullable=True, doc="")
    hazardous_material_specific_gravity=db.Column(db.Numeric(precision=5, scale=3), nullable=True, doc="自動車登録番号の例①の場合　１２３４")
    expiry_date=db.Column(db.String(8), nullable=False, doc="")
    deregistration_status=db.Column(CHAR(1), nullable=True, doc="")

class motas_info_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = motas_info
        load_instance = True
    motas_info_id = ma.auto_field(metadata={
        'description':  motas_info.__table__.c.motas_info_id.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),])
    max_payload_1= ma.auto_field(metadata={
        'description':  motas_info.__table__.c.max_payload_1.doc,
        "max_length":6},
        validate=[validate.Range(min=1,max=999999),])
    max_payload_2= ma.auto_field(metadata={
        'description':  motas_info.__table__.c.max_payload_2.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),])
    vehicle_weight= ma.auto_field(metadata={
        'description':  motas_info.__table__.c.vehicle_weight.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),])
    vehicle_length= ma.auto_field(metadata={
        'description':  motas_info.__table__.c.vehicle_length.doc,
        "max_length":4},
        validate=[validate.Range(min=1,max=9999),])
    vehicle_width= ma.auto_field(metadata={
        'description':  motas_info.__table__.c.vehicle_width.doc,
        "max_length":3},
        validate=[validate.Range(min=1,max=999),])
    vehicle_height= ma.auto_field(metadata={
        'description':  motas_info.__table__.c.vehicle_height.doc,
        "max_length":3},
        validate=[validate.Range(min=1,max=999),])    
    hazardous_material_volume= ma.auto_field(metadata={
        'description':  motas_info.__table__.c.hazardous_material_volume.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),]) 
    hazardous_material_specific_gravity= fields.Decimal(as_string=True, metadata={
        'description':  motas_info.__table__.c.hazardous_material_specific_gravity.doc,
        'precision':5,'scale':3})
    expiry_date= ma.auto_field(metadata={
        'description':  motas_info.__table__.c.expiry_date.doc,
        "max_length":8},
        validate=[validate.Length(max=8),])
    deregistration_status= fields.String(metadata={
        'description':  motas_info.__table__.c.deregistration_status.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
