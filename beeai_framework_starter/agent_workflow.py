import asyncio
import os
import sys
import traceback

from beeai_framework.backend import ChatModel
from beeai_framework.errors import FrameworkError
from beeai_framework.tools.search import WikipediaTool
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.workflows.agent import AgentWorkflow, AgentWorkflowInput
from dotenv import load_dotenv

from beeai_framework_starter.helpers.io import ConsoleReader

load_dotenv()


async def main() -> None:
    llm = ChatModel.from_name(os.getenv("LLM_CHAT_MODEL_NAME", "ollama:llama3.1"))
    workflow = AgentWorkflow(name="Smart assistant")

    workflow.add_agent(
        name="Researcher",
        role="A diligent researcher.",
        instructions="You look up and provide information about a specific topic.",
        tools=[WikipediaTool()],
        llm=llm,
    )

    workflow.add_agent(
        name="WeatherForecaster",
        role="A weather reporter.",
        instructions="You provide detailed weather reports.",
        tools=[OpenMeteoTool()],
        llm=llm,
    )

    workflow.add_agent(
        name="DataSynthesizer",
        role="A meticulous and creative data synthesizer",
        instructions="You can combine disparate information into a final coherent summary.",
        llm=llm,
    )

    reader = ConsoleReader()

    reader.write("Assistant 🤖 : ", "What location do you want to learn about?")
    for prompt in reader:
        await workflow.run(
            inputs=[
                AgentWorkflowInput(prompt="Provide a short history of the location.", context=prompt),
                AgentWorkflowInput(
                    prompt="Provide a comprehensive weather summary for the location today.",
                    expected_output="Essential weather details such as chance of rain, temperature and wind. Only report information that is available.",  # noqa: E501
                ),
                AgentWorkflowInput(
                    prompt="Summarize the historical and weather data for the location.",
                    expected_output="A paragraph that describes the history of the location, followed by the current weather conditions.",  # noqa: E501
                ),
            ]
        ).on(
            "success",
            lambda data, event: reader.write(
                f"-> Step '{data.step}' has been completed with the following outcome:\n",
                data.state.final_answer,
            ),
        )
        reader.write("Assistant 🤖 : ", "What location do you want to learn about?")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
