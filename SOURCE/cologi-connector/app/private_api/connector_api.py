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

from flask_restx import Namespace, Resource, fields
from flask import request
from datetime import datetime
import uuid
from enum import Enum

# import aiohttp
# import asyncio
# import nest_asyncio

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# from database import db
# from com.helper import create_restx_model_usingSchema
# from dataspace.dataspace import check_access
# from model.asset_model import Asset, AssetSchema
# from model.asset_properties_model import AssetProperties

# API
connector_private_api_ns = Namespace(
    "/private/api", description="private API for connector"
)


# Classes
class NegotiationError(Exception):
    pass


class TransferError(Exception):
    """Custom exception for transfer errors"""

    pass


class NegotiationState(Enum):
    REQUESTING = "REQUESTING"
    REQUESTED = "REQUESTED"
    VALIDATING = "VALIDATING"
    AGREEING = "AGREEING"
    AGREED = "AGREED"
    DECLINING = "DECLINING"
    DECLINED = "DECLINED"
    FAILED = "FAILED"


class TransferState(Enum):
    INITIAL = "INITIAL"
    REQUESTED = "REQUESTED"
    VALIDATING = "VALIDATING"
    PROVISIONING = "PROVISIONING"
    PROVISIONED = "PROVISIONED"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# Detailed API Models
asset_property = connector_private_api_ns.model(
    "AssetProperty",
    {
        "name": fields.String(required=True),
        "value": fields.String(required=True),
    },
)

data_address = connector_private_api_ns.model(
    "DataAddress",
    {
        "type": fields.String(required=True),
        "baseUrl": fields.String(required=True),
        "proxyPath": fields.String(required=False),
    },
)

asset_model = connector_private_api_ns.model(
    "Asset",
    {
        "id": fields.String(required=False),
        "properties": fields.List(fields.Nested(asset_property)),
        "dataAddress": fields.Nested(data_address),
    },
)

constraint_model = connector_private_api_ns.model(
    "Constraint",
    {
        "type": fields.String(required=True, example="BPN"),
        "operator": fields.String(required=True, example="eq"),
        "value": fields.String(required=True, example="BPN12345"),
    },
)

permission_model = connector_private_api_ns.model(
    "Permission",
    {
        "action": fields.String(required=True, example="USE"),
        "constraints": fields.List(fields.Nested(constraint_model)),
    },
)

policy_request_model = connector_private_api_ns.model(
    "PolicyRequest",
    {
        "id": fields.String(required=True, example="policy-123"),
        "permissions": fields.List(fields.Nested(permission_model)),
    },
)

contract_def_request_model = connector_private_api_ns.model(
    "ContractDefinitionRequest",
    {
        "id": fields.String(required=True, example="contract-def-123"),
        "accessPolicyId": fields.String(required=True, example="policy-123"),
        "contractPolicyId": fields.String(required=True, example="policy-456"),
        "assetId": fields.String(required=True, example="asset-123"),
    },
)

catalog_item_model = connector_private_api_ns.model(
    "CatalogItem",
    {
        "id": fields.String(required=True),
        "title": fields.String(required=True),
        "description": fields.String(required=True),
        "assetId": fields.String(required=True),
        "policies": fields.List(fields.String(required=True)),
    },
)

catalog_request_model = connector_private_api_ns.model(
    "CatalogRequest",
    {
        "bpn": fields.String(required=True, example="BPN12345"),
        "limit": fields.Integer(required=False, example=10),
        "offset": fields.Integer(required=False, example=0),
    },
)

negotiation_request_model = connector_private_api_ns.model(
    "NegotiationRequest",
    {
        "bpn": fields.String(required=True, description="Business Partner Number"),
        "catalog_item_id": fields.String(required=True),
        "offer_details": fields.Raw(description="Negotiation terms"),
        "limit": fields.Integer(default=10),
        "offset": fields.Integer(default=0),
    },
)

negotiation_state_model = connector_private_api_ns.model(
    "NegotiationState",
    {
        "state": fields.String(
            required=True,
            example="AGREED",
            description="New state for the negotiation",
            enum=[state.value for state in NegotiationState],  # Add enum validation
        ),
    },
)

