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

class package_info(db.Model):
    __tablename__= "package_info"
    package_info_id = db.Column(db.Integer, primary_key=True, nullable=False, doc="パッケージ情報 ID")
    package_code = db.Column(
        CHAR(3), 
        nullable=True, 
        doc="""
        BA :たる（Barrel）､BK :かご（Basket）､BO :瓶（Bottle）､CA :缶（Can）､DR :ﾄﾞﾗﾑ（Drum）､
        CY :ｼﾘﾝﾀﾞｰ（Cylinder）､BX :箱（Box）､PU :ﾄﾚｲ（Tray）､PA :ﾍﾟｰﾙ（Pail）､EN :封筒､
        BGP:紙袋（Paperbag）､RL :巻（Roll）､BGC:布袋（Clothbag）､CO :ｺﾝﾃﾅ（Container）､
        BGO:ﾎﾟﾘ袋､COF:ﾌﾚｺﾝ､BG :袋（Bag）､RP :連包装､CT :紙器（Carton）､HA :ﾊﾝｶﾞｰ（Hanger）､
        CP :段ﾎﾞｰﾙ､NA :裸､PL :ﾊﾟﾚｯﾄ（Pallet）､RB :ｶｺﾞ車（RollBox）､CR :ｸﾚｰﾄ（Crate）､
        FC :ｵﾘｺﾝ（Folding Container）､BJ :ばんじゅう（Banju）､MP :未包装､ETC:その他
        """)
    package_name_kanji = db.Column(db.String(40), nullable=False, doc="荷姿名（漢字）")
    width = db.Column(db.Numeric(precision=15, scale=6), nullable=False, doc="幅")
    height = db.Column(db.Numeric(precision=15, scale=6), nullable=False, doc="高さ")
    depth = db.Column(db.Numeric(precision=15, scale=6), nullable=False, doc="奥行き")
    dimension_unit_code = db.Column(
        CHAR(3), 
        nullable=False, 
        doc="""
        CS :ｹｰｽ（Case）、DZN:ﾀﾞｰｽ（Dozen）、BL :ﾎﾞｰﾙ（Bowl）、TNE:ﾄﾝ（Tonne）、PCE:個（Piece）、G  :ｸﾞﾗﾑ（Gram）、
        CY :ｼﾘﾝﾀﾞ（Cylinder）、KG :ｷﾛｸﾞﾗﾑ、BK :かご（Basket）、MG :ﾐﾘｸﾞﾗﾑ、BG :袋（Bag）、LB :ﾎﾟﾝﾄﾞ（Pound）、
        PL :ﾊﾟﾚｯﾄ（Pallet）、OZ :ｵﾝｽ（Ounce）、RN :連、M  :ﾒｰﾄﾙ（Meter）、BR :ﾎﾞｰﾄﾞ連、KM :ｷﾛﾒｰﾄﾙ、
        SA :才、CM :ｾﾝﾁﾒｰﾄﾙ、ST :枚（Sheet）、MM :ﾐﾘﾒｰﾄﾙ、RL :巻（Roll）、IN :ｲﾝﾁ（Inch）、
        VL :冊（Volume）、FT :ﾌｨｰﾄ（Foot）、CA :缶（Can）、QT :ｸｫｰﾄ（Quart）、SET:式（Set）、M2 :平方ﾒｰﾄﾙ、
        UT :組（Unit）、CM2:平方ｾﾝﾁﾒｰﾄ、BX :箱（Box）、M3 :立方ﾒｰﾄﾙ、BA :樽（Barrel）、DM3:立方ﾃﾞｼﾒｰﾄﾙ、
        DR :ﾄﾞﾗﾑ（Drum）、CM3:立方ｾﾝﾁﾒｰﾄﾙ、CC :ｶｰｶｽ（Carcass）、L  :ﾘｯﾄﾙ（Liter）、KPC:千個､千台、GAL:ｶﾞﾛﾝ（Gallon）
        CP :部（Copy）、HR :時間（Hour）、BT :本（Bottle）、W  :ﾜｯﾄ（Watt）、PR :一対（Pair）、WH :ﾜｯﾄ時、
        PK :一包み（Pack）、VA :ﾎﾞﾙﾄｱﾝﾍﾟｱ、GRO:ｸﾞﾛｽ（Gross）、ETC:その他、ML :ﾐﾘﾘｯﾄﾙ､cc、KL :ｷﾛﾘｯﾄﾙ、
        YD :ﾔｰﾄﾞ、GR :粒、TB :錠、CAP:ｶﾌﾟｾﾙ、AC :匹、FC :尾
        """)
    max_load_quantity = db.Column(db.Numeric(2), nullable=False, doc="最大積載数")

class package_info_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = package_info
        load_instance = True
    package_info_id = ma.auto_field(metadata={
        'description': package_info.__table__.c.package_info_id.doc,
        "max_length":5},
        validate=[validate.Range(min=1,max=99999),])
    package_code = fields.String(metadata={
        'description': package_info.__table__.c.package_code.doc,
        'max_length':3,
        'example':"BA "},
        validate=[validate.Length(equal=3),])
    package_name_kanji = ma.auto_field(metadata={
        'description': package_info.__table__.c.package_name_kanji.doc,
        'max_length':40},
        validate=[validate.Length(max=40),])
    width = fields.Decimal(as_string=True, metadata={
        'description': package_info.__table__.c.width.doc,
        'precision':15,'scale':6})
    height = fields.Decimal(as_string=True, metadata={
        'description': package_info.__table__.c.height.doc,
        'precision':15,'scale':6})
    depth = fields.Decimal(as_string=True, metadata={
        'description': package_info.__table__.c.depth.doc,
        'precision':15,'scale':6})
    dimension_unit_code = fields.String(metadata={
        'description': package_info.__table__.c.dimension_unit_code.doc,
        'max_length':3,
        'example':"CS "},
        validate=[validate.Length(equal=3),])
    max_load_quantity = ma.auto_field(metadata={
        'description': package_info.__table__.c.max_load_quantity.doc,
        "max_length":2},
        validate=[validate.Range(min=1,max=99),])
