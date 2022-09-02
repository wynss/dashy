from time import sleep

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.exceptions import PreventUpdate

import dashy.dashy as dy
import dashy.components as dc

# some example data
DF_IRIS = px.data.iris()
DF_MEDALS = px.data.medals_long()
DF_GAPMINDER = px.data.gapminder()
DF_MT_BRUNO = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv"
)

# create main layout with a nav bar and tabs
main_layout = [
    dc.navbar("Dashy Overview!", dark=True, links=["Home", "Overview", "Analysis"]),
    dc.tabs(
        id="tabs",
        labels=["UI Components", "Plots", "Load And Explore"],
        content_id="my-content",
    ),
]

# create the app
app = dy.create_app(
    "MyApp", main_layout, theme=dy.themes.BOOTSTRAP, suppress_callback_exceptions=True
)


def create_load_files_example(app: dy.DashyApp):

    # Update the dropdown with the column values
    @app.cb(
        inputs=("csv-upload-table", "columns"),
        outputs=[
            ("x-values-drop", "options"),
            ("x-values-drop", "value"),
            ("y-values-drop", "options"),
            ("y-values-drop", "value"),
            ("color-drop", "options"),
            ("color-drop", "value"),
        ],
    )
    def update_drops(cols):
        options = [{"label": c["name"], "value": c["name"]} for c in cols]
        return [
            options,
            options[0]["value"],
            options,
            options[1]["value"],
            options,
            options[-1]["value"],
        ]

    # update the graph
    @app.cb(
        inputs=[
            ("x-values-drop", "value"),
            ("y-values-drop", "value"),
            ("color-drop", "value"),
        ],
        outputs=("load-files-graph", "figure"),
        states=("csv-upload-table", "data"),
    )
    def update_graph(x_col, y_col, color, data):
        if None in [x_col, y_col, data]:
            raise PreventUpdate
        else:
            df = pd.DataFrame.from_records(data)
            return px.scatter(df, x=x_col, y=y_col, color=color)

    layout = dc.container(
        [
            dc.row(dc.graph(id="load-files-graph", height=500)),
            dc.row(
                [
                    dc.dropdown("X-values", placeholder="Select X values", width=300),
                    dc.dropdown("Y-values", placeholder="Select Y values", width=300),
                    dc.dropdown("Color", placeholder="Select color values", width=300),
                ]
            ),
            dc.row(dc.upload_and_show("csv-upload", app=app)),
        ]
    )
    return layout


load_files_layout = create_load_files_example(app)


# Handle switching of tabs
@app.cb(("tabs", "active_tab"), ("my-content", "children"))
def switch_tabs(tab_id: str):
    if tab_id == "plots":
        return dc.container(
            [
                dc.row(
                    [
                        dc.graph(
                            "my-graph-1",
                            figure=px.scatter(
                                DF_IRIS,
                                x="sepal_width",
                                y="sepal_length",
                                title="Scatter plot",
                                color="species",
                                size="petal_length",
                                hover_data=["petal_width"],
                            ),
                            height=500,
                        ),
                        dc.graph(
                            "my-graph-2",
                            figure=px.bar(
                                DF_MEDALS,
                                x="medal",
                                y="count",
                                color="nation",
                                text="nation",
                                title="Bar plot",
                            ),
                        ),
                    ],
                    margin=0,
                ),
                dc.row(
                    [
                        dc.graph(
                            "my-graph-3",
                            height=800,
                            figure=px.scatter(
                                DF_GAPMINDER.query("year==2007"),
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                                hover_name="country",
                                log_x=True,
                                size_max=60,
                                title="Bubble Plot",
                            ),
                        ),
                        dc.graph(
                            "my-graph-4",
                            height=800,
                            figure=go.Figure(
                                data=[go.Surface(z=DF_MT_BRUNO.values)],
                                layout=go.Layout(title="Mt Bruno Elevation"),
                            ),
                        ),
                    ]
                ),
            ]
        )
    elif tab_id == "ui-components":
        return dc.container(
            [
                dc.row(
                    [
                        dc.button(text="Button", id="btn-1"),
                        dc.button(
                            text="Popover",
                            id="btn-2",
                            popover_header="This is a popover",
                            color=dc.Color.SECONDARY,
                        ),
                        dc.button(
                            text="Popover and delay",
                            id="btn-3",
                            popover_body="Below and a bit delayed!",
                            popover_delay=500,
                            popover_placement=dc.Placement.BOTTOM,
                        ),
                        dc.button(
                            "Button with a spinner",
                            id="btn-4",
                            spinner_div_id="btn-spinner-div",
                        ),
                    ],
                    margin=0,
                ),
                dc.row(
                    [
                        dc.dropdown("Dropdown", width=300),
                        dc.checks(
                            id="checklist",
                            header="Some checks",
                            labels=["Check 1", "Check 2", "Check 3"],
                            initial="Check 1",
                        ),
                        dc.checks(
                            id="toggles",
                            header="Some Toggles",
                            labels=["Toggle 1", "Toggle 2", "Toggle 3"],
                            initial=["Toggle 1", "Toggle 2"],
                            toggles=True,
                        ),
                        dc.radios(
                            id="radios",
                            header="Some Radios",
                            labels=["Radio 1", "Radio 2", "Radio 3"],
                        ),
                    ],
                    margin=0,
                ),
                dc.row(
                    [
                        dc.inputs(
                            ids=["input-1", "input-2", "input-3"],
                            titles=["Text", "Number", "Password"],
                            input_type=[
                                dc.InputType.TEXT,
                                dc.InputType.NUMBER,
                                dc.InputType.PASSWORD,
                            ],
                        ),
                        dc.slider(
                            "my-slider",
                            title="A slider",
                            min=0,
                            max=10,
                            step=1,
                        ),
                        dc.slider(
                            "my-slider",
                            title="A range slider with tooltip",
                            min=0,
                            max=100,
                            step=10,
                            tooltip=True,
                            tooltip_always_visible=True,
                            value=[20, 50],
                        ),
                    ],
                    margin=0,
                ),
                dc.row(
                    [
                        dc.card(
                            "my-card-1", "This is a primary card", "We are horizontal"
                        ),
                        dc.card(
                            "my-card-2",
                            "This is a warning card",
                            "We are horizontal",
                            color=dc.Color.WARNING,
                        ),
                    ],
                    margin=0,
                ),
                dc.col(
                    [
                        dc.card(
                            "my-card-3",
                            "This is a info card",
                            "We are vertical",
                            color=dc.Color.INFO,
                        ),
                        dc.card(
                            "my-card-4",
                            "This is a light card",
                            "We are vertical",
                            color=dc.Color.LIGHT,
                        ),
                    ],
                    margin=0,
                ),
                dc.row(dc.upload("upload"), margin=0),
            ],
            margin=0,
        )
    elif tab_id == "load-and-explore":
        return load_files_layout


@app.cb(("btn-4", "n_clicks"), ("btn-spinner-div", "children"))
def btn_spinner(_):
    sleep(5)
    return []


if __name__ == "__main__":
    app.launch(debug=True)