transfer_request_model = connector_private_api_ns.model(
    "TransferRequest",
    {
        "negotiationId": fields.String(required=True),
    },
)

# nest_asyncio.apply()


class DataStorage:
    def __init__(self):
        self.assets = {}
        self.policies = {}
        self.contracts = {}
        self.catalog = {}
        self.tokens = {}
        self.negotiations = {}
        self.transfers = {}

    def create_asset(self, data):
        asset_id = str(uuid.uuid4()) if "id" not in data else data["id"]
        asset = {
            "id": asset_id,
            "createdAt": datetime.utcnow().isoformat(),
            "properties": data.get("properties", []),
            "dataAddress": data.get("dataAddress", {}),
            "status": "ACTIVE",
        }
        self.assets[asset_id] = asset
        return asset

    def create_policy(self, data):
        policy_id = data.get("id", str(uuid.uuid4()))
        policy = {
            "id": policy_id,
            "createdAt": datetime.utcnow().isoformat(),
            "permissions": data.get("permissions", []),
            "status": "ACTIVE",
        }
        self.policies[policy_id] = policy
        return policy

    def create_contract(self, data):
        contract_id = data.get("id", str(uuid.uuid4()))
        contract = {
            "id": contract_id,
            "createdAt": datetime.utcnow().isoformat(),
            "assetId": data.get("assetId"),
            "accessPolicyId": data.get("accessPolicyId"),
            "contractPolicyId": data.get("contractPolicyId"),
            "status": "ACTIVE",
        }
        self.contracts[contract_id] = contract
        return contract

    def get_asset(self, asset_id):
        return self.assets.get(asset_id)

    def get_policy(self, policy_id):
        return self.policies.get(policy_id)

    def get_contract(self, contract_id):
        return self.contracts.get(contract_id)

    def list_assets(self):
        return list(self.assets.values())

    def list_policies(self):
        return list(self.policies.values())

    def list_contracts(self):
        return list(self.contracts.values())

    def get_catalog_items(self, bpn, limit=10, offset=0):
        """Get catalog items available for the given BPN"""
        available_items = []
        for asset_id, asset in self.assets.items():
            # Check if asset has any policies that allow this BPN
            valid_policies = self._get_valid_policies_for_bpn(asset_id, bpn)
            if valid_policies:
                item = {
                    "id": str(uuid.uuid4()),
                    "title": self._get_asset_property(asset, "name", "Untitled Asset"),
                    "description": self._get_asset_property(
                        asset, "description", "No description available"
                    ),
                    "assetId": asset_id,
                    "policies": valid_policies,
                }
                available_items.append(item)
        # Apply pagination
        start = offset
        end = offset + limit
        return available_items[start:end]

    def _get_valid_policies_for_bpn(self, asset_id, bpn):
        """Get list of policy IDs that allow the given BPN for an asset"""
        valid_policies = []

        for contract in self.contracts.values():
            if contract["assetId"] != asset_id:
                continue

            access_policy = self.policies.get(contract["accessPolicyId"])
            if access_policy and self._policy_allows_bpn(access_policy, bpn):
                valid_policies.append(contract["accessPolicyId"])

        return valid_policies

    def _policy_allows_bpn(self, policy, bpn):
        """Check if policy allows the given BPN"""
        for permission in policy.get("permissions", []):
            for constraint in permission.get("constraints", []):
                if (
                    constraint["type"] == "BPN"
                    and constraint["operator"] == "eq"
                    and constraint["value"] == bpn
                ):
                    return True
        return False

    def _get_asset_property(self, asset, property_name, default=""):
        """Get asset property value by name

        Args:
            asset (dict): Asset dictionary containing properties
            property_name (str): Name of the property to find
            default (str): Default value if property not found

        Returns:
            str: Property value or default if not found
        """
        if not asset or not isinstance(asset, dict):
            return default

        properties = asset.get("properties", [])
        if not properties or not isinstance(properties, list):
            return default

        for prop in properties:
            if isinstance(prop, dict) and prop.get("name") == property_name:
                return prop.get("value", default)

        return default

    def create_negotiation(self, bpn, catalog_item_id, offer_details=None):
        try:
            # Input validation
            if not bpn:
                raise NegotiationError("BPN is required")
            if not catalog_item_id:
                raise NegotiationError("Catalog item ID is required")

            # Get asset details
            asset = self.assets.get(catalog_item_id)
            if not asset:
                raise NegotiationError(f"Asset {catalog_item_id} not found")

            # Get valid policies for the asset
            valid_policies = self._get_valid_policies_for_bpn(catalog_item_id, bpn)
            if not valid_policies:
                raise NegotiationError(f"No valid policies found for BPN {bpn}")

            negotiation_id = str(uuid.uuid4())
            current_time = datetime.utcnow().isoformat()

            negotiation = {
                "id": negotiation_id,
                "bpn": bpn,
                "assetId": catalog_item_id,
                "state": NegotiationState.REQUESTED.value,
                "offerDetails": offer_details or {},
                "providerId": self._get_asset_property(asset, "providerId"),
                "accessPolicyId": valid_policies[0],
                "createdAt": current_time,
                "updatedAt": current_time,
                "stateHistory": [
                    {
                        "state": NegotiationState.REQUESTED.value,
                        "timestamp": current_time,
                    }
                ],
            }

            # Additional validation
            provider_id = negotiation["providerId"]
            if not provider_id:
                raise NegotiationError("Provider ID not found in asset properties")

            self.negotiations[negotiation_id] = negotiation
            return negotiation

        except NegotiationError as e:
            raise e
        except Exception as e:
            raise NegotiationError(f"Failed to create negotiation: {str(e)}")

    def update_negotiation_state(self, negotiation_id, new_state, reason=None):
        """Update negotiation state with history tracking"""
        if negotiation_id not in self.negotiations:
            raise NegotiationError("Negotiation not found")

        negotiation = self.negotiations[negotiation_id]
        current_time = datetime.utcnow().isoformat()

        # Add to state history
        state_change = {"state": new_state, "timestamp": current_time}
        if reason:
            state_change["reason"] = reason

        negotiation["stateHistory"].append(state_change)

        # Update current state
        negotiation["state"] = new_state
        negotiation["updatedAt"] = current_time

        return negotiation

    def get_negotiation(self, negotiation_id):
        return self.negotiations.get(negotiation_id)

    def update_negotiation(self, negotiation_id, **updates):
        if negotiation_id not in self.negotiations:
            return None

        negotiation = self.negotiations[negotiation_id]
        negotiation.update(updates)
        negotiation["updatedAt"] = str(datetime.now())
        return negotiation

    # def create_transfer(self, negotiation_id):
    #     try:
    #         # Get negotiation details
    #         negotiation = self.negotiations.get(negotiation_id)
    #         if not negotiation:
    #             raise TransferError(f"Negotiation {negotiation_id} not found")

    #         if negotiation["state"] != NegotiationState.AGREED.value:
    #             raise TransferError(
    #                 "Transfer can only be initiated for agreed negotiations"
    #             )

    #         # Create transfer record
    #         transfer_id = str(uuid.uuid4())
    #         current_time = datetime.utcnow().isoformat()

    #         transfer = {
    #             "id": transfer_id,
    #             "negotiationId": negotiation_id,
    #             "assetId": negotiation["assetId"],
    #             "bpn": negotiation["bpn"],
    #             "state": TransferState.INITIAL.value,
    #             "createdAt": current_time,
    #             "updatedAt": current_time,
    #             "stateHistory": [
    #                 {"state": TransferState.INITIAL.value, "timestamp": current_time}
    #             ],
    #         }

    #         self.transfers[transfer_id] = transfer

    #         # Create new event loop for async operations
    #         loop = asyncio.new_event_loop()
    #         asyncio.set_event_loop(loop)

    #         # Run the async task
    #         loop.run_until_complete(self.process_transfer(transfer_id))

    #         return transfer

    #     except Exception as e:
    #         raise TransferError(f"Failed to create transfer: {str(e)}")

    # async def process_transfer(self, transfer_id):
    #     """Process the data transfer asynchronously"""
    #     try:
    #         transfer = self.transfers.get(transfer_id)
    #         if not transfer:
    #             raise TransferError("Transfer not found")

    #         # Update state to VALIDATING
    #         self.update_transfer_state(transfer_id, TransferState.VALIDATING.value)

    #         # Get asset details
    #         asset = self.assets.get(transfer["assetId"])
    #         if not asset:
    #             raise TransferError("Asset not found")

    #         # Validate data address
    #         data_address = asset.get("dataAddress")
    #         if not data_address:
    #             raise TransferError("Data address not found in asset")

    #         # Update state to PROVISIONING
    #         self.update_transfer_state(transfer_id, TransferState.PROVISIONING.value)

    #         try:
    #             # Get data based on address type
    #             data = await self._fetch_data(data_address)

    #             # Update state to STARTED
    #             self.update_transfer_state(transfer_id, TransferState.STARTED.value)

    #             # Process and deliver data
    #             await self._deliver_data(transfer, data)

    #             # Update state to COMPLETED
    #             self.update_transfer_state(
    #                 transfer_id,
    #                 TransferState.COMPLETED.value,
    #                 {"message": "Transfer completed successfully"},
    #             )
    #         except Exception as e:
    #             self.update_transfer_state(
    #                 transfer_id, TransferState.FAILED.value, {"error": str(e)}
    #             )
    #             raise TransferError(f"Transfer process failed: {str(e)}")

    #     except Exception as e:
    #         self.update_transfer_state(
    #             transfer_id, TransferState.FAILED.value, {"error": str(e)}
    #         )
    #         raise TransferError(f"Transfer failed: {str(e)}")

    # async def _fetch_data(self, data_address):
    #     """Fetch data from source based on data address type"""
    #     try:
    #         address_type = data_address.get("type", "").lower()

    #         if address_type == "http":
    #             # For development/testing, return dummy data
    #             return b"Test data payload for development purposes"

    #             # If you want to actually fetch from URL, use this instead:
    #             """
    #             async with aiohttp.ClientSession() as session:
    #                 # Configure longer timeout
    #                 timeout = aiohttp.ClientTimeout(
    #                     total=30,  # 30 seconds total timeout
    #                     connect=10,  # 10 seconds connection timeout
    #                     sock_connect=10,  # 10 seconds to establish connection
    #                     sock_read=10  # 10 seconds to read data
    #                 )

    #                 headers = {
    #                     'User-Agent': 'Mozilla/5.0',
    #                     'Accept': '*/*'
    #                 }

    #                 async with session.get(
    #                     data_address["baseUrl"],
    #                     timeout=timeout,
    #                     headers=headers,
    #                     ssl=False  # Disable SSL verification for testing
    #                 ) as response:
    #                     if response.status != 200:
    #                         raise TransferError(
    #                             f"HTTP fetch failed with status {response.status}"
    #                         )
    #                     return await response.read()
    #             """

    #         elif address_type == "s3":
    #             # Mock S3 data for testing
    #             return b"Mock S3 data"

    #         elif address_type == "azure":
    #             # Mock Azure data for testing
    #             return b"Mock Azure data"

    #         else:
    #             raise TransferError(f"Unsupported data address type: {address_type}")

    #     except asyncio.TimeoutError as e:
    #         raise TransferError(
    #             f"Connection timeout to host {data_address['baseUrl']}: {str(e)}"
    #         )
    #     except aiohttp.ClientError as e:
    #         raise TransferError(f"HTTP request failed: {str(e)}")
    #     except Exception as e:
    #         raise TransferError(f"Data fetch failed: {str(e)}")

    # async def _deliver_data(self, transfer, data):
    #     """Deliver data to the consumer"""
    #     try:
    #         negotiation = self.negotiations[transfer["negotiationId"]]
    #         delivery_url = negotiation.get("offerDetails", {}).get("deliveryUrl")

    #         if not delivery_url:
    #             # For testing, just log the data length
    #             print(f"Test delivery: Received {len(data)} bytes of data")
    #             return

    #         # If you want to actually deliver to URL, use this:
    #         """
    #         async with aiohttp.ClientSession() as session:
    #             timeout = aiohttp.ClientTimeout(total=30)
    #             async with session.post(
    #                 delivery_url,
    #                 data=data,
    #                 timeout=timeout,
    #                 ssl=False
    #             ) as response:
    #                 if response.status != 200:
    #                     raise TransferError(
    #                         f"Data delivery failed with status {response.status}"
    #                     )
    #         """

    #     except Exception as e:
    #         raise TransferError(f"Data delivery failed: {str(e)}")

    # def update_transfer_state(self, transfer_id, new_state, result=None):
    #     """Update transfer state with history tracking"""
    #     if transfer_id not in self.transfers:
    #         raise TransferError("Transfer not found")

    #     transfer = self.transfers[transfer_id]
    #     current_time = datetime.utcnow().isoformat()

    #     # Add to state history
    #     state_change = {"state": new_state, "timestamp": current_time}
    #     if result:
    #         state_change["result"] = result

    #     transfer["stateHistory"].append(state_change)

    #     # Update current state
    #     transfer["state"] = new_state
    #     transfer["updatedAt"] = current_time

    #     return transfer

    # def get_transfer(self, transfer_id):
    #     """Get transfer status"""
    #     transfer = self.transfers.get(transfer_id)
    #     if not transfer:
    #         raise TransferError("Transfer not found")
    #     return transfer


