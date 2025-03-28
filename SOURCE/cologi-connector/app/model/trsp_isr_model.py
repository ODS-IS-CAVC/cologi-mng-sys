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
from marshmallow import fields,validate
from database import db,ma

class TrspIsr(db.Model):
    trsp_instruction_id= db.Column(db.String(20), primary_key=True, doc="荷送人が運送依頼メッセージ毎に付与した管理番号")
    trsp_instruction_date_subm_dttm= db.Column(db.String(8), nullable=True, doc="荷送人が運送事業者に対して運送を依頼した日付")
    inv_num_id= db.Column(db.String(20), nullable=True, doc="運送事業者が運送送り状毎に付与した管理番号")
    cmn_inv_num_id= db.Column(db.String(20), nullable=True, doc="運送事業者等が共通に使用できるように統一された運送送り状番号")
    mix_load_num_id= db.Column(db.String(20), nullable=True, doc="他の運送依頼との積み合わせをする時のグループ付けの番号")

class TrspIsrSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrspIsr
        load_instance = True
    trsp_instruction_id= ma.auto_field(metadata={'description': TrspIsr.__table__.c.trsp_instruction_id.doc, 'max_length': 20}, validate=[validate.Length(20),])
    trsp_instruction_date_subm_dttm= ma.auto_field(metadata={'description': TrspIsr.__table__.c.trsp_instruction_date_subm_dttm.doc, 'max_length': 8}, validate=[validate.Length(max=8),])
    inv_num_id= ma.auto_field(metadata={'description': TrspIsr.__table__.c.inv_num_id.doc, 'max_length': 20}, validate=[validate.Length(max=20),])
    cmn_inv_num_id= ma.auto_field(metadata={'description': TrspIsr.__table__.c.cmn_inv_num_id.doc, 'max_length': 20}, validate=[validate.Length(max=20),])
    mix_load_num_id= ma.auto_field(metadata={'description': TrspIsr.__table__.c.mix_load_num_id.doc, 'max_length': 20}, validate=[validate.Length(max=20),])