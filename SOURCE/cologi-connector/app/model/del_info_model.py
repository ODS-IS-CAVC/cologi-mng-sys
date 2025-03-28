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
from database import db,ma

class DelInfo(db.Model):
    __tablename__="del_info"
    del_info_id=db.Column(db.Integer, primary_key=True, doc="The primary key")
    del_note_id=db.Column(db.String(23), nullable=True, doc="１回の納品を特定するための管理番号")
    shpm_num_id=db.Column(db.String(20), nullable=True, doc="荷送人が出荷単位に付与した管理番号")
    rced_ord_num_id=db.Column(db.String(23), nullable=True, doc="受注者が受注単位に付与した管理番号")

class DelInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= DelInfo
        load_instance = True
    del_info_id= ma.auto_field(metadata={'description': DelInfo.__table__.c.del_info_id.doc, 'max_length':5}, validate=[validate.Range(min=1, max=99999)])
    del_note_id= ma.auto_field(metadata={'description': DelInfo.__table__.c.del_note_id.doc, 'max_length':23}, validate=[validate.Length(max=23)])
    shpm_num_id= ma.auto_field(metadata={'description': DelInfo.__table__.c.shpm_num_id.doc, 'max_length':20}, validate=[validate.Length(max=20)])
    rced_ord_num_id= ma.auto_field(metadata={'description': DelInfo.__table__.c.rced_ord_num_id.doc, 'max_length':23}, validate=[validate.Length(max=23)])