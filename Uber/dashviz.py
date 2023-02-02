import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

# Warning, doesn't work on Dash 2.7 because of this issue: https://github.com/plotly/plotly.py/issues/3631

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
# load_figure_template('SUPERHERO')

df = pd.read_csv("output/uber-clusters.csv", index_col=[0])


@app.callback(
    # Output('dd-dayofweek-text', 'children'),
    Output("hist-spot", "figure"),
    Output("map-spot", "figure"),
    Input("tabs-dayofweek", "value"),
    Input("hour-slider", "value"),
)
def update_graph(day, hour):
    day = int(day)
    hour = int(hour)

    df_map = df[(df["dayofweek"] == day) & (df["hour"] == hour)]

    fig_map = px.scatter_mapbox(
        df_map,
        title="",
        lat="lat",
        lon="lon",
        color="clusters",
        mapbox_style="carto-positron",
        color_continuous_scale=["#323aa8", "#db1616", "#26ab26"],
        size="nbcourses",
        size_max=20,
        zoom=10,
    )
    fig_map.update_layout(showlegend=False, paper_bgcolor="rgb(78, 93, 108)")

    df_hist = df[(df["dayofweek"] == day)]
    fig_hist = px.histogram(
        df_hist,
        x="hour",
        y="nbcourses",
        histfunc="sum",
        opacity=0.5,
        title="Count of courses by hours :",
    )
    fig_hist.update_layout(
        paper_bgcolor="rgb(78, 93, 108)",
        font_color="white",
    )

    # return f'You have selected {DAYS_OF_WEEK[value]}', fig
    return fig_hist, fig_map


app.layout = html.Div(
    children=[
        html.H1(children="Uber courses in New York"),
        # html.Div(children='''
        #     Hot spots of Uber courses per hours
        # ''', className='sub-title'),
        dcc.Dropdown(
            [
                {"label": DAYS_OF_WEEK[0], "value": 0},
                {"label": DAYS_OF_WEEK[1], "value": 1},
                {"label": DAYS_OF_WEEK[2], "value": 2},
                {"label": DAYS_OF_WEEK[3], "value": 3},
                {"label": DAYS_OF_WEEK[4], "value": 4},
                {"label": DAYS_OF_WEEK[5], "value": 5},
                {"label": DAYS_OF_WEEK[6], "value": 6},
            ],
            value=0,
            id="dd-dayofweek",
        ),
        dcc.Tabs(
            id="tabs-dayofweek",
            value="0",
            children=[
                dcc.Tab(label=DAYS_OF_WEEK[0], value="0"),
                dcc.Tab(label=DAYS_OF_WEEK[1], value="1"),
                dcc.Tab(label=DAYS_OF_WEEK[2], value="2"),
                dcc.Tab(label=DAYS_OF_WEEK[3], value="3"),
                dcc.Tab(label=DAYS_OF_WEEK[4], value="4"),
                dcc.Tab(label=DAYS_OF_WEEK[5], value="5"),
                dcc.Tab(label=DAYS_OF_WEEK[6], value="6"),
            ],
        ),
        # html.Div(id='dd-dayofweek-text'),
        dcc.Slider(
            0,
            23,
            1,
            value=10,
            marks={i: "{}h".format(i) for i in range(24)},
            id="hour-slider",
        ),
        # dcc.Checklist(
        # [
        #     {
        #         "label": "Darkmode",
        #         "value": "dark",
        #     },
        # ]
        # ),
        dcc.Graph(
            id="map-spot",
            figure={},
        ),
        dcc.Graph(
            id="hist-spot",
            figure={},
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)
