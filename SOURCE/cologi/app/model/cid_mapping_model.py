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
from marshmallow import fields, validate, ValidationError
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import db, ma
from model.model_5001.trsp_ability_line_item_model import TrspAbilityLineItem


class CidMapping(db.Model):
    __tablename__ = "reserve"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )  # created to have a primary key
    cid = db.Column(
        db.String(256),
        doc="事業者ID",
    )
    endpoint=db.Column(
        db.String(256),
        doc="エンドポイント",
    )

class CidMappingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        model = CidMapping
        load_instance = True
        exclude = ("id")
    id = ma.auto_field(
        metadata={"description": CidMapping.__table__.c.id.doc, "max_length": 5}
    )
    cid = ma.auto_field(
        metadata={
            "description": CidMapping.__table__.c.cid.doc,
            "max_length": 256,
            "example":"490000001",
        },
    )
    endpoint = ma.auto_field(
        metadata={
            "description": CidMapping.__table__.c.endpoint.doc,
            "max_length": 256,
            "example":"https://localhost:8020",
        },
    )

