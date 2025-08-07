# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15"
# ]
# ///
"""Hello World."""

import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import marimo as mo


@app.cell
def _():
    mo.md(r"""# Marimo Hello World""")
    return


if __name__ == "__main__":
    app.run()
