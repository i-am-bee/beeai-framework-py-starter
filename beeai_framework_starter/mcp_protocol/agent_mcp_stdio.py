import asyncio
from pathlib import Path

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool
from beeai_framework.tools.mcp import MCPTool
from dotenv import load_dotenv
from mcp import StdioServerParameters, stdio_client

load_dotenv()


async def main() -> None:
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="uvx",
        args=["mcp-server-git"],
        cwd=Path(__file__).parent.parent.parent.resolve(),  # get project root
    )

    mcp_tools = await MCPTool.from_client(stdio_client(server_params))
    agent = RequirementAgent(
        llm=ChatModel.from_name("ollama:granite3.3:8b"),
        tools=[*mcp_tools],
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
    )

    prompt = "What's the last commit message? Use git_status tool."
    print(f"User: {prompt}")
    response = await agent.run(prompt)
    print(f"Agent: {response.last_message.text}")


if __name__ == "__main__":
    asyncio.run(main())
