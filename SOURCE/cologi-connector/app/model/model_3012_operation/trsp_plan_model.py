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

from marshmallow import fields, validate
from database import db, ma


class TrspPlan(db.Model):
    __tablename__ = "trsp_plan"
    trsp_plan_id = db.Column(db.Integer, primary_key=True, doc="The primary key")
    trsp_plan_stas_cd = db.Column(
        db.String(2),
        nullable=True,
        doc="Code indicating the type of transportation plan (next month plan, weekly plan, etc.)",
    )


class TrspPlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrspPlan
        load_instance = True
        exclude = ("trsp_plan_id",)
        trsp_plan_id = ma.auto_field(
            metadata={
                "description": TrspPlan.__table__.c.trsp_plan_id.doc,
                "max_length": 5,
            },
            validate=[
                validate.Range(min=1, max=99999),
            ],
        )
        trsp_plan_stas_cd = ma.auto_field(
            metadata={
                "description": TrspPlan.__table__.c.trsp_plan_stas_cd.doc,
                "max_length": 2,
            },
            validate=[
                validate.Length(max=2),
            ],
        )
