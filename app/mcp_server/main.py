from fastmcp import FastMCP

from app.core.config import settings
from app.mcp_server.tools import register_all_tools

mcp = FastMCP(
    name="life-log-mcp",
    instructions="Tools for saving, querying, and analyzing workout and coffee logs.",
    version="0.1.0",
)
register_all_tools(mcp)


def main() -> None:
    mcp.run(
        transport="streamable-http",
        host=settings.MCP_HOST,
        port=settings.MCP_PORT,
    )


if __name__ == "__main__":
    main()
