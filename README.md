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

### Install taskfile

Please install [Taskfile](https://taskfile.dev/installation/).

### Verify a working SSH GitHub connection

Try with

```bash
ssh -T git@github.com
```

or use

### Build the virtual environment

Creating the virtual environment also installs [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
task cradle:install
```

## Using the cradle tool

## Install uvx

The current way to deploy apps is to use [uvx](https://docs.astral.sh/uv/guides/tools/).
The tool creates a temporary virtual environment for each app.

For the installation of uv/uvx please refer to the [uvx documentation](https://docs.astral.sh/uv/getting-started/installation/).

## Install cvxcradle with uvx

cvxcradle has been deployed to PyPI like any other Python package. It could be
installed via pip but we advise against that.

cvxcradle is a command line app rather than a package you install into your projects.

So please run via uvx

```bash
uvx --from cvxcradle cradle
```

This command will create a temporary virtual environment for cvxcradle
and install the package into that environment.

Please note that you **do need uvx** to be installed on your machine.
