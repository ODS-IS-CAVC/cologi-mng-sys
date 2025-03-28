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

class vehicle_details(db.Model):
    __tablename__= "vehicle_details"
    vehicle_details_id = db.Column(db.Integer, primary_key=True , doc="車両の詳細 ID")
    bed_height=db.Column(db.Numeric(15), nullable=False, doc="荷台高さ")
    cargo_height=db.Column(db.Numeric(15), nullable=False, doc="荷室高さ")
    cargo_width=db.Column(db.Numeric(15), nullable=False, doc="荷室全幅")
    cargo_length=db.Column(db.Numeric(15), nullable=False, doc="荷室長さ")
    max_cargo_capacity=db.Column(db.Numeric(precision=11, scale=4), nullable=True, doc="最大積載容量")
    body_type=db.Column(CHAR(1), nullable=True, doc="1：平ボティ、2：バンボディ、9：指定なし")
    power_gate=db.Column(CHAR(1), nullable=True, doc="1：パワーゲート有、2：パワーゲート無、9：指定なし")
    wing_doors=db.Column(CHAR(1), nullable=False, doc="1：ウィング有、2：ウィング無、9：指定なし")
    refrigeration_unit=db.Column(CHAR(1), nullable=True, doc="1：冷凍・冷蔵設備有、2：冷凍・冷蔵設備無、9：指定なし")
    temperature_range_min=db.Column(db.Numeric(precision=5, scale=2), nullable=True, doc="温度範囲（下限）")
    temperature_range_max=db.Column(db.Numeric(precision=5, scale=2), nullable=True, doc="温度範囲（上限）")
    crane_equipped=db.Column(CHAR(1), nullable=False, doc="1：クレーン有、2：クレーン無、9：指定なし")
    vehicle_equipment_notes=db.Column(db.String(200), nullable=True, doc="車輌設備補足")
    master_data_start_date=db.Column(db.String(8), nullable=True, doc="マスタ適用開始日")
    master_data_end_date=db.Column(db.String(8), nullable=True, doc="マスタ適用終了日")

class vehicle_details_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = vehicle_details
        load_instance = True
    vehicle_details_id = ma.auto_field(metadata={
        'description':  vehicle_details.__table__.c.vehicle_details_id.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),])
    bed_height = ma.auto_field(metadata={
        'description':  vehicle_details.__table__.c.bed_height.doc,
        "max_length":15},
        validate=[validate.Range(min=1,max=999999999999999),])
    cargo_height = ma.auto_field(metadata={
        'description':  vehicle_details.__table__.c.cargo_height.doc,
        "max_length":15},
        validate=[validate.Range(min=1,max=999999999999999),])
    cargo_width = ma.auto_field(metadata={'description':  vehicle_details.__table__.c.cargo_width.doc,
        "max_length":15},
        validate=[validate.Range(min=1,max=999999999999999),])
    cargo_length = ma.auto_field(metadata={'description':  vehicle_details.__table__.c.cargo_length.doc,
        "max_length":15},
        validate=[validate.Range(min=1,max=999999999999999),])
    max_cargo_capacity = fields.Decimal(as_string=True, metadata={
        'description':  vehicle_details.__table__.c.max_cargo_capacity.doc,
        'precision':11,'scale':4})
    body_type = fields.String(metadata={
        'description':  vehicle_details.__table__.c.body_type.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
    power_gate = fields.String(metadata={
        'description':  vehicle_details.__table__.c.power_gate.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
    wing_doors = fields.String(metadata={
        'description':  vehicle_details.__table__.c.wing_doors.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
    refrigeration_unit = fields.String(metadata={
        'description':  vehicle_details.__table__.c.refrigeration_unit.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
    temperature_range_min = fields.Decimal(as_string=True, metadata={
        'description':  vehicle_details.__table__.c.temperature_range_min.doc,
        'precision':5,'scale':2})
    temperature_range_max = fields.Decimal(as_string=True, metadata={
        'description':  vehicle_details.__table__.c.temperature_range_max.doc,
        'precision':5,'scale':2})
    crane_equipped = fields.String(metadata={
        'description':  vehicle_details.__table__.c.crane_equipped.doc,
        'max_length':1,
        'example':"1"},
        validate=[validate.Length(equal=1),])
    vehicle_equipment_notes = ma.auto_field(metadata={
        'description':  vehicle_details.__table__.c.vehicle_equipment_notes.doc,
        "max_length":200},
        validate=[validate.Length(max=200),])
    master_data_start_date = ma.auto_field(metadata={
        'description':  vehicle_details.__table__.c.master_data_start_date.doc,
        "max_length":8},
        validate=[validate.Length(max=8),])
    master_data_end_date = ma.auto_field(metadata={
        'description':  vehicle_details.__table__.c.master_data_end_date.doc,
        "max_length":8},
        validate=[validate.Length(max=8),])
