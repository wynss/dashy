import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go


def header(title: str, logo: str = None) -> html.Div:
    t = html.Div(title, className='item')
    children = [t]

    if logo is not None:
        img = html.Img(src=logo)
        children.append(img)

    h = html.Div(children, className='header')
    return h


def text(text: str, id: str = None, font_size: int = 15, align: str = 'center', tight=False):

    css_classes = [
        'container',
        'curved',
        f's{font_size}',
        f'align-{align}'
    ]

    if not tight:
        css_classes.append('m10')
        css_classes.append('p10')

    kwargs = {
        'children': text,
        'className': ' '.join(css_classes)
    }

    if id is not None:
        kwargs['id'] = id

    return html.Div(**kwargs)


def code(src: str, id: str = None, tight=False):

    css_classes = [
        'container',
        'curved'
    ]

    if not tight:
        css_classes.append('m10')
        css_classes.append('p10')

    kwargs = {
        'children': src,
    }
    if id is not None:
        kwargs['id'] = id

    return html.Pre(html.Code(**kwargs), className=' '.join(css_classes))

#----------------------------------------------------------
#   Graphs
#----------------------------------------------------------

def scatter(x, y, title: str = None, id: str = None):
    data = go.Scatter(x=x, y=y, mode='markers')
    layout = go.Layout(title=title)
    figure = go.Figure(data=[data], layout=layout)

    kwargs = {
        'figure': figure,
        'className': 'container curved'
    }

    if id is not None:
        kwargs['id'] = id

    return dcc.Graph(**kwargs)


def line(x, y, title: str = None, id: str = None):
    data = go.Scatter(x=x, y=y, mode='lines')
    layout = go.Layout(title=title)
    figure = go.Figure(data=[data], layout=layout)

    kwargs = {
        'figure': figure,
        'className': 'container curved'
    }

    if id is not None:
        kwargs['id'] = id

    return dcc.Graph(**kwargs)
