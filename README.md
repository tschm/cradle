# 🚀 qCradle

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/qCradle.svg)](https://badge.fury.io/py/qCradle)
[![Coverage Status](https://coveralls.io/repos/github/tschm/cradle/badge.png?branch=main)](https://coveralls.io/github/tschm/cradle?branch=main)
[![ci](https://github.com/tschm/cradle/actions/workflows/ci.yml/badge.svg)](https://github.com/tschm/cradle/actions/workflows/ci.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/tschm/cradle/badge)](https://www.codefactor.io/repository/github/tschm/cradle)
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/renovatebot/renovate)

🛠️ qcradle is a command line tool to create repos based on a group of templates.
It has been created
to speed up, simplify, and to harmonize the development
of experiments and quantitative strategies.

Assuming the presence of uvx
you can start the tool with

```bash
uvx qcradle
```

![Creating a repository from the command line](https://raw.githubusercontent.com/tschm/cradle/main/demo.png)

**qcradle** is a tool inspired by [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/#),
but more biased towards quants, researchers, and academics.

Whether you're building entire Python packages or financial models,
running simulations, or writing academic papers,
qcradle helps you hit the ground running with a structured
and efficient setup following the most recent standards set in 2025.

We use [uv](https://github.com/astral-sh/uv), [hatch](https://hatch.pypa.io/),
[marimo](https://marimo.io/) and [Tectonic](https://tectonic-typesetting.github.io/).
We support
[Renovate](https://github.com/renovatebot/renovate) and
take full advantage of [GitHub Workflows](https://docs.github.com/en/actions/using-workflows/about-workflows).

Each template comes with curated [pre-commit hooks](https://pre-commit.com/).
We collect test reports, API documentation, and notebooks.

Let’s make project setup as rigorous as your research!

## 📚 Examples

Users can interact with qcradle by either creating templates or
by using existing templates to create projects. We would be
delighted to list your public work here:

### 🏆 User projects

We would like to encourage our users to point to public repositories
created with the qcradle. We start with

* [cvxball](https://github.com/cvxgrp/cvxball). We created badges
  for you

### 🧩 User templates

Please share your templates with the world!

## 🔄 Install uv and uvx

🚀 uv is a modern, high-performance Python package manager and installer
written in Rust.
It serves as a drop-in replacement for traditional tools like pip and pipx.
For macOS and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows follow the [official instructions](https://docs.astral.sh/uv/getting-started/installation/)

## 🧠 Understanding uvx

🔍 uvx is a command provided by uv to run tools published as Python packages
without installing them permanently. It creates temporary,
isolated environments for these tools:

```bash
uvx qcradle
```

This command will:

* Resolve and install the qcradle package in a temporary environment.
* Execute the qcradle command.

**Note**: If you plan to use a tool frequently, consider installing
it permanently using uv:

```bash
uv tool install qcradle
````

Once the tool is permanently installed it is enough to start it with

```bash
qcradle
```

## 📝 Templates

✨ You could create your own templates and standardize project structures
across your team or organization.
It's essentially a project scaffolding tool that helps maintain consistency
in Python projects.

We currently offer $3$ standard templates out of the box

* 📄 The document template
* 🧪 The experiments template
* 📦 The package template

### 🌟 Standard Templates

We follow the one template, one repository policy.
You are encouraged to create your own templates and we give $4$ examples that
may serve as inspiration

#### 📄 [The document template](https://github.com/tschm/paper)

The template supports the fast creation of repositories of LaTeX documents.
The repo can compile your LaTeX documents with every commit and put them
on a dedicated branch.

#### 🧪 [The experiments template](https://github.com/tschm/experiments)

Here we support the creation of notebooks without the ambition to release software.
The repo is not minimalistic but comes with a curated set of pre-commit hooks and
follows modern and established guidelines. The notebooks are based on Marimo.

#### 📦 [The package template](https://github.com/tschm/package)

The package template is most useful when the final
goal is the release of software to a registry, e.g. pypi.
It offers full uv support and compiles documentation
into a Jupyter Book.

### 🔒 Proprietary templates

#### 🛠️ Creation

You can create your very own templates and we recommend to start with
forking the
[dedicated repo](https://github.com/tschm/template/blob/main/README.md)
for the job.

Templates rely on [Jinja](https://jinja.palletsprojects.com/en/stable/).
At the root level the repo needs a 'copier.yml' file and a 'template' folder.

#### 🚀 Usage

We essentially expose the copier interface directly with
minor modifications, e.g. if the user is not submitting a source template
we offer to choose one of the standard templates.

Any cradle template could be used directly as the first 'template'
argument

```bash
uvx qcradle --template=git@github.com:tschm/paper.git
```

By default, Copier (and hence the cradle) will copy from the last
release found in template Git tags, sorted as
[PEP 440](https://peps.python.org/pep-0440/).

### 🔄 Update existing projects

Templates are moving targets in most professional setups. It is possible to update
projects created with the help of the qcradle by specifying an existing path
instead of a template.

```bash
uvx qcradle --dst_path=/Users/thomasschmelzer/projects/my_marimo_experiments
```

The tool expects a full path. Your repo should contain your previous answers
in a file '.copier-answers.yml' which serve as default arguments for the
questions you have been asked before. All standard templates create the file.

## 🔄 GitHub Actions

⚙️ This repository provides a collection of reusable
GitHub Actions that can be used by other repositories.
These actions are defined in the `actions` directory and
can be referenced in your workflows.

### 🛠️ Available Actions

* 📚 **book**: Builds and publishes a Jupyter Book
* 📦 **build**: Builds a Python package and uploads artifacts
* 📊 **coverage**: Generates and uploads code coverage reports
* 🔍 **deptry**: Checks for dependency issues using deptry
* 🐳 **docker**: Builds and pushes Docker images
* 🔧 **environment**: Sets up Python environment with dependencies
* 📄 **latex**: Compiles LaTeX documents
* 📝 **pdoc**: Generates API documentation using pdoc
* ✅ **pre-commit**: Runs pre-commit hooks
* 🏷️ **tag**: Bumps version, creates a tag, and publishes a release
* 🧪 **test**: Runs tests with pytest

### 📋 How to Use These Actions

You can use these actions in your GitHub workflows
by referencing them with the `uses` keyword. For example:

```yaml
jobs:
  tag:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Generate Tag
        uses: tschm/cradle/actions/tag@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

Each action has its own inputs and outputs defined in
its `action.yml` file. You can find more details by
examining these files in the repository.

## :warning: Private repositories

Using workflows in private repos will eat into your monthly GitHub bill.
You may want to restrict the workflow to operate only when merging on the main branch
while operating on a different branch or deactivate the flow.
