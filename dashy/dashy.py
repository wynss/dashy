import dash
import dash_core_components as dcc
import dash_html_components as html


def header(title, cn=None, logo=None):

    t = html.Div(title, className='item')
    children = [t]

    if logo is not None:
        img = html.Img(src=logo)
        children.append(img)

    h = html.Div(children, className='header container')
    return h


def tabs():
    children = []
    children.append(dcc.Tab(label='Test', value='test',
                            className='tab', selected_className='tab--selected'))
    children.append(dcc.Tab(label='Tabs', value='tabs',
                            className='tab', selected_className='tab--selected'))
    return dcc.Tabs(id='tabs', children=children, className='tabs')


def create_app(children: list, static_folder: str=None):
    app = dash.Dash(static_folder=static_folder)

    children.append(html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"))

    app.layout = html.Div(children)
    return app
