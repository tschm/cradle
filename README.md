# cvxcradle

[![Apache 2.0 License](https://img.shields.io/badge/License-APACHEv2-brightgreen.svg)](https://github.com/cvxgrp/cradle/blob/master/LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/cvxgrp/cradle/badge.png?branch=main)](https://coveralls.io/github/cvxgrp/cradle?branch=main)

cradle is a command line tool to create repos based on a group of templates.

## Install gradle

We currently assume the reader is doing a clone of this repo via

```bash
git clone git@github.com:cvxgrp/cradle.git
```

### Install gh

Please install GitHub's official command line tool [gh](https://github.com/cli/cli).
This tool is used to create GitHub repos from the command line.

### Verify a working SSH GitHub connection

Try with

```bash
ssh -T git@github.com
```

or use

```bash
make verify
```

using the Makefile. A new SSH connection can be established [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

### Build the virtual environment

Creating the virtual environment also installs [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
make install
```

## Using the cradle tool

Cradle is a command-line utility that creates projects from templates.
It is similar to the popular
[Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/#) project.

You could create your own templates and standardize project structures
across your team or organization.
It's essentially a project scaffolding tool that helps maintain consistency
in Python projects.

## :warning: Private repositories

Using workflows in private repos will eat into your monthly GitHub bill.
You may want to restrict the workflow to operate only when merging on the main branch
while operating on a different branch or deactivate the flow.

We currently distinguish

* The document template
* The experiments template
* The package template

## Templates

We follow the one template, one repository policy.
You are encouraged to create your own templates and we give $3$ examples that
may serve as an inspiration

### [The document template](https://github.com/tschm/paper)

The template supports the fast creation of repositories of LaTeX documents.
Out of the box you get

* curated pre-commit-hooks (e.g. for spelling)
* github ci/cd workflows
* Makefile
* Example *.tex and bib file.

```bash
    create  paper
    create  paper/references.bib
    create  paper/{{ project_name }}.tex
    create  README.md
    create  .gitignore
    create  .github
    create  .github/workflows
    create  .github/workflows/latex.yml
    create  Makefile
```

When you run cradle, it prompts for these variables
and replaces them in filenames and file contents.

With every push into the repo the document is compiled
and published on a draft branch.

### [The experiments template](https://github.com/tschm/experiments)

Here we support the creation of notebooks without the ambition to release software.
The repo is not minimalistic but comes with a curated set of pre-commit hooks and
follows modern and established guidelines.

* uv support
* curated pre-commit-hooks
* DevContainer
* github ci/cd workflows
* Makefile
* marimo support

```bash
    create  requirements.txt
    create  .pre-commit-config.yaml
    create  README.md
    create  .devcontainer
    create  .devcontainer/startup.sh
    create  .devcontainer/devcontainer.json
    create  .gitignore
    create  .github
    create  .github/workflows
    create  .github/workflows/marimo.yml
    create  .github/dependabot.yml
    create  .python-version
    create  Makefile
    create  notebooks
    create  notebooks/minimal enclosing circle.py
    create  notebooks/{{ project_lower }}.py
```

### [The package template](https://github.com/tschm/package)

The package template is most useful when the final
goal is the real of software to a registry, e.g. pypi.
It features include

* uv support
* curated set of pre-commit hooks
* DevContainer
* Makefile
* github ci/cd workflows
* marimo support
* JupyterBook
* pdoc documentation

```bash
    create  uv.lock
    create  .pre-commit-config.yaml
    create  README.md
    create  .devcontainer
    create  .devcontainer/startup.sh
    create  .devcontainer/devcontainer.json
    create  Makefile
    create  .gitignore
    create  LICENSE.txt
    create  questions.yml
    create  .github
    create  .github/CONTRIBUTING.md
    create  .github/workflows
    create  .github/workflows/release.yml
    create  .github/workflows/pre-commit.yml
    create  .github/workflows/book.yml
    create  .github/workflows/ci.yml
    create  .github/CODE_OF_CONDUCT.md
    create  .github/dependabot.yml
    create  book
    create  book/docs
    create  book/docs/api.md
    create  book/docs/reports.md
    create  book/docs/index.md
    create  book/docs/marimo.md
    create  book/_config.yml
    create  book/_toc.yml
    create  book/marimo
    create  book/marimo/demo.py
    create  pyproject.toml
    create  .env
    create  src
    create  src/tests
    create  src/tests/conftest.py
    create  src/tests/test_trivial.py
    create  src/tests/resources
    create  src/tests/resources/.gitkeep
    create  src/tests/__init__.py
    create  src/{{ project_name }}
    create  src/{{ project_name }}/add.py
    create  src/{{ project_name }}/__init__.py

```
