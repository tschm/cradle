# cvxcli

[![PyPI version](https://badge.fury.io/py/cvxcli.svg)](https://badge.fury.io/py/cvxcli)
[![Apache 2.0 License](https://img.shields.io/badge/License-APACHEv2-brightgreen.svg)](https://github.com/cvxgrp/cvxcli/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/personalized-badge/cvxcli?period=month&units=international_system&left_color=black&right_color=orange&left_text=PyPI%20downloads%20per%20month)](https://pepy.tech/project/cvxcli)
[![Coverage Status](https://coveralls.io/repos/github/cvxgrp/simulator/badge.png?branch=main)](https://coveralls.io/github/cvxgrp/cvxcli?branch=main)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/cvxgrp/cvxcli)

We demonstrate how to deploy to simple command line apps using uvx.

## Install uvx

The current way to deploy apps is to use [uvx](https://docs.astral.sh/uv/guides/tools/).
The tool creates a temporary virtual environment for each app.

For the installation of uv/uvx please refer to the [uvx documentation](https://docs.astral.sh/uv/getting-started/installation/).

## Install cvxcli with uvx

cvxcli has been deployed to PyPI like any other Python package. It could be
installed via pip but we advise against that.

cvxcli is not exactly a package you should use as a dependency in your own code.
cvxcli is the home for two apps that are meant to be used from the command line.
So please run via uvx

```bash
uvx --from cvxcli weather
```

This command will create a temporary virtual environment for cvxcli
and install the package into that environment.

Please note that you **do need uvx** to be installed on your machine.
