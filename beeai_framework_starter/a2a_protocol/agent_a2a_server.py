from beeai_framework.adapters.a2a import A2AServer, A2AServerConfig
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.serve.utils import LRUMemoryManager
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.weather import OpenMeteoTool
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    agent = RequirementAgent(
        llm=ChatModel.from_name("ollama:granite3.3:8b"),
        tools=[DuckDuckGoSearchTool(), OpenMeteoTool()],
        memory=UnconstrainedMemory(),
        middlewares=[GlobalTrajectoryMiddleware(included=[ChatModel])],
    )

    server = A2AServer(
        config=A2AServerConfig(port=9999, protocol="jsonrpc"), memory_manager=LRUMemoryManager(maxsize=100)
    )
    server.register(agent)
    server.serve()


if __name__ == "__main__":
    main()
