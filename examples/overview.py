from time import sleep

import dashy.dashy as dy
import dashy.components as dc
import numpy as np
import plotly.express as px


layout = [
    dc.navbar('Dashy Overview!', dark=True, buttons=['Home', 'Overview', 'Analysis']),
    dc.tabs(id='tabs', labels=['Plots', 'Buttons', 'Tab3'], content_id='my-content'),
    dc.row([
        dc.card('my-card', "This is a card", "this is some text"), 
        dc.card('my-card-2', "This is a card", "this is some text")
    ])
]

app = dy.create_app('MyApp', layout, theme=dy.themes.FLATLY, suppress_callback_exceptions=True)


@app.cb(('tabs', 'active_tab'), ('my-content', 'children'))
def switch_tabs(tab_id: str):
    match tab_id:
        case 'plots':
            return dc.container([
                dc.row([
                    dc.graph("my-graph-1", figure=px.line(y=np.arange(10))), 
                    dc.graph("my-graph-2", figure=px.scatter(y=2*np.linspace(-10, 10, 100)**2 + 1))
                ])
            ])
        case 'buttons':
            return dc.container(
                dc.row([
                    dc.button(text="Button", id='btn-1'),
                    dc.button(text="Button with a popover", id='btn-2', popover_header="This is a popover"),
                    dc.button(text="Button with a popover and delay", id='btn-3',
                              popover_body="This is a popover a bit delayed!", popover_delay=500,
                              popover_placement=dc.Placement.TOP),
                    dc.button("Button with a spinner", id='btn-4', spinner_div_id='btn-spinner-div')
                ])
            )
        case _:
            return dc.div(f'Hello from {tab_id}')


@app.cb(('btn-4', 'n_clicks'), ('btn-spinner-div', 'children'))
def btn_spinner(_):
    sleep(5)
    return []


if __name__ == "__main__":
    app.run_app(debug=True)
