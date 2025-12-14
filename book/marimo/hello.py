"""Hello World."""

# /// script
# dependencies = [
#     "marimo==0.18.4"
# ]
#
# ///

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
