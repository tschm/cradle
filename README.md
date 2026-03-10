# 🚀 Cradle Actions

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/tschm/cradle/badge)](https://www.codefactor.io/repository/github/tschm/cradle)
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/renovatebot/renovate)

⚙️ A collection of reusable GitHub Actions for Python projects.
These actions are defined in the `actions` directory and can be referenced
in your workflows to standardise CI/CD pipelines across repositories.

## 🛠️ Available Actions

| Action | Description |
|--------|-------------|
| 📚 **book** | Builds and publishes a Jupyter Book |
| 📦 **build** | Builds a Python package and uploads artifacts |
| 📊 **coverage** | Generates and uploads code coverage reports |
| 🔍 **deptry** | Checks for dependency issues using deptry |
| 🐳 **docker** | Builds and pushes Docker images |
| 🔧 **environment** | Sets up Python environment with dependencies |
| 📄 **latex** | Compiles LaTeX documents |
| 📝 **pdoc** | Generates API documentation using pdoc |
| ✅ **pre-commit** | Runs pre-commit hooks |
| 🏷️ **tag** | Bumps version, creates a tag, and publishes a release |
| 🧪 **test** | Runs tests with pytest |

## 📋 How to Use These Actions

Reference any action in your GitHub workflow using the `uses` keyword:

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

Each action has its own inputs and outputs defined in its `action.yml` file.
Examine these files in the `actions/` directory for full details.

## :warning: Private repositories

Using workflows in private repos will eat into your monthly GitHub bill.
You may want to restrict the workflow to operate only when merging on the main branch
while operating on a different branch or deactivate the flow.