# Initialize storage
storage = DataStorage()


# Asset endpoints
@connector_private_api_ns.route("assets")
class AssetCollection(Resource):
    @connector_private_api_ns.doc("list_assets")
    def get(self):
        """List all assets"""
        return storage.list_assets()

    @connector_private_api_ns.doc("create_asset")
    @connector_private_api_ns.expect(asset_model)
    def post(self):
        """Create a new asset"""
        asset = storage.create_asset(request.json)
        return asset, 201


@connector_private_api_ns.route("assets/<string:id>")
class AssetResource(Resource):
    @connector_private_api_ns.doc("get_asset")
    def get(self, id):
        """Get an asset by ID"""
        asset = storage.get_asset(id)
        return asset if asset else ("Asset not found", 404)


# Policy endpoints
@connector_private_api_ns.route("policies")
class PolicyCollection(Resource):
    @connector_private_api_ns.doc("list_policies")
    def get(self):
        """List all policies"""
        return storage.list_policies()

    @connector_private_api_ns.doc("create_policy")
    @connector_private_api_ns.expect(policy_request_model)
    def post(self):
        """Create a new policy"""
        policy = storage.create_policy(request.json)
        return policy, 201


@connector_private_api_ns.route("policies/<string:id>")
class PolicyResource(Resource):
    @connector_private_api_ns.doc("get_policy")
    def get(self, id):
        """Get a policy by ID"""
        policy = storage.get_policy(id)
        return policy if policy else ("Policy not found", 404)


