from time import sleep

import dashy.dashy as dy
import dashy.components as dc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

DF_IRIS = px.data.iris()
DF_MEDALS = px.data.medals_long()
DF_GAPMINDER = px.data.gapminder()
DF_MT_BRUNO = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

layout = [
    dc.navbar('Dashy Overview!', dark=True, links=['Home', 'Overview', 'Analysis']),
    dc.tabs(id='tabs', labels=['Plots', 'UI Components', 'Tab3'], content_id='my-content')
]

app = dy.create_app('MyApp', layout, theme=dy.themes.COSMO, suppress_callback_exceptions=True)


@app.cb(('tabs', 'active_tab'), ('my-content', 'children'))
def switch_tabs(tab_id: str):
    match tab_id:
        case 'plots':
            return dc.container([
                dc.row([
                    dc.graph("my-graph-1",
                             figure=px.scatter(DF_IRIS, x="sepal_width", y="sepal_length", color="species",
                                               size='petal_length', hover_data=['petal_width']), height=500),
                    dc.graph("my-graph-2",
                             figure=px.bar(DF_MEDALS, x="medal", y="count", color="nation", text="nation"))
                ], margin=0),
                dc.row([

                    dc.graph("my-graph-3", height=800,
                             figure=px.scatter(DF_GAPMINDER.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop",
                                               color="continent", hover_name="country", log_x=True, size_max=60)
                             ),
                    dc.graph("my-graph-4", height=800, figure=go.Figure(data=[go.Surface(z=DF_MT_BRUNO.values)],
                                                                        layout=go.Layout(title='Mt Bruno Elevation')))
                ]),
            ])
        case 'ui-components':
            return dc.container([
                dc.row([
                    dc.button(text="Button", id='btn-1'),
                    dc.button(text="Popover", id='btn-2', popover_header="This is a popover", color=dc.Color.SECONDARY),
                    dc.button(text="Popover and delay", id='btn-3',
                              popover_body="Below and a bit delayed!", popover_delay=500,
                              popover_placement=dc.Placement.BOTTOM),
                    dc.button("Button with a spinner", id='btn-4', spinner_div_id='btn-spinner-div')
                ], margin=0),
                dc.row([
                    dc.dropdown('Dropdown', width=300),
                    dc.checks(id='checklist', header="Some checks",
                              labels=['Check 1', 'Check 2', 'Check 3'], initial='Check 1'),
                    dc.checks(id='toggles', header="Some Toggles", labels=['Toggle 1', 'Toggle 2', 'Toggle 3'],
                              initial=['Toggle 1', 'Toggle 2'], toggles=True),
                    dc.radios(id='radios', header="Some Radios", labels=['Radio 1', 'Radio 2', 'Radio 3']),
                ], margin=0),
                dc.row([
                    dc.inputs(ids=['input-1', 'input-2', 'input-3'], titles=['Text', 'Number', 'Password'],
                              input_type=[dc.InputType.TEXT, dc.InputType.NUMBER, dc.InputType.PASSWORD]),
                    dc.slider('my-slider', title="A slider", min=0, max=10, step=1,),
                    dc.slider('my-slider', title="A slider with tooltip", min=0, max=100,
                              step=10, tooltip=True, tooltip_always_visible=True)
                ], margin=0),
                dc.row([
                    dc.card('my-card-1', "This is a primary card", "We are horizontal"),
                    dc.card('my-card-2', "This is a warning card", "We are horizontal", color=dc.Color.WARNING)
                ]),
                dc.col([
                    dc.card('my-card-3', "This is a info card", "We are vertical", color=dc.Color.INFO),
                    dc.card('my-card-4', "This is a light card", "We are vertical", color=dc.Color.LIGHT)
                ])
            ], margin=0)
        case _:
            return dc.div(f'Hello from {tab_id}')


@app.cb(('btn-4', 'n_clicks'), ('btn-spinner-div', 'children'))
def btn_spinner(_):
    sleep(5)
    return []


if __name__ == "__main__":
    app.run_app(debug=True)
