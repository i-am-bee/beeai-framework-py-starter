import asyncio

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool
from beeai_framework.tools.mcp import MCPTool
from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()


async def main() -> None:
    mcp_tools = await MCPTool.from_client(streamablehttp_client("https://remote.mcpservers.org/fetch/mcp"))

    agent = RequirementAgent(
        llm=ChatModel.from_name("ollama:granite3.3:8b"),
        tools=[*mcp_tools],
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool, ChatModel])],
    )

    prompt = "Fetch content of https://example.com"
    print(f"User: {prompt}")
    response = await agent.run(prompt)
    print(f"Agent: {response.last_message.text}")


if __name__ == "__main__":
    asyncio.run(main())
