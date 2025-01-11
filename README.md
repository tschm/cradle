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

We currently distinguish

* The document template
* The experiment template
* The package template

### The document template

The
