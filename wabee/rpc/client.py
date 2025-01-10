import json
import grpc
from typing import Any, Optional, Dict, Union

from wabee.tools.base_model import StructuredToolResponse
from wabee.rpc.protos import tool_service_pb2
from wabee.rpc.protos import tool_service_pb2_grpc

class ToolServiceClient:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 50051,
        use_json: bool = True
    ):
        self.host = host
        self.port = port
        self.use_json = use_json
        self.channel = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
        self.stub = tool_service_pb2_grpc.ToolServiceStub(self.channel)
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        self.channel = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
        self.stub = tool_service_pb2_grpc.ToolServiceStub(self.channel)
        self.use_json = self.use_json

    async def get_tool_schema(
        self,
        tool_name: str
    ) -> Dict[str, Any]:
        """Get the schema for a specific tool"""
        request = tool_service_pb2.GetToolSchemaRequest(
            tool_name=tool_name
        )
        
        try:
            response = await self.stub.GetToolSchema(request)
            return {
                "tool_name": response.tool_name,
                "fields": [
                    {
                        "name": field.name,
                        "type": field.type,
                        "required": field.required,
                        "description": field.description
                    }
                    for field in response.fields
                ]
            }
        except grpc.RpcError as e:
            return {"error": str(e)}

    async def execute(
        self,
        tool_name: str,
        input_data: Dict[str, Any]
    ) -> tuple[Optional[StructuredToolResponse], Optional[Dict]]:
        """Execute a tool with the given input data"""
        try:
            request = tool_service_pb2.ExecuteRequest(
                tool_name=tool_name
            )
            
            if self.use_json:
                request.json_data = json.dumps(input_data)
            else:
                request.proto_data = json.dumps(input_data).encode()
            
            response = await self.stub.Execute(request)
            
            if response.HasField('error'):
                return None, {
                    'type': response.error.type,
                    'message': response.error.message
                }
            
            if response.HasField('json_result'):
                result_dict = json.loads(response.json_result), None
            else:
                result_dict = json.loads(response.proto_result.decode()), None
            
            return StructuredToolResponse(**result_dict), None
            
        except grpc.RpcError as e:
            return None, {
                'type': 'RPC_ERROR',
                'message': str(e)
            }

    async def close(self):
        await self.channel.close()

async def execute_tool(
    tool_name: str,
    input_data: Dict[str, Any],
    host: str = "localhost",
    port: int = 50051
) -> Union[Any, Dict[str, str]]:
    """Convenience function for one-off tool execution"""
    async with ToolServiceClient(host, port) as client:
        result, error = await client.execute(tool_name, input_data)
        if error:
            return error
        return result
