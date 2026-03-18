from fastmcp import FastMCP

from app.mcp_server.tools import register_all_tools

mcp = FastMCP(
    name="life-log-mcp",
    instructions="Tools for saving, querying, and analyzing workout and coffee logs.",
    version="0.1.0",
)
register_all_tools(mcp)


def main() -> None:
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8767)


if __name__ == "__main__":
    main()
