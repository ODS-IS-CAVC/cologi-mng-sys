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

from datetime import datetime,date,time
from marshmallow import fields
from database import db,ma

class Bp1(db.Model):
    __tablename__= "bp1"
    id=db.Column(db.Integer, primary_key=True, doc="The unique id")
    email=db.Column(db.String(50), nullable=False, doc="The email of the id")
    created_at=db.Column(db.DateTime(timezone=True), nullable=False, doc="The created date time of the id",default=datetime.now)
    schedule_date=db.Column(db.Date,   doc="The schedule date of the id",default=date.today)
    schedule_time=db.Column(db.Time,  doc="The schedule time of the id", default=lambda: datetime.now().time())
   

class Bp1Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bp1
        load_instance = True
    id=ma.auto_field(metadata={'description': Bp1.__table__.c.id.doc})
    email=ma.auto_field(metadata={'description': Bp1.__table__.c.email.doc})
    created_at=ma.auto_field(metadata={'description': Bp1.__table__.c.created_at.doc},format="%Y-%m-%dT%H:%M:%S.%f%z")
    schedule_date=ma.auto_field(metadata={'description': Bp1.__table__.c.schedule_date.doc},format='%Y-%m-%d')
    schedule_time=ma.auto_field(metadata={'description': Bp1.__table__.c.schedule_time.doc},format='%H:%M:%S')
