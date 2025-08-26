import os
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = px.data.gapminder().query("year == 2007").copy()

app = dash.Dash(__name__, title="Dash Docker Starter")
server = app.server  # for gunicorn

app.layout = html.Div(
    [
        html.H2("Dash on Docker"),
        html.Div(
            [
                html.Label("대륙 선택"),
                dcc.Dropdown(
                    id="continent",
                    options=[{"label": c, "value": c} for c in sorted(df["continent"].unique())],
                    value="Asia",
                    clearable=False,
                    style={"width": 300},
                ),
            ],
            style={"marginBottom": 16},
        ),
        dcc.Graph(id="scatter"),
        html.Div(id="summary", style={"marginTop": 12, "fontWeight": "600"}),
    ],
    style={"padding": 24, "fontFamily": "ui-sans-serif"},
)

@ app.callback(
    Output("scatter", "figure"),
    Output("summary", "children"),
    Input("continent", "value"),
)
def update(continent):
    dff = df[df["continent"] == continent]
    fig = px.scatter(
        dff,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="country",
        hover_name="country",
        size_max=40,
        title=f"{continent} — GDP vs Life Expectancy (2007)",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    return fig, f"표본 수: {len(dff):,}개"

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))  # Cloud Run 기본 포트
    app.run(host="0.0.0.0", port=port, debug=False)

