# Development

This git repository is provided to help you get started using BeeAI Framework.

## Setting up git hooks 

This is recommended if you are either:

* developing this template.
* basing a project on top of this template and want to adopt some of the best practices and tools used by the BeeAI team.

Run 
```
.githooks/install.sh
```
to setup additional code checks


## Background

The [README](README.md) aims to provide a quick start guide to get your project working.

However, the repository has also been setup following some of the development practices adopted by the BeeAI project which
include tools to make the development process easier and more efficient. These include the definition of tasks for
checking and testing code.

These are based on the definitions used in the  [BeeAI Framework repository](https://github.com/beeai-framework/beeai_framework). That repositories [python/CONTRIBUTING.md](https://github.com/i-am-bee/beeai-framework/blob/main/python/CONTRIBUTING.md) provides a more detailed guide to contributing to that project.

Similar tooling is provided in this repository with the following differences:

* This is not a monorepo, so some of the complexity of managing a mix of code in Python and Typescript does not apply
* The `commitizen` plugin is not used
* no copyright check is included


With the githooks installed the following will run automatically on a commit:

* [ruff](https://github.com/astral-sh/ruff) is used to lint and format your code
* [mypy](https://github.com/python/mypy) is used to check for type errors
* a simple format check is applied to the commit message to verify for use of conventional commits

Additional tools are integrated into poetry via the https://poethepoet.natn.io/poetry_plugin.html plugin

Tools can also be run directly via the command line (run within `poetry shell` or prefix with `poetry run`):

* `poe lint` - lints and formats your code
* `poe format` - formats your code
* `poe type-check` - checks for type errors in your code