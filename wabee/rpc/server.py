import json
import asyncio
import grpc
from typing import Dict, Any, Optional
from concurrent import futures

from wabee.tools.base_tool import BaseTool
from wabee.tools.tool_error import ToolError
from wabee.rpc.schema import ProtoSchemaGenerator

from wabee.rpc.protos import tool_service_pb2
from wabee.rpc.protos import tool_service_pb2_grpc

class ToolServicer(tool_service_pb2_grpc.ToolServiceServicer):
    def __init__(self, tools: Dict[str, BaseTool | Any]):
        self.tools = tools
        self.schema_generator = ProtoSchemaGenerator()

    async def GetToolSchema(
        self,
        request: tool_service_pb2.GetToolSchemaRequest,
        context: grpc.aio.ServicerContext
    ) -> tool_service_pb2.ToolSchema:
        tool_name = request.tool_name
        if tool_name not in self.tools:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Tool '{tool_name}' not found")
            return tool_service_pb2.ToolSchema()

        tool = self.tools[tool_name]
        schema = self.schema_generator.get_tool_schema(tool)
        
        response = tool_service_pb2.ToolSchema(
            tool_name=tool_name
        )
        
        for name, details in schema.get("properties", {}).items():
            field = response.fields.add()
            field.name = name
            field.type = details.get("type", "string")
            field.required = name in schema.get("required", [])
            field.description = details.get("description", "")
            
        return response

    async def _execute_tool(
        self,
        tool: BaseTool | Any,
        input_data: Dict[str, Any]
    ) -> tuple[Any, Optional[ToolError]]:
        try:
            if isinstance(tool, type):  # For simple_tool decorated functions
                return await tool(**input_data)
            else:  # For BaseTool instances
                return await tool(input_data)
        except Exception as e:
            return None, ToolError(
                type="INTERNAL_ERROR",
                message=f"Execution failed: {str(e)}"
            )

    async def Execute(
        self,
        request: tool_service_pb2.ExecuteRequest,
        context: grpc.aio.ServicerContext
    ) -> tool_service_pb2.ExecuteResponse:
        tool_name = request.tool_name
        
        if tool_name not in self.tools:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Tool '{tool_name}' not found")
            return tool_service_pb2.ExecuteResponse()

        # Handle both JSON and proto inputs
        input_case = request.WhichOneof('input')
        if input_case == 'json_data':
            try:
                input_data = json.loads(request.json_data)
            except json.JSONDecodeError:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid JSON input")
                return tool_service_pb2.ExecuteResponse()
        else:  # proto_data
            try:
                # Deserialize the dynamic proto message
                input_data = json.loads(request.proto_data.decode())
            except Exception as e:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(f"Invalid proto input: {str(e)}")
                return tool_service_pb2.ExecuteResponse()

        tool = self.tools[tool_name]
        result, error = await self._execute_tool(tool, input_data)
        
        response = tool_service_pb2.ExecuteResponse()
        
        if error:
            response.error.type = error.type
            response.error.message = error.message
        else:
            # Use same format as request
            if input_case == 'json_data':
                response.json_result = json.dumps(result)
            else:
                response.proto_result = json.dumps(result).encode()
                
        return response

async def serve(
    tools: Dict[str, BaseTool | Any],
    port: int = 50051,
    max_workers: int = 10
) -> None:
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=max_workers)
    )
    tool_service_pb2_grpc.add_ToolServiceServicer_to_server(
        ToolServicer(tools), server
    )
    server.add_insecure_port(f'[::]:{port}')
    
    print(f"Starting gRPC server on port {port}")
    await server.start()
    await server.wait_for_termination()
