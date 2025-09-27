import asyncio
import sys
import traceback
from typing import Any

from beeai_framework.adapters.a2a.agents import A2AAgent
from beeai_framework.backend import UserMessage
from beeai_framework.emitter import EventMeta
from beeai_framework.errors import FrameworkError
from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory


async def main() -> None:
    agent = A2AAgent(url="http://127.0.0.1:9999", memory=UnconstrainedMemory())

    @agent.emitter.on("update")
    def log_update(data: Any, meta: EventMeta) -> None:
        print("Agent 🤖 (debug) : ", data)

    prompt = UserMessage("What's the current weather in Berlin?")
    print("User: ", prompt)
    response = await agent.run(prompt)
    print("Agent: ", response.last_message.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
