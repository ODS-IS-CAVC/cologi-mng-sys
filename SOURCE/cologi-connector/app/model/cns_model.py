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


class Cns(db.Model):
    __tablename__="cns"
    cns_id= db.Column(db.Integer, primary_key=True, doc="The primary keys")
    istd_totl_pcks_quan= db.Column(db.Integer, nullable=False, doc="運送梱包の個数単位に基づく依頼（予定）総個数")
    num_unt_cd= db.Column(db.String(3), nullable=True, doc="個数の単位を表すコード（繰り返しの外で使用する）")
    istd_totl_weig_meas= db.Column(db.Numeric(precision=14, scale=3), nullable=True, doc="運送梱包の重量単位に基づく依頼（予定）総重量")
    weig_unt_cd= db.Column(db.String(3), nullable=True, doc="重量の単位を表すコード（繰り返しの外で使用する）")
    istd_totl_vol_meas= db.Column(db.Numeric(precision=11, scale=3), nullable=True, doc="運送梱包の容積単位に基づく依頼（予定）総容積")
    vol_unt_cd= db.Column(db.String(3), nullable=True, doc="容積の単位を表すコード（繰り返しの外で使用する）")
    istd_totl_untl_quan= db.Column(db.Integer, nullable=True, doc="ユニットロード(パレット等)の依頼(予定)合計個数")
    
class CnsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cns
        load_instance= True
    cns_id= ma.auto_field(metadata={'description': Cns.__table__.c.cns_id.doc, 'max_length':5}, validate=[validate.Range(min=1, max=99999)])
    istd_totl_pcks_quan= ma.auto_field(metadata={'description': Cns.__table__.c.istd_totl_pcks_quan.doc, 'max_length':9}, validate=[validate.Range(min=1, max=999999999)])
    num_unt_cd= ma.auto_field(metadata={'description': Cns.__table__.c.num_unt_cd.doc, 'max_length': 3}, validate=[validate.Length(max=3),])
    istd_totl_weig_meas= fields.Decimal(as_string=True, metadata={'description': Cns.__table__.c.istd_totl_weig_meas.doc, 'precision':14, 'scale':3})
    weig_unt_cd= ma.auto_field(metadata={'description': Cns.__table__.c.weig_unt_cd.doc, 'max_length':3}, validate=[validate.Length(max=3)])
    istd_totl_vol_meas= fields.Decimal(as_string=True, metadata={'description': Cns.__table__.c.istd_totl_vol_meas.doc, 'precision':11, 'scale':3})
    vol_unt_cd= ma.auto_field(metadata={'description': Cns.__table__.c.vol_unt_cd.doc, 'max_length':3}, validate=[validate.Length(max=3)])
    istd_totl_untl_quan= ma.auto_field(metadata={'description': Cns.__table__.c.istd_totl_untl_quan.doc, 'max_length':9}, validate=[validate.Range(min=1 ,max=999999999)])
