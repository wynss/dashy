from dashy import create_app
from dashy.components import navbar, tabs, div


app = create_app(__name__, layout=[
    navbar('My App', dark=True),
    tabs(id='tabs', labels=['Tab1', 'Tab2', 'Tab3'], content_id='tab-content')
])


@app.cb(('tabs', 'active_tab'), ('tab-content', 'children'))
def switch_tabs(tab_id: str):
    return div(f'Hello from {tab_id}')


if __name__ == "__main__":
    app.launch()
