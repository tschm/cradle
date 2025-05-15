import marimo

__generated_with = "0.10.10"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""# Demo""")
    return


if __name__ == "__main__":
    app.run()
