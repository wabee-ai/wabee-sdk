# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from wabee.rpc.protos import tool_service_pb2 as wabee_dot_rpc_dot_protos_dot_tool__service__pb2

GRPC_GENERATED_VERSION = '1.69.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in wabee/rpc/protos/tool_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ToolServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Execute = channel.unary_unary(
                '/wabee.tools.ToolService/Execute',
                request_serializer=wabee_dot_rpc_dot_protos_dot_tool__service__pb2.ExecuteRequest.SerializeToString,
                response_deserializer=wabee_dot_rpc_dot_protos_dot_tool__service__pb2.ExecuteResponse.FromString,
                _registered_method=True)
        self.GetToolSchema = channel.unary_unary(
                '/wabee.tools.ToolService/GetToolSchema',
                request_serializer=wabee_dot_rpc_dot_protos_dot_tool__service__pb2.GetToolSchemaRequest.SerializeToString,
                response_deserializer=wabee_dot_rpc_dot_protos_dot_tool__service__pb2.ToolSchema.FromString,
                _registered_method=True)


class ToolServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Execute(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetToolSchema(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ToolServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Execute': grpc.unary_unary_rpc_method_handler(
                    servicer.Execute,
                    request_deserializer=wabee_dot_rpc_dot_protos_dot_tool__service__pb2.ExecuteRequest.FromString,
                    response_serializer=wabee_dot_rpc_dot_protos_dot_tool__service__pb2.ExecuteResponse.SerializeToString,
            ),
            'GetToolSchema': grpc.unary_unary_rpc_method_handler(
                    servicer.GetToolSchema,
                    request_deserializer=wabee_dot_rpc_dot_protos_dot_tool__service__pb2.GetToolSchemaRequest.FromString,
                    response_serializer=wabee_dot_rpc_dot_protos_dot_tool__service__pb2.ToolSchema.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'wabee.tools.ToolService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('wabee.tools.ToolService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ToolService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Execute(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/wabee.tools.ToolService/Execute',
            wabee_dot_rpc_dot_protos_dot_tool__service__pb2.ExecuteRequest.SerializeToString,
            wabee_dot_rpc_dot_protos_dot_tool__service__pb2.ExecuteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetToolSchema(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/wabee.tools.ToolService/GetToolSchema',
            wabee_dot_rpc_dot_protos_dot_tool__service__pb2.GetToolSchemaRequest.SerializeToString,
            wabee_dot_rpc_dot_protos_dot_tool__service__pb2.ToolSchema.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
