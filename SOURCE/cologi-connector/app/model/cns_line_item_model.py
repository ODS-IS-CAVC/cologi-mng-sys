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

class CnsLineItem(db.Model):
    __tablename__="cns_line_item"
    cns_line_item_id=db.Column(db.Integer, primary_key=True, doc="The primary key")
    line_item_num_id=db.Column(db.String(10), nullable=False, doc="繰り返しの明細情報を識別する管理番号")
    sev_ord_num_id=db.Column(db.String(23), nullable=False, doc="発注者が注文毎に付与した管理番号（繰り返しの中で使用する）")
    cnsg_crg_item_num_id=db.Column(db.String(15), nullable=True, doc="運送品毎の運送データを特定する為に、荷送人が採番した管理番号")
    buy_assi_item_cd=db.Column(db.String(25), nullable=True, doc="発注者が採番した商品の管理コード")
    sell_assi_item_cd=db.Column(db.String(55), nullable=True, doc="受注者又は寄託者が採番した商品の管理コード")
    wrhs_assi_item_cd=db.Column(db.String(25), nullable=True, doc="倉庫事業者が採番した商品の管理コード")
    item_name_txt=db.Column(db.String(400), nullable=True, doc="商品を表す漢字名称")
    gods_idcs_in_ots_pcke_name_txt=db.Column(db.String(100), nullable=True, doc="運送品に標記する漢字品名、一般的商品名又は代表品名を用いる")
    num_of_istd_untl_quan=db.Column(db.Integer, nullable=True, doc="ユニットロード(パレット等)の依頼(予定)個数")
    num_of_istd_quan=db.Column(db.Integer, nullable=True, doc="運送品又は受寄物の依頼（予定）個数")
    sev_num_unt_cd=db.Column(db.String(3), nullable=True, doc="個数の単位を表すコード（繰り返しの中で使用する）")
    istd_pcke_weig_meas=db.Column(db.Numeric(precision=12, scale=3), nullable=True, doc="運送品毎の運送梱包材込みの依頼(予定)重量")
    sev_weig_unt_cd=db.Column(db.String(3), nullable=True, doc="重量の単位を表すコード（繰り返しの中で使用する）")
    istd_pcke_vol_meas=db.Column(db.Numeric(precision=11, scale=4), nullable=True, doc="運送品毎の運送梱包材込みの依頼(予定)容積")
    sev_vol_unt_cd=db.Column(db.String(3), nullable=True, doc="容積の単位を表すコード（繰り返しの中で使用する）")
    istd_quan_meas=db.Column(db.Numeric(precision=15, scale=4), nullable=True, doc="運送品又は受寄物の依頼(予定)数量")
    cnte_num_unt_cd=db.Column(db.String(3), nullable=True, doc="運送品又は受寄物の数量の単位")
    dcpv_trpn_pckg_txt=db.Column(db.String(20), nullable=True, doc="運送梱包の外形寸法を記述式（横幅Ｘ長さＸ高さ）で表す")
    pcke_frm_cd=db.Column(db.String(3), nullable=True, doc="梱包の形態を表すコード")
    pcke_frm_name_cd=db.Column(db.String(40), nullable=True, doc="梱包の形態の漢字名称（段ボール箱・缶・袋・通箱等）")
    crg_hnd_trms_spcl_isrs_txt=db.Column(db.String(60), nullable=True, doc="横積み厳禁、段積み制限等の荷扱い上の条件を表す（漢字表記）")
    glb_retb_asse_id=db.Column(db.String(14), nullable=True, doc="リターナブル資産識別コード(シリアル番号を除く)")
    totl_rti_quan_quan=db.Column(db.Integer, nullable=True, doc="リターナブル物流容器（RTI）の数量")
    chrg_of_pcke_ctrl_num_unt_amnt=db.Column(db.Integer, nullable=True, doc="梱包管理番号毎に配賦した運賃")

class CnsLineItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CnsLineItem
        load_instance = True
    cns_line_item_id= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.cns_line_item_id.doc, 'max_length':5}, validate=[validate.Range(min=1, max=99999)])
    line_item_num_id= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.line_item_num_id.doc, 'max_length':10}, validate=[validate.Length(max=10)])
    sev_ord_num_id= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.sev_ord_num_id.doc, 'max_length':23}, validate=[validate.Length(max=23)])
    cnsg_crg_item_num_id= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.cnsg_crg_item_num_id.doc, 'max_length':15}, validate=[validate.Length(max=15)])
    buy_assi_item_cd= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.buy_assi_item_cd.doc, 'max_length':25}, validate=[validate.Length(max=25)])
    sell_assi_item_cd= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.sell_assi_item_cd.doc, 'max_length':55}, validate=[validate.Length(max=55)])
    wrhs_assi_item_cd= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.wrhs_assi_item_cd.doc, 'max_length':25}, validate=[validate.Length(max=25)])
    item_name_txt= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.item_name_txt.doc, 'max_length':400}, validate=[validate.Length(max=400)])
    gods_idcs_in_ots_pcke_name_txt= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.gods_idcs_in_ots_pcke_name_txt.doc, 'max_length':100}, validate=[validate.Length(max=100)])
    num_of_istd_untl_quan= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.num_of_istd_untl_quan.doc, 'max_length':9}, validate=[validate.Range(min=1, max=999999999)])
    num_of_istd_quan= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.num_of_istd_quan.doc, 'max_length':9}, validate=[validate.Range(min=1, max=999999999)])
    sev_num_unt_cd= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.sev_num_unt_cd.doc, 'max_length':3}, validate=[validate.Length(max=3)])
    istd_pcke_weig_meas= fields.Decimal(as_string=True, metadata={'description': CnsLineItem.__table__.c.istd_pcke_weig_meas.doc, 'precision':12, 'scale':3})
    sev_weig_unt_cd= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.sev_weig_unt_cd.doc, 'max_length':3}, validate=[validate.Length(max=3)])
    istd_pcke_vol_meas= fields.Decimal(as_string=True, metadata={'description': CnsLineItem.__table__.c.istd_pcke_vol_meas.doc, 'precision':11, 'scale':4})
    sev_vol_unt_cd= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.sev_vol_unt_cd.doc, 'max_length':3}, validate=[validate.Length(max=3)])
    istd_quan_meas= fields.Decimal(as_string=True, metadata={'description': CnsLineItem.__table__.c.istd_quan_meas.doc, 'precision':15, 'scale':4})
    cnte_num_unt_cd= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.cnte_num_unt_cd.doc, 'max_length':3}, validate=[validate.Length(max=3)])
    dcpv_trpn_pckg_txt= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.dcpv_trpn_pckg_txt.doc, 'max_length':20}, validate=[validate.Length(max=20)])
    pcke_frm_cd= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.pcke_frm_cd.doc, 'max_length':3}, validate=[validate.Length(max=3)])
    pcke_frm_name_cd= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.pcke_frm_name_cd.doc, 'max_length':40}, validate=[validate.Length(max=40)])
    crg_hnd_trms_spcl_isrs_txt= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.crg_hnd_trms_spcl_isrs_txt.doc, 'max_length':60}, validate=[validate.Length(max=60)])
    glb_retb_asse_id= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.glb_retb_asse_id.doc, 'max_length':14}, validate=[validate.Length(max=14)])
    totl_rti_quan_quan= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.totl_rti_quan_quan.doc, 'max_length':5}, validate=[validate.Range(min=1, max=99999)])
    chrg_of_pcke_ctrl_num_unt_amnt= ma.auto_field(metadata={'description': CnsLineItem.__table__.c.chrg_of_pcke_ctrl_num_unt_amnt.doc, 'max_length':8}, validate=[validate.Range(min=1, max=99999999)])