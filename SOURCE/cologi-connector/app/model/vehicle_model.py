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

class vehicle_info(db.Model):
    __tablename__= "vehicle_info"
    vehicle_info_id = db.Column(db.Integer, primary_key=True, doc="The vehicle_info id")
    registration_number=db.Column(db.String(48), nullable=False, doc="自動車登録番号")
    registration_transport_office_name=db.Column(db.String(16), nullable=False, doc="自動車登録番号の例①の場合　品川")
    registration_vehicle_type=db.Column(db.String(12), nullable=False, doc="自動車登録番号の例①の場合　５００")
    registration_vehicle_use=db.Column(db.String(4), nullable=False, doc="自動車登録番号の例①の場合　あ")
    registration_vehicle_id=db.Column(db.String(16), nullable=False, doc="自動車登録番号の例①の場合　１２３４")
    chassis_number=db.Column(db.String(42), nullable=True, doc="")
    vehicle_id=db.Column(db.String(20), nullable=True, doc="")
    operator_corporate_number=db.Column(db.String(13), nullable=False, doc="")
    operator_business_code=db.Column(db.String(17), nullable=True, doc="事業所コード分類＋事業所コード")
    owner_corporate_number=db.Column(db.String(13), nullable=True, doc="所有者と使用者が異なる場合に入力")
    owner_business_code=db.Column(db.String(17), nullable=True, doc="車庫などの車輌の保有地（SIPが各事業所に付与する事業所を示すコード）")
    vehicle_type=db.Column(CHAR(1), nullable=False, doc="1：小型（2t・3t）、2：中型（4t）、3：大型（10t）、4：特大（25t）、5：軽貨物、9：その他")
    hazardous_material_vehicle_type=db.Column(CHAR(1), nullable=True, doc="0：危険物積載車輌以外、1：危険物積載車輌")
    tractor=db.Column(CHAR(1), nullable=True, doc="0：トラクタ（けん引車）以外、1：トラクタ（けん引車）")
    trailer=db.Column(db.String(48), nullable=True, doc="トラクタ（けん引車）に特定のトレーラが常時牽引される場合")

class vehicle_info_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = vehicle_info
        load_instance = True
    vehicle_info_id = ma.auto_field(metadata={
        'description':  vehicle_info.__table__.c.vehicle_info_id.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),])
    registration_number=ma.auto_field(metadata={
        'description':  vehicle_info.__table__.c.registration_number.doc,
        "max_length":48},
        validate=[validate.Length(max=48),])
    registration_transport_office_name=ma.auto_field(metadata={
        'description':  vehicle_info.__table__.c.registration_transport_office_name.doc,
        "max_length":16},
        validate=[validate.Length(max=16),])
    registration_vehicle_type=ma.auto_field(metadata={
        'description':  vehicle_info.__table__.c.registration_vehicle_type.doc,
        "max_length":12},
        validate=[validate.Length(max=12),])
    registration_vehicle_use=ma.auto_field(metadata={
        'description':  vehicle_info.__table__.c.registration_vehicle_use.doc,
        "max_length":4},
        validate=[validate.Length(max=4),])
    registration_vehicle_id=ma.auto_field(metadata={
        'description':  vehicle_info.__table__.c.registration_vehicle_id.doc,
        "max_length":16},
        validate=[validate.Length(max=16),])
    chassis_number=ma.auto_field(metadata={
        'description':  vehicle_info.__table__.c.chassis_number.doc,
        "max_length":42},
        validate=[validate.Length(max=42),])
    vehicle_id=ma.auto_field(metadata={'description':  vehicle_info.__table__.c.vehicle_id.doc,
        "max_length":20},
        validate=[validate.Length(max=20),])
    operator_corporate_number=ma.auto_field(metadata={
        'description':  vehicle_info.__table__.c.operator_corporate_number.doc,
        "max_length":13},
        validate=[validate.Length(max=13),])
    operator_business_code=ma.auto_field(metadata={'description':  vehicle_info.__table__.c.operator_business_code.doc,
        "max_length":17},
        validate=[validate.Length(max=17),])
    owner_corporate_number=ma.auto_field(metadata={
        'description':  vehicle_info.__table__.c.owner_corporate_number.doc,
        "max_length":13},
        validate=[validate.Length(max=13),])
    owner_business_code=ma.auto_field(metadata={'description':  vehicle_info.__table__.c.owner_business_code.doc,
        "max_length":17},
        validate=[validate.Length(max=17),])
    vehicle_type=fields.String(metadata={'description':  vehicle_info.__table__.c.vehicle_type.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
    hazardous_material_vehicle_type=ma.auto_field(metadata={'description':  vehicle_info.__table__.c.hazardous_material_vehicle_type.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
    tractor=ma.auto_field(metadata={'description':  vehicle_info.__table__.c.tractor.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
    trailer=ma.auto_field(metadata={'description':  vehicle_info.__table__.c.trailer.doc,
        "max_length":48},
        validate=[validate.Length(max=48),])

# class hazardous_material_info(db.Model):
#     __tablename__= "hazardous_material_info"
#     hazardous_material_info_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     vehicle_info_id = db.Column(db.Integer, db.ForeignKey('vehicle_info_id'), nullable=False)
#     hazardous_material_item_code_info_id = db.Column(db.Integer, db.ForeignKey('hazardous_material_item_code_info_id'), nullable=False)

# class hazardous_material_info_schema(ma.SQLAlchemyAutoSchema):
    # class Meta:
    #     model = hazardous_material_info
    #     load_instance = True
    # hazardous_material_info_id = ma.auto_field(metadata={'description': hazardous_material_info.__table__.c.hazardous_material_info_id.doc})
    # vehicle_info_id = ma.auto_field(metadata={'description': hazardous_material_info.__table__.c.vehicle_info_id.doc})
    # hazardous_material_item_code_info_id = ma.auto_field(metadata={'description': hazardous_material_info.__table__.c.hazardous_material_item_code_info_id.doc})