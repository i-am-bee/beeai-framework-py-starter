import asyncio

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool
from beeai_framework.tools.mcp import MCPTool
from beeai_framework.utils.strings import to_json
from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from pydantic import BaseModel

load_dotenv()


async def main() -> None:
    #mcp_tools = await MCPTool.from_client(streamablehttp_client("https://remote.mcpservers.org/fetch/mcp"))  # type: ignore
    mcp_tools = await MCPTool.from_client(streamablehttp_client("https://mcp.kiwi.com"))  # type: ignore

    schema: type[BaseModel] = mcp_tools[0].input_schema
    print(schema.model_validate({
        "departureDate": "02/10/2024",
        "departureDateFlexRange": 3,
        "flyFrom": "Paris",
        "flyTo": "Lisbon",
        "returnDate": "09/10/2024",
        "returnDateFlexRange": 3
    }))
    #print(to_json(schema.model_json_schema(), sort_keys=False, indent=4))
    #agent = RequirementAgent(
    #    llm=ChatModel.from_name("watsonx:meta-llama/llama-3-3-70b-instruct"),
    #    tools=[*mcp_tools],
    #    middlewares=[GlobalTrajectoryMiddleware(included=[Tool, ChatModel])],
    #)
    #prompt = "Fetch content of https://example.com"
    #print(f"User: {prompt}")
    #response = await agent.run(prompt)
    #print(f"Agent: {response.last_message.text}")


if __name__ == "__main__":
    asyncio.run(main())
