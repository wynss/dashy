import dashy as dy
import dashy.components as dc


layout = dc.sidebar(
    title="This is a Dashboard",
    id='sidebar',
    links=['Page 1', 'Page 2', 'Page 3'],
    text="A simple dashboard with navigation. Try clicking the links."
)
app = dy.create_app(__name__, layout=layout)


@app.cb(('sidebar-url', 'pathname'), ('sidebar-content', 'children'))
def switch_page(url):
    return dc.html.H2(f'Hello from {url}')


if __name__ == '__main__':
    app.launch()
