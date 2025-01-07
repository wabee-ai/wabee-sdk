import asyncio
import os
import logging
from pathlib import Path
from wabee.rpc.server import serve
from wabee.rpc.loader import ToolLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    try:
        port = int(os.environ.get('WABEE_GRPC_PORT', '50051'))
        tool = ToolLoader.load_from_spec(Path("toolspec.yaml"))
        logger.info(f"Starting gRPC server on port {port}")
        asyncio.run(serve({tool.tool_name: tool}, port=port))
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == '__main__':
    main()
