from mcp import Client
from app.mcp.server import mcp
async def call_mcp_tool(name:str, arguments:dict)->dict:
    async with Client(mcp,raise_exceptions=True) as client:
        result=await client.call_tool(name,arguments)
        if result.structured_content:return result.structured_content
        texts=[getattr(x,"text","") for x in result.content if getattr(x,"type",None)=="text"]
        return {"result":"\n".join(texts)}
async def list_mcp_tools()->list[str]:
    async with Client(mcp,raise_exceptions=True) as client:
        page=await client.list_tools()
        return [t.name for t in page.tools]
