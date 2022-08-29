import dashy.dashy as dy
import dashy.components as dc


layout = [
    dc.navbar('Hello Tabs!', dark=True),
    dc.tabs(id='tabs', labels=['Tab1', 'Tab2', 'Tab3'], content_id='my-content')
]

app = dy.create_app('MyApp', layout)


@app.cb(('tabs', 'active_tab'), ('my-content', 'children'))
def switch_tabs(tab_id: str):
    return dc.div(f'Hello from {tab_id}')


if __name__ == "__main__":
    app.run_app(debug=True)
