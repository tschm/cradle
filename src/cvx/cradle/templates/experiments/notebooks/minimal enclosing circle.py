#    Copyright 2023 Stanford University Convex Optimization Group
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md("""# Problem""")
    return


@app.cell
def _(mo):
    mo.md(
        """We compute the radius and center of the smallest enclosing ball for $N$ points in $d$ dimensions."""
    )
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Generate a cloud of points""")
    return


@app.cell
def _():
    import numpy as np
    import plotly.graph_objects as go

    return go, np


@app.cell
def _(np):
    pos = np.random.randn(10000, 3)
    return (pos,)


@app.cell
def _(go, pos):
    # Create the scatter plot
    fig = go.Figure(
        data=go.Scatter(
            x=pos[:, 0], y=pos[:, 1], mode="markers", marker=dict(symbol="x", size=10)
        )
    )

    # Update layout for equal aspect ratio and axis labels
    fig.update_layout(
        xaxis_title="x",
        yaxis_title="y",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
        ),
    )

    # Show the plot
    fig.show()

    # plot makes really only sense when using d=2
    return (fig,)


@app.cell
def _(mo):
    mo.md("""## Compute with cvxpy""")
    return


@app.cell
def _(np):
    import cvxpy as cp

    # We compare 3 equivalent ways to create the constraint that
    # each point has to be within the ball of radius r centered at x
    def con_1(points, x, r):
        return [cp.norm(point - x) <= r for point in points]

    def con_2(points, x, r):
        return [cp.SOC(r, point - x) for point in points]

    def con_3(points, x, r):
        return [
            cp.SOC(
                r * np.ones(points.shape[0]),
                points - cp.outer(np.ones(points.shape[0]), x),
                axis=1,
            )
        ]

    def min_circle_cvx(points, constraints=None, **kwargs):
        # Use con_1 if no constraint construction is defined
        constraints = constraints or con_1
        # cvxpy variable for the radius
        r = cp.Variable(1, name="Radius")
        # cvxpy variable for the midpoint
        x = cp.Variable(points.shape[1], name="Midpoint")

        objective = cp.Minimize(r)
        _constraints = constraints(points, x, r)

        problem = cp.Problem(objective=objective, constraints=_constraints)
        problem.solve(**kwargs)

        return r.value, x.value

    return con_1, con_2, con_3, cp, min_circle_cvx


@app.cell
def _(con_3, min_circle_cvx, pos):
    min_circle_cvx(points=pos, constraints=con_3, solver="MOSEK")
    return


@app.cell
def _(con_3, min_circle_cvx, pos):
    min_circle_cvx(points=pos, constraints=con_3, solver="CLARABEL")
    return


if __name__ == "__main__":
    app.run()
