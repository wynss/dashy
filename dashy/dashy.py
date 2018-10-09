import dash
import dash_core_components as dcc
import dash_html_components as html


def header(title, cn=None, logo=None):

    t = html.Div(title, className='item')
    children = [t]

    if logo is not None:
        img = html.Img(src=logo)
        children.append(img)

    args = {'children': children}

    if cn is not None:
        args['className'] = cn

    h = html.Div(**args)
    return h


def create_app(children: list, static_folder: str=None):
    app = dash.Dash(static_folder=static_folder)

    children.append(html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"))

    app.layout = html.Div(children)
    return app
