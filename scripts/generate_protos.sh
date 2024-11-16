#!/bin/sh

# Create the generated code directory
mkdir -p wabee/rpc/protos

# Generate the gRPC code
python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    --pyi_out=. \
    wabee/rpc/protos/tool_service.proto