# Contract endpoints
@connector_private_api_ns.route("contractdefinitions")
class ContractCollection(Resource):
    @connector_private_api_ns.doc("list_contracts")
    def get(self):
        """List all contracts"""
        return storage.list_contracts()

    @connector_private_api_ns.doc("create_contract")
    @connector_private_api_ns.expect(contract_def_request_model)
    def post(self):
        """Create a new contract"""
        data = request.json

        # Validate asset and policies existence
        asset = storage.get_asset(data.get("assetId"))
        access_policy = storage.get_policy(data.get("accessPolicyId"))
        contract_policy = storage.get_policy(data.get("contractPolicyId"))

        if not asset:
            return {"message": "Asset not found"}, 404
        if not access_policy:
            return {"message": "Access policy not found"}, 404
        if not contract_policy:
            return {"message": "Contract policy not found"}, 404

        contract = storage.create_contract(data)
        return contract, 201


@connector_private_api_ns.route("contractdefinitions/<string:id>")
class ContractResource(Resource):
    @connector_private_api_ns.doc("get_contract")
    def get(self, id):
        """Get a contract by ID"""
        contract = storage.get_contract(id)
        return contract if contract else ("Contract not found", 404)


# Catalog endpoints
@connector_private_api_ns.route("catalog/request")
class CatalogResource(Resource):
    @connector_private_api_ns.doc("get_catalog")
    @connector_private_api_ns.expect(catalog_request_model)
    def post(self):
        """Get catalog items for a specific BPN"""
        data = request.json
        bpn = data.get("bpn")

        if not bpn:
            return {"message": "BPN is required"}, 400

        limit = data.get("limit", 10)
        offset = data.get("offset", 0)

        # Get catalog items
        items = storage.get_catalog_items(bpn, limit, offset)

        return {
            "items": items,
            "total": len(items),
            "limit": limit,
            "offset": offset,
        }, 200


