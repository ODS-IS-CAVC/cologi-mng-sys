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

class max_carrying_capacity(db.Model):
    __tablename__= "max_carrying_capacity"
    max_carrying_capacity_id = db.Column(db.Integer, primary_key=True, nullable=False)
    package_info_id = db.Column(db.Integer, db.ForeignKey('package_info_id'), nullable=False)

class max_carrying_capacity_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = max_carrying_capacity
        load_instance = True
    max_carrying_capacity_id = ma.auto_field(metadata={
        'description': max_carrying_capacity.__table__.c.max_carrying_capacity_id.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),])
    package_info_id = ma.auto_field(metadata={
        'description': max_carrying_capacity.__table__.c.package_info_id.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),])
