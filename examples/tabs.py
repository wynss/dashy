import dashy.dashy as dy
import dashy.components as cp


layout = [
    cp.navbar('Hello Tabs!', dark=True),
    cp.tabs(id='tabs', labels=['Tab1', 'Tab2', 'Tab3'], content_id='my-content')
]

app = dy.create_app('MyApp', layout=layout)


@app.bind(('tabs', 'active_tab'), ('my-content', 'children'))
def switch_tabs(tab_id: str):
    return cp.div(f'Hello from {tab_id}')


app.run()
