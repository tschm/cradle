# cvxcradle

[![Apache 2.0 License](https://img.shields.io/badge/License-APACHEv2-brightgreen.svg)](https://github.com/cvxgrp/cradle/blob/master/LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/cvxgrp/cradle/badge.png?branch=main)](https://coveralls.io/github/cvxgrp/cradle?branch=main)

cradle is a command line tool to create repos based on a group of templates.

![Creating a repository from the command line](demo.png)

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
make verify
```

A new SSH connection could be established [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

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

We currently offer $3$ templates out of the box

- The document template
- The experiments template
- The package template

## Templates

We follow the one template, one repository policy.
You are encouraged to create your own templates and we give $3$ examples that
may serve as an inspiration

### [The document template](https://github.com/tschm/paper)

The template supports the fast creation of repositories of LaTeX documents.
Out of the box you get

- curated pre-commit-hooks (e.g. for spelling)
- github ci/cd workflows
- Makefile
- Example *.tex and bib file.

### [The experiments template](https://github.com/tschm/experiments)

Here we support the creation of notebooks without the ambition to release software.
The repo is not minimalistic but comes with a curated set of pre-commit hooks and
follows modern and established guidelines.

- uv support
- curated pre-commit-hooks
- DevContainer
- github ci/cd workflows
- Makefile
- marimo support

### [The package template](https://github.com/tschm/package)

The package template is most useful when the final
goal is the release of software to a registry, e.g. pypi.
It features include

- uv support
- curated set of pre-commit hooks
- DevContainer
- Makefile
- github ci/cd workflows
- marimo support
- JupyterBook
- pdoc documentation

## :warning: Private repositories

Using workflows in private repos will eat into your monthly GitHub bill.
You may want to restrict the workflow to operate only when merging on the main branch
while operating on a different branch or deactivate the flow.
