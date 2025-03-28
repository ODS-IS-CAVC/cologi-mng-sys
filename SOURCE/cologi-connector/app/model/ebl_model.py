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

import sys
import os
import uuid
import json
from pytz import timezone
from datetime import datetime
from marshmallow import fields
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from database import db, ma


class EBL(db.Model):
    __tablename__ = "ebl"
    id = db.Column(
        db.Integer, primary_key=True, doc="The unique id", autoincrement=True
    )  # created to have a primary key
    bl_no = db.Column(db.String(100), nullable=False, doc="B/L管理番号")
    bl_data = db.Column(
        db.String(4000), nullable=False, doc="B/Lデータ eFBL JSON String"
    )
    bl_cid = db.Column(
        db.String(256),
        doc="B/L発行者の事業者ID",
    )
    recipient_cid = db.Column(
        db.String(256),
        doc="荷受け人の事業者ID",
    )
    trailer_giai_list_str = db.Column(
        db.String(140),
        nullable=True,
        doc="使用するトレーラーのGIAIのリスト（カンマ区切りの文字列）",
    )
    trsp_instruction_id = db.Column(
        db.String(20),
        doc="trsp_instruction_id",
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc="作成日時",
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        doc="更新日時",
    )

    @hybrid_property
    def bl(self) -> dict:
        if self.bl_data is None or self.bl_data == "":
            return {}
        else:
            try:
                return json.loads(
                    self.bl_data,
                )
            except:
                return {}

    @hybrid_property
    def trailer_giai_list(self) -> list[str]:
        if self.trailer_giai_list_str is None or self.trailer_giai_list_str == "":
            return []
        return self.trailer_giai_list_str.split(",")


class EBLSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        model = EBL
        load_instance = True
        exclude = ("id", "bl_data")

    id = ma.auto_field(
        metadata={"description": EBL.__table__.c.id.doc, "max_length": 5}
    )
    bl_no = ma.auto_field(
        metadata={
            "description": EBL.__table__.c.bl_no.doc,
            "max_length": 100,
            "example": "7845487545",
        },
    )
    bl_data = ma.auto_field(
        metadata={
            "description": EBL.__table__.c.bl_data.doc,
            "max_length": 4000,
            "example": "{'exchanged_document':{...}}",
        },
    )
    bl_cid = ma.auto_field(
        metadata={
            "description": EBL.__table__.c.bl_cid.doc,
            "max_length": 256,
            "example": "992000001",
        },
    )
    recipient_cid = ma.auto_field(
        metadata={
            "description": EBL.__table__.c.recipient_cid.doc,
            "max_length": 256,
            "example": "991000001",
        },
    )
    trailer_giai_list = fields.List(
        fields.Str(),
        allow_none=True,
        metadata={
            "description": "使用するトレーラーのGIAIのリスト",
            "example": [
                "8004991000001000000000000000000001",
                "8004991000001000000000000000000002",
            ],
        },
    )
    trsp_instruction_id = ma.auto_field(
        metadata={
            "description": EBL.__table__.c.trsp_instruction_id.doc,
            "max_length": 20,
            "example": "12345678901",
        },
    )
    created_at = ma.auto_field(
        metadata={
            "description": EBL.__table__.c.created_at.doc,
            "max_length": 256,
            "example": "20250225",
        },
    )
    updated_at = ma.auto_field(
        metadata={
            "description": EBL.__table__.c.updated_at.doc,
            "max_length": 256,
            "example": "20250114",
        },
    )


