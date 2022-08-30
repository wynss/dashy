from time import sleep

import dashy.dashy as dy
import dashy.components as dc
import numpy as np
import plotly.express as px


layout = [
    dc.navbar('Dashy Overview!', dark=True, buttons=['Home', 'Overview', 'Analysis']),
    dc.tabs(id='tabs', labels=['Plots', 'Buttons', 'Tab3'], content_id='my-content'),
    dc.container([
        dc.row([
            dc.card('my-card-1', "This is a card", "this is some text"),
            dc.card('my-card-2', "This is a card", "this is some text")
        ]),
        dc.col([
            dc.card('my-card-3', "This is a card", "this is some text"),
            dc.card('my-card-4', "This is a card", "this is some text")
        ])
    ])
]

app = dy.create_app('MyApp', layout, theme=dy.themes.QUARTZ, suppress_callback_exceptions=True)


@app.cb(('tabs', 'active_tab'), ('my-content', 'children'))
def switch_tabs(tab_id: str):
    match tab_id:
        case 'plots':
            return dc.container([
                dc.row([
                    dc.graph("my-graph-1", figure=px.line(y=np.arange(10))), 
                    dc.graph("my-graph-2", figure=px.scatter(y=2*np.linspace(-10, 10, 100)**2 + 1))
                ], margin=0)
            ])
        case 'buttons':
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
                    dc.checklist(id='checklist', header="Some checks", labels=['Check 1', 'Check 2', 'Check 3'], initial='Check 1'),
                    dc.radios(id='radios', header="Some Radios", labels=['Radio 1', 'Radio 2', 'Radio 3']),
                    dc.inputs(ids=['input-1', 'input-2', 'input-3'], titles=['Input 1', 'Input 2', 'Input 3'], input_type=[dc.InputType.TEXT, dc.InputType.NUMBER, dc.InputType.RANGE])
                ], margin=0)
            ], margin=0)
        case _:
            return dc.div(f'Hello from {tab_id}')


@app.cb(('btn-4', 'n_clicks'), ('btn-spinner-div', 'children'))
def btn_spinner(_):
    sleep(5)
    return []


if __name__ == "__main__":
    app.run_app(debug=True)
