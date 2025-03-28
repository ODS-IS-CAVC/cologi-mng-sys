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

from marshmallow import fields
from database import db,ma
from .trsp_isr_model import TrspIsrSchema

class TrspPlanLineItem(db.Model):
    __tablename__="trsp_plan_line_item"
    trsp_plan_line_item_id = db.Column(db.Integer, primary_key=True, doc="The primary key")
    
class TrspPlanLineItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= TrspPlanLineItem
        load_instance = True
    trsp_plan_line_item_id= ma.auto_field(metadata={'description': TrspPlanLineItem.__table__.c.trsp_plan_line_item_id.doc})