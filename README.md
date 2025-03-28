# 🚀 BeeAI Framework Python Starter <img align="cener" alt="Project Status: Alpha" src="https://img.shields.io/badge/Status-Alpha-red">

[![Python library](https://img.shields.io/badge/Python-4584b6?style=flat&logo=python&logoColor=white)](https://github.com/i-am-bee/beeai-framework/tree/main/python)
[![Typescript library](https://img.shields.io/badge/TypeScript-3178c6?style=flat&logo=typescript&logoColor=white)](https://github.com/i-am-bee/beeai-framework/tree/main/typescript)
[![License](https://img.shields.io/badge/License-Apache%202.0-EA7826?style=flat)](https://github.com/i-am-bee/beeai-framework?tab=Apache-2.0-1-ov-file#readme)
[![Bluesky](https://img.shields.io/badge/Bluesky-0285FF?style=flat&logo=bluesky&logoColor=white)](https://bsky.app/profile/beeaiagents.bsky.social)
[![Discord](https://img.shields.io/discord/1309202615556378705?style=social&logo=discord&logoColor=black&label=Discord&labelColor=7289da&color=black)](https://discord.com/invite/NradeA6ZNF)
[![GitHub Repo stars](https://img.shields.io/github/stars/I-am-bee/beeai-framework)](https://github.com/i-am-bee/beeai-framework)

This starter template helps you **quickly** get started with the [BeeAI framework for Python](https://github.com/i-am-bee/beeai-framework/python)

---

## 🌟 Key Features

- 🔒 Safely execute an arbitrary Python Code via [BeeAI Code Interpreter](https://github.com/i-am-bee/beeai-code-interpreter).
- ⚡ Fully fledged Python project setup with linting and formatting.

---

## 📋 Requirements

- **Python 3.11+**
- **Poetry** for Python package management - See [installation guide](https://python-poetry.org/docs/#installation) 
- **Container system** (with Compose support):
    - [Docker](https://www.docker.com/)
    - [Rancher](https://www.rancher.com/) (For macOS, use VZ instead of QEMU)
    - [Podman](https://podman.io/) (Requires [Compose](https://podman-desktop.io/docs/compose/setting-up-compose) and rootful machine)
- **LLM Provider** - External [WatsonX](https://www.ibm.com/watsonx) (OpenAI, Groq, ...) or local [Ollama](https://ollama.com)
- **IDE/Code Editor** (e.g., WebStorm, VSCode) - Optional but recommended for smooth smooth configuration handling

---

## 🛠️ Installation

**Step one:** Clone this repository or [use it as a template](https://github.com/new?template_name=beeai-framework-py-starter&template_owner=i-am-bee)
```sh
git clone https://github.com/i-am-bee/beeai-framework-py-starter.git
cd beeai-framework-py-starter
```

**Step two:** Install dependencies
```sh
poetry install
```

**Step three:** Install and start the poetry environment
```sh
poetry self add poetry-plugin-shell && poetry shell
```

**Step four:** Configure your project by filling in missing values in the `.env` file.

> [!TIP] 
> To run the examples below, [Ollama](https://ollama.com/) must be installed and running, with the llama3.1 model pulled.

---

## 🤖 Agent example

Now that you’ve set up your project, let’s run the agent example located at `/beeai_framework_starter/agent.py`.

You have two options:

**Option 1:** Interactive mode
```sh
python beeai_framework_starter/agent.py
```

**Option 2:** Define your prompt up front
```sh
python beeai_framework_starter/agent.py <<< "I am going out tomorrow morning to walk around Boston. What should I plan to wear?"
```

> [!NOTE]
> Notice this prompts triggers the agent to call a tool.

---

## 🧑‍💻 Code interpreter agent example

Now let's run the code interpreter agent example located at `/beeai_framework_starter/agent_code_interpreter.py`.

> [!IMPORTANT]
> Start all services related to [beeai-code-interpreter](https://github.com/i-am-bee/beeai-code-interpreter) using `poe infra --type start`
> beeai-code-interpreter runs on `http://127.0.0.1:50081`.

Try the `Python Tool` and ask the agent to perform a complex calculation:
```sh
python beeai_framework_starter/agent_code_interpreter.py <<< "Calculate 534*342?"
```

Try the `SandBox tool` and run a custom Python function `get_riddle()`:
```sh
python beeai_framework_starter/agent_code_interpreter.py <<< "Generate a riddle"
```

---

## 🌐 Multi-agent workflow

This example demonstrates a **multi-agent workflow** where different agents work together to provide a comprehensive understanding of a location.

The workflow includes three agents:
1. **Researcher:** Gathers information about the location using the Wikipedia tool.
2. **WeatherForecaster:** Retrieves and reports weather details using the OpenMeteo API.
3. **DataSynthesizer:** Combines the historical and weather data into a final summary.

To run the workflow:
```sh
python beeai_framework_starter/agent_workflow.py
```

---

## 🎯 More examples

For additional examples to try, check out the examples directory of BeeAI framework for Python repository [here](https://github.com/i-am-bee/beeai-framework/blob/main/python/examples).
