import numpy as np
import plotly.graph_objs as go

import dashy as dy
import dashy.components as cp
from dashy import themes

x = np.arange(10)
y = np.arange(10) + np.random.rand(10)

layout = [
    cp.navbar('Test App'),
    cp.container([
        cp.row([cp.graph('test-plot')])
    ]),
    cp.hidden_div('trigger-div')
]

app = dy.create_app(name='MyApp', layout=layout, theme=themes.StandardTheme)


@app.bind(('trigger-div', 'children'), ('test-plot', 'figure'))
def update_plot(_):
    return go.Figure(data=[go.Scatter(x=np.arange(10), y=np.random.rand(10))])


if __name__ == '__main__':
    app.run(debug=False)
