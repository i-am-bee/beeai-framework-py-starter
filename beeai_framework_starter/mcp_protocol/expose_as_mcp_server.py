import asyncio
import os
import sys
import time
import traceback
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

from beeai_framework.adapters.mcp import MCPServer, MCPServerConfig
from beeai_framework.adapters.mcp.serve.server import MCPSettings
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool
from beeai_framework.tools.mcp import MCPTool
from beeai_framework.tools.weather import OpenMeteoTool
from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()


def mcp_server() -> None:
    agent = RequirementAgent(
        llm=ChatModel.from_name("ollama:granite3.3:8b"),
        tools=[OpenMeteoTool()],
        role="Weather Specialist",
        instructions="Use a weather tool only if the user gives you a concrete location.",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
    )

    server = MCPServer(config=MCPServerConfig(transport="streamable-http", settings=MCPSettings(port=7777)))
    server.register_many([agent])
    server.serve()

    # Run npx -y @modelcontextprotocol/inspector
    # Visit: http://127.0.0.1:7777/mcp


async def mcp_client() -> None:
    [agent_tool] = await MCPTool.from_client(streamablehttp_client("http://127.0.0.1:7777/mcp"))
    prompt = "What's the current weather in Berlin?"
    print(f"User: {prompt}")
    response = await agent_tool.run({"input": prompt})
    print(f"Agent: {response.get_text_content()}")


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as pool:
        try:
            f1 = pool.submit(mcp_server)
            time.sleep(3)  # wait for the server to start
            f2 = pool.submit(asyncio.run, mcp_client())

            done, _ = wait([f1, f2], return_when=FIRST_COMPLETED)
            for f in done:
                if f.exception():
                    raise f.exception()
        except Exception as e:
            traceback.print_exc()
            sys.exit(str(e))
        finally:
            os.kill(os.getpid(), 9)
