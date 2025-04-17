import asyncio
import os
import sys
import traceback

from beeai_framework.agents import AgentExecutionConfig
from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import ChatModel
from beeai_framework.errors import FrameworkError
from beeai_framework.memory import TokenMemory
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.weather import OpenMeteoTool
from dotenv import load_dotenv

from beeai_framework_starter.helpers.instrumentation import setup_observability

setup_observability()

load_dotenv()


async def main() -> None:
    llm = ChatModel.from_name(os.getenv("LLM_CHAT_MODEL_NAME", "ollama:llama3.1"))
    agent = ReActAgent(llm=llm, tools=[DuckDuckGoSearchTool(), OpenMeteoTool()], memory=TokenMemory(llm))

    prompt = "What is the current weather in Las Vegas?"

    response = await agent.run(
        prompt, execution=AgentExecutionConfig(max_iterations=8, max_retries_per_step=3, total_max_retries=10)
    )

    print("Agent 🤖 : ", response.result.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
