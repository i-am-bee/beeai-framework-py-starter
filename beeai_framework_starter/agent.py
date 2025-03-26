import asyncio
import os
import sys
import traceback

from beeai_framework import ReActAgent, TokenMemory
from beeai_framework.agents import AgentExecutionConfig
from beeai_framework.backend.chat import ChatModel
from beeai_framework.errors import FrameworkError
from beeai_framework.tools.search import DuckDuckGoSearchTool
from beeai_framework.tools.weather.openmeteo import OpenMeteoTool
from dotenv import load_dotenv

from beeai_framework_starter.helpers.io import ConsoleReader

load_dotenv()


async def main() -> None:
    llm = ChatModel.from_name(os.getenv("LLM_CHAT_MODEL_NAME", "ollama:llama3.1"))
    agent = ReActAgent(llm=llm, tools=[DuckDuckGoSearchTool(), OpenMeteoTool()], memory=TokenMemory(llm))

    reader = ConsoleReader({"fallback": "What is the current weather in Las Vegas?"})

    for prompt in reader:
        response = await agent.run(
            prompt, execution=AgentExecutionConfig(max_iterations=8, max_retries_per_step=3, total_max_retries=10)
        ).on("update", lambda data, event: reader.write(f"Agent 🤖 ({data.update.key}) : ", data.update.parsed_value))

        reader.write("Agent 🤖 : ", response.result.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
