import dash_html_components as html

from dashy import dashy as dy


children = [
    dy.header('Dashboard', cn='header container', logo='/assets/logo.png'),
    dy.tabs()
]
app = dy.create_app(children)


if __name__ == '__main__':
    app.run_server(debug=True)
