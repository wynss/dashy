import time

import numpy as np
import plotly.graph_objs as go

import dashy as dy
import dashy.components as cp
from dashy.layout_builder import col, row
from dashy import themes

x = np.arange(10)
y = np.arange(10) + np.random.rand(10)

layout = [
    cp.header('Demo App'),
    col([
        row([
            cp.button('A Button', id='button'),
            cp.dropdown('Plot', 'drop-1', labels=['Scatter', 'Line'], initial_label=0),
            cp.dropdown('Change Data', 'drop-2', labels=['Data2', 'Data1'], initial_label=0),
        ]),
        row([
            cp.scatter(title='Some data', id='plot-1', height=500),
            cp.scatter(title='', id='plot-2', height=500)
        ], loading_state=True),
        row([cp.scatter(title='Some Data', id='plot-3', height=300)], loading_state=True)
    ])
]

app = dy.create_app(layout=layout, theme=themes.StandardTheme)


@app.bind(('drop-1', 'value'), ('plot-1', 'figure'))
def update_plot(plot_type):
    print(plot_type)
    time.sleep(0.5)
    if plot_type == 'scatter':
        data = [go.Scatter(x=x, y=y, mode='markers')]
    else:
        data = [go.Scatter(x=x, y=y, mode='lines')]
    return go.Figure(data=data)


@app.bind(('drop-2', 'value'), ('plot-3', 'figure'))
def update_data_plot(data):
    time.sleep(1.0)
    return go.Figure()


if __name__ == '__main__':
    app.run(debug=False)
