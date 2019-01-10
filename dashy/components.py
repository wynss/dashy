import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go


# ----------------------------------------------------------
#   Static UI components
# ----------------------------------------------------------
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


# ----------------------------------------------------------
#   UI components
# ----------------------------------------------------------
def button(title: str, id: str = None, font_size: int = 14):

    kwargs = {
        'className': f'std-button s{font_size}'
    }

    if id is not None:
        kwargs['id'] = id

    return html.Div(html.Button(title, **kwargs), className='container curved m10 p10')


def radio_buttons(labels: list, title: str = None, id: str = None, initial_label=None):

    options = _options_from_labels(labels)

    kwargs = {
        'options': options,
        'className': 'container curved m10 p10'
    }

    if id is not None:
        kwargs['id'] = id

    if initial_label is not None:
        if isinstance(initial_label, int):
            kwargs['value'] = _value_from_label(labels[initial_label])
        elif isinstance(initial_label, str):
            if initial_label in labels:
                kwargs['value'] = _value_from_label(initial_label)
            else:
                raise ValueError("'initial_label' does not exist in 'labels' list")

    return dcc.RadioItems(**kwargs)


def dropdown(title: str, id: str = None, labels: list = None, initial_label=None, placeholder: str = None,
             clearable=True, searchable=False):

    kwargs = {
        'clearable': clearable,
        'searchable': searchable
    }

    if labels is not None:
        options = _options_from_labels(labels)
        kwargs['options'] = options

        if initial_label is not None:
            if isinstance(initial_label, int):
                kwargs['value'] = _value_from_label(labels[initial_label])
            elif isinstance(initial_label, str):
                if initial_label in labels:
                    kwargs['value'] = _value_from_label(initial_label)
                else:
                    raise ValueError("'initial_label' does not exist in 'labels' list")

    if id is not None:
        kwargs['id'] = id

    if placeholder is not None:
        kwargs['placeholder'] = placeholder

    title_div = html.Div(title)
    dd = dcc.Dropdown(**kwargs)

    return html.Div([title_div, dd], className='container col m10 p10')


# ----------------------------------------------------------
#   Graphs
# ----------------------------------------------------------
def scatter(x=None, y=None, title: str = None, id: str = None, height: int = None):
    return _line_scatter_graph(id=id, x=x, y=y, title=title, mode='markers', height=height)


def line(x=None, y=None, title: str = None, id: str = None, height: int = None):
    return _line_scatter_graph(id=id, x=x, y=y, title=title, mode='lines', height=height)


def _line_scatter_graph(id, x, y, title: str, mode: str, height: int) -> dcc.Graph:

    # Create data list
    if x is None or y is None:
        data = []
    else:
        data = [go.Scatter(x=x, y=y, mode=mode)]

    # Create layout
    if title is None:
        layout = go.Layout()
    else:
        layout = go.Layout(title=title)

    figure = go.Figure(layout=layout, data=data)

    kwargs = {
        'figure': figure,
        'className': 'container curved p10 m10'
    }

    if id is not None:
        kwargs['id'] = id
    
    # Build style dict
    style = {}
    if height is not None:
        style['height'] = f'{height}px'
    
    kwargs['style'] = style

    return dcc.Graph(**kwargs)


# ----------------------------------------------------------
#   Helpers
# ----------------------------------------------------------
def _options_from_labels(labels):
    options = []
    for l in labels:
        if not isinstance(l, str):
            raise ValueError('Labels must be strings')
        options.append({'label': l, 'value': _value_from_label(l)})
    return options


def _value_from_label(label):
    return label.lower().replace(' ', '-').replace('/', '-')
