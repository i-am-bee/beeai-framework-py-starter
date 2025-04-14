import asyncio
import os
import sys
import traceback

from beeai_framework.agents.tool_calling import ToolCallingAgent, ToolCallingAgentSuccessEvent
from beeai_framework.backend import ChatModel
from beeai_framework.emitter import EventMeta
from beeai_framework.errors import FrameworkError
from beeai_framework.memory import TokenMemory
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.weather import OpenMeteoTool
from dotenv import load_dotenv

from beeai_framework_starter.helpers.io import ConsoleReader

load_dotenv()


async def main() -> None:
    llm = ChatModel.from_name(os.getenv("LLM_CHAT_MODEL_NAME", "ollama:llama3.1"))
    agent = ToolCallingAgent(llm=llm, tools=[DuckDuckGoSearchTool(), OpenMeteoTool()], memory=TokenMemory(llm))

    reader = ConsoleReader({"fallback": "What is the current weather in Las Vegas?"})

    def on_success(data: ToolCallingAgentSuccessEvent, event: EventMeta) -> None:
        reader.write("Agent 🤖(update) : ", str(data.state.memory.messages[-1].to_plain()))

    for prompt in reader:
        response = await agent.run(prompt).on("success", on_success)
        reader.write("Agent 🤖 : ", response.result.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
