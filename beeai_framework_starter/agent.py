import asyncio
import os
import sys
import traceback

from beeai_framework.agents import AgentExecutionConfig
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.backend import ChatModel
from beeai_framework.errors import FrameworkError
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.tools.tool import Tool
from beeai_framework.tools.weather import OpenMeteoTool
from dotenv import load_dotenv

from beeai_framework_starter.helpers.io import ConsoleReader

load_dotenv()


async def main() -> None:
    agent = RequirementAgent(
        llm=ChatModel.from_name(os.getenv("LLM_CHAT_MODEL_NAME", "ollama:granite3.3")),
        tools=[ThinkTool(), OpenMeteoTool(), DuckDuckGoSearchTool()],
        instructions="Plan activities for a given destination based on current weather and events.",
        requirements=[
            ConditionalRequirement(ThinkTool, force_at_step=1, max_invocations=3),
            ConditionalRequirement(
                DuckDuckGoSearchTool, only_after=[OpenMeteoTool], min_invocations=1, max_invocations=2
            ),
        ],
        # Log intermediate steps to the console
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
    )

    reader = ConsoleReader({"fallback": "What to do in Boston?"})

    for prompt in reader:
        response = await agent.run(
            prompt, execution=AgentExecutionConfig(max_iterations=8, max_retries_per_step=3, total_max_retries=10)
        )

        reader.write("Agent 🤖 : ", response.result.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
