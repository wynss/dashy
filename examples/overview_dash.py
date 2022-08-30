from dash import Dash, html, Output, Input


app = Dash(__name__)

app.layout = html.Div(children=[
    html.Button("A button", id='my-btn'),
    html.Div('Click the button', id='my-div')
])


@app.callback(Output('my-div', 'children'), Input('my-btn', 'n_clicks'))
def button_cb(n_clicks):
    return f'Button has been clicked {n_clicks} times'


if __name__ == "__main__":
    app.run(debug=True)
