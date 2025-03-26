# 🐝 BeeAI Framework Python Starter

This starter template lets you quickly start working with the [BeeAI Framework](https://github.com/i-am-bee/beeai-framework) in a second.

📚 See the [documentation](https://i-am-bee.github.io/beeai-framework/) to learn more.

## ✨ Key Features

- 🔒 Safely execute an arbitrary Python Code via [Bee Code Interpreter](https://github.com/i-am-bee/bee-code-interpreter).
- 🚀 Fully fledged Python project setup with linting and formatting.

## 📦 Requirements

- Python version 3.11 or higher
- Poetry, a tool for Python package management. Installation steps can be found [here](https://python-poetry.org/docs/#installation) 
- Container system like [Rancher Desktop](https://rancherdesktop.io/), [Podman](https://podman.io/) (VM must be rootfull machine) or [Docker](https://www.docker.com/).
- LLM Provider either external [WatsonX](https://www.ibm.com/watsonx) (OpenAI, Groq, ...) or local [ollama](https://ollama.com).

## 🛠️ Getting started

1. Clone this repository or [use it as a template](https://github.com/new?template_name=beeai-framework-py-starter&template_owner=i-am-bee).
2. Install dependencies `poetry install`.
3. Install and start the poetry environment `poetry self add poetry-plugin-shell` and `poetry shell`
4. Configure your project by filling in missing values in the `.env` file (default LLM provider is locally hosted `Ollama`).
5. Run the agent `python beeai_framework_starter/agent.py`

To run an agent with a custom prompt, simply do this `python beeai_framework_starter/agent.py <<< 'Hello Bee!'`

🧪 More examples can be found [here](https://github.com/i-am-bee/beeai-framework/blob/main/python/examples).

> [!TIP]
>
> To use Bee agent with [Python Code Interpreter](https://github.com/i-am-bee/bee-code-interpreter) refer to the [Code Interpreter](#code-interpreter) section.

## 🏗 Infrastructure

> [!NOTE]
>
> Docker distribution with support for _compose_ is required, the following are supported:
>
> - [Docker](https://www.docker.com/)
> - [Rancher](https://www.rancher.com/) - macOS users may want to use VZ instead of QEMU
> - [Podman](https://podman.io/) - requires [compose](https://podman-desktop.io/docs/compose/setting-up-compose) and **rootful machine** (if your current machine is rootless, please create a new one, also ensure you have enabled Docker compatibility mode).

## 🔒Code interpreter

The [Bee Code Interpreter](https://github.com/i-am-bee/bee-code-interpreter) is a gRPC service that an agent uses to execute an arbitrary Python code safely.

### Instructions

1. Start all services related to the [`Code Interpreter`](https://github.com/i-am-bee/bee-code-interpreter) `poe infra --type start`
2. Run the agent `python beeai_framework_starter/agent_code_interpreter.py`

> [!NOTE]
>
> Code Interpreter runs on `http://127.0.0.1:50081`.
