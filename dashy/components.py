import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import plotly.graph_objs as go


# ----------------------------------------------------------
#   Static UI components
# ----------------------------------------------------------
def header(title: str, logo: str = None) -> html.Div:

    t = html.Div(title, className='item')
    children = [t]

    if logo is not None:
        img = html.Img(src=logo, className='logo')
        children.insert(0, img)

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
def button(title: str, id: str = None, font_size: int = 14, n_clicks=None):

    kwargs = {
        'n_clicks': n_clicks,
        'className': f'std-button s{font_size}'
    }

    if id is not None:
        kwargs['id'] = id

    return html.Div(html.Button(title, **kwargs), className='container curved m10 p10')


def radio_buttons(labels: list, id: str = None, initial_label=None):

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


def checkboxes(labels: list, id: str = None, active_labels: list = None):

    options = _options_from_labels(labels)
    kwargs = {
        'options': options,
        'className': 'container curved m10 p10'
    }
    if id is not None:
        kwargs['id'] = id

    if active_labels is not None:
        if all(l in labels for l in active_labels):
            kwargs['values'] = active_labels
        else:
            raise ValueError('Active labels does not match labels')
    else:
        kwargs['values'] = []
    return dcc.Checklist(**kwargs)


def slider(id=None, min=0.0, max=1.0, step=0.01, value=0.0):
    return html.Div(dcc.Slider(id=id, min=min, max=max, step=step, value=value, vertical=True),
                    className='container curved m10 p10')


def dropdown(title: str, id: str = None, labels: list = None, initial_label=None, placeholder: str = None,
             clearable=True, searchable=False, multi=False):

    kwargs = {
        'clearable': clearable,
        'searchable': searchable,
        'multi': multi
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


def table(id, columns, data=None, style_cell=None, style_table=None, **kwargs):
    table = dt.DataTable(id=id, columns=columns, data=data,
                         style_cell=style_cell, style_table=style_table, **kwargs)
    return html.Div([table], className='container col m10 m10')


# ----------------------------------------------------------
#   Graphs
# ----------------------------------------------------------
def scatter(x=None, y=None, title: str = None, id: str = None, figure: go.Figure = None, height: int = None,
            loading_state: bool = False):
    return _line_scatter_graph(id=id, x=x, y=y, title=title, mode='markers', figure=figure, height=height,
                               loading_state=loading_state)


def line(x=None, y=None, title: str = None, id: str = None, figure: go.Figure = None, height: int = None):
    return _line_scatter_graph(id=id, x=x, y=y, title=title, mode='lines', figure=figure, height=height)


def _line_scatter_graph(id, x, y, title: str, mode: str, height: int,
                        loading_state: bool, figure: go.Figure = None) -> dcc.Graph:

    # Create data list
    if x is None or y is None:
        data = []
    else:
        data = [go.Scatter(x=x, y=y, mode=mode)]

    if figure is None:
        # Create layout
        if title is None:
            layout = go.Layout()
        else:
            layout = go.Layout(title=title)

        figure = go.Figure(layout=layout, data=data)

    kwargs = {
        'figure': figure,
        'className': 'container mt0 mb0'
    }

    if id is not None:
        kwargs['id'] = id
    
    # Build style dict
    style = {}
    if height is not None:
        style['height'] = f'{height}px'
    
    kwargs['style'] = style
    graph = dcc.Graph(**kwargs)

    if loading_state:
        graph = add_loading_state(graph)

    return graph


# ----------------------------------------------------------
#   Control Flow
# ----------------------------------------------------------
def interval(id, interval, n_intervals=0):
    """
    Creates an interval components that will be triggered each 'interval' milliseconds

    Args:
        id: Id of the component
        interval: How often the components will trigger, in milliseconds
        n_intervals: Initial start value for number of triggers

    Returns:
        dcc.Interval component
    """
    return dcc.Interval(id=id, interval=interval, n_intervals=n_intervals)


# ----------------------------------------------------------
#   Basic html components
# ----------------------------------------------------------
def div(id, **kwargs):
    return html.Div(id=id, **kwargs)


# ----------------------------------------------------------
#   Helpers
# ----------------------------------------------------------
def _options_from_labels(labels):
    options = []
    for l in labels:
        if not isinstance(l, str):
            raise ValueError(f'Labels must be strings was {type(l)}')
        options.append({'label': l, 'value': _value_from_label(l)})
    return options


def _value_from_label(label):
    return label.lower().replace(' ', '-').replace('/', '-')


def add_loading_state(components):
    kwargs = {'type': 'circle', 'className': 'container m0'}

    style = {'justify-content': 'center', 'align-items': 'center'}
    if isinstance(components, list):
        height = max([c.style['height'] for c in components if 'height' in c.style])
        if height is not None:
            style['height'] = height
    else:
        if 'height' in components.style:
            style['height'] = components.style['height']

    kwargs['style'] = style
    return dcc.Loading(children=components, **kwargs)