# Negotiation endpoints
@connector_private_api_ns.route("contractnegotiations")
class ContractNegotiationCollection(Resource):
    @connector_private_api_ns.doc("initiate_negotiation")
    @connector_private_api_ns.expect(negotiation_request_model)
    def post(self):
        try:
            data = request.json
            negotiation = storage.create_negotiation(
                bpn=data.get("bpn"),
                catalog_item_id=data.get("catalog_item_id"),
                offer_details=data.get("offer_details"),
            )
            if negotiation["state"] == NegotiationState.DECLINED.value:
                return {
                    "message": "Negotiation declined",
                    "reason": negotiation.get("errorDetail", "BPN validation failed"),
                }, 403

            return negotiation, 201

        except NegotiationError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": f"Internal server error: {str(e)}"}, 500


@connector_private_api_ns.route("contractnegotiations/<string:id>")
class ContractNegotiationResource(Resource):
    @connector_private_api_ns.doc("get_negotiation")
    def get(self, negotiation_id):
        try:
            negotiation = storage.get_negotiation(negotiation_id)
            if not negotiation:
                return {"message": "Negotiation not found"}, 404
            return negotiation
        except Exception as e:
            return {"message": f"Error retrieving negotiation: {str(e)}"}, 500


@connector_private_api_ns.route("contractnegotiations/<string:id>/state")
class ContractNegotiationStateResource(Resource):
    @connector_private_api_ns.doc("update_negotiation_state")
    @connector_private_api_ns.expect(negotiation_state_model)
    def put(self, id):
        """Update the state of a contract negotiation"""
        try:
            data = request.json
            new_state = data.get("state")

            if not new_state:
                return {"message": "State is required"}, 400

            try:
                # Validate the state is a valid enum value
                new_state = NegotiationState(new_state).value
            except ValueError:
                return {
                    "message": f"Invalid state. Must be one of: {[state.value for state in NegotiationState]}"
                }, 400

            negotiation = storage.update_negotiation_state(id, new_state)
            return negotiation

        except NegotiationError as e:
            return {"message": str(e)}, 404
        except Exception as e:
            return {"message": f"Internal server error: {str(e)}"}, 500


# Data Transfer
# @connector_private_api_ns.route("transfers")
# class TransferCollection(Resource):
#     @connector_private_api_ns.doc("create_transfer")
#     @connector_private_api_ns.expect(transfer_request_model)
#     def post(self):
#         """Initiate a data transfer"""
#         try:
#             negotiation_id = request.json.get("negotiationId")
#             transfer = storage.create_transfer(negotiation_id)
#             return transfer, 201
#         except TransferError as e:
#             return {"message": str(e)}, 400
#         except Exception as e:
#             return {"message": "Internal server error"}, 500


# @connector_private_api_ns.route("transfers/<transfer_id>")
# class TransferResource(Resource):
#     @connector_private_api_ns.doc("get_transfer")
#     def get(self, transfer_id):
#         """Get transfer status"""
#         try:
#             transfer = storage.get_transfer(transfer_id)
#             return transfer
#         except TransferError as e:
#             return {"message": str(e)}, 404
#         except Exception as e:
#             return {"message": "Internal server error"}, 500
