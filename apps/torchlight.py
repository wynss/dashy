import dashy as dy
import dashy.components as cp
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

layout = [
    cp.navbar('Torch Light'),
    cp.tabs(labels=['Scalars', 'Gradients', 'Images']),
]

app = dy.create_app('TorchLight', layout)


@app.bind(('tabs', 'active_tab'), ('tab-content', 'children'))
def switch_tab(active_tab):
    return cp.div(active_tab)


if __name__ == '__main__':
    app.run()
