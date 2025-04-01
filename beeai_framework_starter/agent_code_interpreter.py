import asyncio
import os
import sys
import traceback

from beeai_framework.agents import AgentExecutionConfig
from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import ChatModel
from beeai_framework.errors import FrameworkError
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.code import LocalPythonStorage, PythonTool, SandboxTool
from dotenv import load_dotenv

from beeai_framework_starter.helpers.io import ConsoleReader

load_dotenv()


async def main() -> None:
    code_interpreter_url = os.getenv("CODE_INTERPRETER_URL", "http://127.0.0.1:50081")

    dir_path = os.path.dirname(os.path.realpath(__file__))

    llm = ChatModel.from_name(os.getenv("LLM_CHAT_MODEL_NAME", "ollama:llama3.1"))

    python_tool = PythonTool(
        code_interpreter_url=code_interpreter_url,
        storage=LocalPythonStorage(
            local_working_dir=os.path.abspath(os.path.join(dir_path, "../tmp/code_interpreter_source")),
            interpreter_working_dir=os.path.abspath(os.path.join(dir_path, "../tmp/code_interpreter_target")),
        ),
    )

    sandbox_tool = await SandboxTool.from_source_code(
        url=code_interpreter_url,
        env={"API_URL": "https://riddles-api.vercel.app/random"},
        source_code="""
import requests
import os
from typing import Optional, Union, Dict

def get_riddle() -> Optional[Dict[str, str]]:
    '''
    Fetches a random riddle from the Riddles API.

    This function retrieves a random riddle and its answer. It does not accept any input parameters.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing:
            - 'riddle' (str): The riddle question.
            - 'answer' (str): The answer to the riddle.
        Returns None if the request fails.
    '''
    url = os.environ.get('API_URL')

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None
""",
    )

    agent = ReActAgent(llm=llm, tools=[python_tool, sandbox_tool], memory=UnconstrainedMemory())

    reader = ConsoleReader({"fallback": "Generate a random riddle."})

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