class EblJson:

    def __init__(self):
        self.ebl = {
            "exchanged_document": {
                "id": "RRRRRRRR-RRRR-4RRR-9RRR-RRRRRRRRRRRR",
                "issueDateTime": {
                    "value": "0000-12-31T00:00:00.000000",
                    "format": "YYYY-MM-DDTHH:mm:ss.ssssss",
                },
                "originalIssuedQuantity": "1",
                "documentStatus": {"value": "TBD"},
                "issueLocation": {
                    "id": "JPTYO",  # 本来はUN/LOCODE,2024年度は東京固定
                    "countryCode": "JP",
                },
                "firstSignatoryAuthentication": {
                    "actualDateTime": {
                        "value": "0000-12-31T00:00:00.000000",
                        "format": "YYYY-MM-DDTHH:mm:ss.ssssss",
                    },
                    "id": "XXXXXXX",
                },
            },
            "supply_chain_consignment": {
                "consignor": {
                    # 荷送人、荷主：shipper
                    "id": [
                        {
                            "value": "XXXXXX",
                            "identificationScheme": "USERID",
                            "identificationSchemeAgency": "COLOGI",
                        }
                    ],
                    "name": {
                        "value": "",
                        "language": "ja",
                    },
                    "languageCode": {
                        "value": "ja",
                    },
                },
                "consignee": {
                    # 荷受人：recipient
                    "id": [
                        {
                            "value": "XXXXXX",
                            "identificationScheme": "USERID",
                            "identificationSchemeAgency": "COLOGI",
                        }
                    ],
                    "name": {
                        "value": "",
                        "language": "ja",
                    },
                    "languageCode": {
                        "value": "ja",
                    },
                },
                "carrierAcceptanceLocation": {
                    # 発MH
                    "id": "JPTYO",  # 本来はUN/LOCODE,2024年度は東京固定
                    "name": {
                        "value": "414999990001XXXX:発MH",  # 2024年度はMHの"GLN:MH名"
                        "language": "ja",
                    },
                    "countryCode": "JP",
                },
                "consigneeReceiptLocation": {
                    # 着MH
                    "id": "JPTYO",  # 本来はUN/LOCODE,2024年度は東京固定
                    "name": {
                        "value": "414999990001XXXX:着MH",  # 2024年度はMHの"GLN:MH名"
                        "language": "ja",
                    },
                    "countryCode": "JP",
                },
                "includedConsignmentItem": [{"associatedTransportEquipment": []}],
                "mainCarriageTransportMovement": [],
            },
        }

    def load_file(self, file_path) -> int:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.ebl = data["signed_bl"]
            return int(data["bl_id"])
        except Exception:
            return -1

    def issue(self, issue_user_id) -> dict:
        utc_now = datetime.now(timezone("UTC"))
        exchanged_document = self.ebl["exchanged_document"]
        exchanged_document["id"] = str(uuid.uuid4())
        exchanged_document["issueDateTime"]["value"] = utc_now.strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        exchanged_document["firstSignatoryAuthentication"]["actualDateTime"][
            "value"
        ] = utc_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        exchanged_document["firstSignatoryAuthentication"]["id"] = issue_user_id

        return self.ebl

    def _set_trade_party(self, item: dict, user_id: str, user_name: str = ""):
        item["id"][0]["value"] = user_id
        if user_name == "":
            item.pop("name")
        else:
            item["name"]["value"] = user_name
            item["name"]["language"] = "ja"

    def _set_logistics_location(self, item: dict, location: str = ""):
        item["name"]["value"] = location

    def set_shipper(self, cid: str, user_name: str = ""):
        self._set_trade_party(
            self.ebl["supply_chain_consignment"]["consignor"],
            cid,
            user_name,
        )

    def set_recipient(self, cid: str, user_name: str = ""):
        self._set_trade_party(
            self.ebl["supply_chain_consignment"]["consignee"],
            cid,
            user_name,
        )

    def set_departure_mh(self, mh_gln: str, mh_name: str = ""):
        location = f"{mh_gln}:{mh_name}"
        self._set_logistics_location(
            self.ebl["supply_chain_consignment"]["carrierAcceptanceLocation"],
            location,
        )

    def set_arrival_mh(self, mh_gln: str, mh_name: str = ""):
        location = f"{mh_gln}:{mh_name}"
        self._set_logistics_location(
            self.ebl["supply_chain_consignment"]["consigneeReceiptLocation"],
            location,
        )

    def set_trailers(self, trailer_list: list):
        self.ebl["supply_chain_consignment"]["includedConsignmentItem"] = [
            {"associatedTransportEquipment": []}
        ]
        associated_transport_equipment = self.ebl["supply_chain_consignment"][
            "includedConsignmentItem"
        ][0]["associatedTransportEquipment"]
        for trailer in trailer_list:
            item = {
                "id": {
                    "value": trailer,
                    "identificationScheme": "GIAI",
                    "identificationSchemeAgency": "GS1",
                }
            }
            associated_transport_equipment.append(item)

    def set_shipper_tractor(self, giai):
        mainCarriageTransportMovement = self.ebl["supply_chain_consignment"][
            "mainCarriageTransportMovement"
        ]
        mainCarriageTransportMovement.append(
            {
                "typeCode": {"value": "3"},
                "typeText": {
                    "value": "荷主トラクター",
                    "language": "ja",
                },
                "id": {
                    "value": giai,
                    "identificationScheme": "GIAI",
                    "identificationSchemeAgency": "GS1",
                },
                "stageCode": {"value": "1"},
            }
        )

    def set_recipient_tractor(self, giai):
        mainCarriageTransportMovement = self.ebl["supply_chain_consignment"][
            "mainCarriageTransportMovement"
        ]
        mainCarriageTransportMovement.append(
            {
                "typeCode": {"value": "3"},
                "typeText": {
                    "value": "荷受人トラクター",
                    "language": "ja",
                },
                "id": {
                    "value": giai,
                    "identificationScheme": "GIAI",
                    "identificationSchemeAgency": "GS1",
                },
                "stageCode": {"value": "21"},
            }
        )

    def get_string(self) -> str:
        return json.dumps(self.ebl, ensure_ascii=False)

    def get_ebl(self) -> dict:
        return self.ebl

    def get_issue_user_id(self) -> str:
        exchanged_document = self.ebl["exchanged_document"]
        issue_user_id = exchanged_document["firstSignatoryAuthentication"]["id"]
        return issue_user_id

    def get_recipient_cid(self) -> str:
        recipient_info = self.ebl["supply_chain_consignment"]["consignee"]
        return recipient_info["id"][0]["value"]

    def get_shipper_cid(self) -> str:
        shipper_info = self.ebl["supply_chain_consignment"]["consignor"]
        return shipper_info["id"][0]["value"]

    def get_trailers_giai(self):
        associated_transport_equipment = self.ebl["supply_chain_consignment"][
            "includedConsignmentItem"
        ][0]["associatedTransportEquipment"]
        return associated_transport_equipment
    
    def get_rshipper_tractor(self):
        mainCarriageTransportMovement = self.ebl["supply_chain_consignment"][
            "mainCarriageTransportMovement"
        ]
        for m in mainCarriageTransportMovement:
            if m["stageCode"]["value"] == "1":
                return m["id"]["value"]
    
    def get_recipient_tractor(self):
        mainCarriageTransportMovement = self.ebl["supply_chain_consignment"][
            "mainCarriageTransportMovement"
        ]
        for m in mainCarriageTransportMovement:
            if m["stageCode"]["value"] == "21":
                return m["id"]["value"]