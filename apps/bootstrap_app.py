import dashy as dy
from dashy import cp
from dashy.components import dbc
import plotly.graph_objs as go
import numpy as np

x = np.arange(10)
y = x ** 2

layout = [
    dbc.NavbarSimple([
        dbc.NavItem(dbc.NavLink("Trace Analytics")),
        dbc.NavItem(dbc.NavLink("Result Data")),
    ],
        brand='Trace Analytics',
        dark=True,
        color='primary'
    ),
    dbc.Container([
        dbc.Row([cp.dropdown('Dataset', width=250)], className='m-1'),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    cp.dropdown('Anomaly Type', width=250),
                    dbc.Col([
                        dbc.Button("Label Trace", id='tag-button', color="success", className="m-1"),
                        dbc.Button("Save Labels", color="success", className='m-1')]),
                ], className='d-flex align-items-end', style={'flex-wrap': 'nowrap'})
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Infer", color="success", className="m-1"),
                    dbc.Button("Export ONNX", color="success", className='m-1')
                ]),
                cp.dropdown('Model', width=250),
            ], className='d-flex align-items-end', style={'flex-wrap': 'nowrap'})
        ], className='m-1'),
        dbc.Row([
            cp.graph(id='graph'),
            cp.graph(id='graph-2'),
        ], style={'flex-wrap': 'nowrap'}),
    ], fluid=False),
    dbc.Container(fluid=True)
]

app = dy.create_app(__name__, layout)


@app.bind(('tag-button', 'n_clicks'), ('graph', 'figure'))
def update(_):
    return go.Figure(
        layout=go.Layout(title='t-SNE'),
        data=[
            go.Scatter(x=x, y=y, mode='lines', line={'color': cp.PLOT_COLORS[0]})
        ])


@app.bind(('tag-button', 'n_clicks'), ('graph-2', 'figure'))
def update_2(_):
    return go.Figure(
        layout=go.Layout(title='Trace'),
        data=[
            go.Scatter(x=np.arange(10), y=np.arange(10))
        ])


if __name__ == "__main__":
    app.run(debug=True)
