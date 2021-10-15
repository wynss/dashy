from typing import List, Union, Optional

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import dash_table as dt
import plotly.graph_objs as go

PLOT_COLORS = [
    '#2A3F5F',
    '#99B898',
    '#581845',
    '#900C3F',
    '#C70039',
    '#FF5733',
    '#FFC305'
]

DEFAULT_MARGIN = 'm-1'


# ----------------------------------------------------------
#   UI components
# ----------------------------------------------------------
def navbar(title: str, fluid=True, color='primary', dark=False, buttons: List[str] = None) -> dbc.NavbarSimple:
    children = []

    if buttons is not None:
        for b in buttons:
            children.append(dbc.NavItem(dbc.NavLink(b, id=_value_from_label(b))))
    return dbc.NavbarSimple(children, brand=title, fluid=fluid, dark=dark, color=color)


def tabs(labels: List[str], id: str = None, tab_ids: List[str] = None, active_tab=None, content_id=None):
    if id is None:
        id = 'tabs'

    if tab_ids is None:
        tab_ids = [l.lower().replace(' ', '-') for l in labels]

    tab_element_kwargs = {
        'children': [dbc.Tab(label=label, tab_id=tab_id) for label, tab_id in zip(labels, tab_ids)],
        'id': id,
    }

    if active_tab is not None:
        tab_element_kwargs['active_tab'] = active_tab

    tab_element = dbc.Tabs(**tab_element_kwargs)

    if content_id is None:
        content_id = 'tab-content'

    return container([tab_element, container(id=content_id, fluid=True)], fluid=True)


def modal(header, id: str, body_layout=None, footer_layout=None, size='lg', scrollable=True):
    return dbc.Modal([
        dbc.ModalHeader(header, id=id+'-header'),
        dbc.ModalBody(body_layout, id=id+'-body'),
        dbc.ModalFooter(footer_layout, id=id+'-footer')
    ], id=id, size=size, scrollable=scrollable)


def button(name: str, id: str = None, className=DEFAULT_MARGIN, color='primary', spinner_div_id=None, n_clicks=0,
           **kwargs):
    if id is None:
        id = _value_from_label(name) + '-button'
    kwargs['id'] = id

    if spinner_div_id:
        return dbc.Button(
            [dbc.Spinner(hidden_div(spinner_div_id), size="sm", spinner_style={'margin': '3px'}), name],
            className='m-1 d-flex', style={'flex-wrap': 'nowrap'},
            color=color, n_clicks=n_clicks, **kwargs
        )

    return dbc.Button(name, n_clicks=n_clicks, active=0, color=color, className=className, **kwargs)


def button_group(id: str, names: List[str], ids: Optional[List[str]] = None, color='primary'):
    if ids is None:
        ids = [f'{_value_from_label(n)}-button' for n in names]
    return dbc.ButtonGroup([button(n, id, className='', color=color) for n, id in zip(names, ids)], id=id)


def graph(id: str = None, hide=False, **kwargs):
    parent_style = {'align-self': 'stretch'}
    if hide:
        parent_style['display'] = 'none'
    return dbc.Col(children=dcc.Graph(id=id, **kwargs), style=parent_style, id=id + '-parent')


def list_group_heading(text: str, font_size: int = 18):
    style = {}
    if font_size:
        style['font-size'] = font_size
    return dbc.ListGroupItemHeading(text, style=style)


def list_group_text(text: str, font_size: int = 14):
    style = {}
    if font_size:
        style['font-size'] = font_size
    return dbc.ListGroupItemText(text, style=style)


def dropdown(title: str, id: str = None, labels: list = None, initial_label=None, values: list = None,
             options: list = None, placeholder: str = None, clearable=True, searchable=False, multi=False, width=None,
             grow=False, shrink=False):
    style = {}
    if width is not None:
        style['width'] = width
    style['flex'] = f'{int(grow)} {int(shrink)} auto'

    kwargs = {
        'clearable': clearable,
        'searchable': searchable,
        'multi': multi,
        'style': style
    }

    if options is not None:
        if labels is not None or values is not None:
            raise ValueError('If passing options labels nor values can be passed')
        kwargs['options'] = options

    elif labels is not None:
        options = create_options(labels, values)
        kwargs['options'] = options

        if initial_label is not None:
            if isinstance(initial_label, int):
                kwargs['value'] = _value_from_label(labels[initial_label])
            elif isinstance(initial_label, str):
                if initial_label in labels:
                    kwargs['value'] = _value_from_label(initial_label)
                else:
                    raise ValueError("'initial_label' does not exist in 'labels' list")

    if id is None:
        id = _value_from_label(title) + '-drop'
    kwargs['id'] = id

    if placeholder is not None:
        kwargs['placeholder'] = placeholder

    title_div = html.Div(title)
    dd = dcc.Dropdown(**kwargs)

    return col([title_div, dd], className=f' flex-grow-{int(grow)} flex-shrink-{int(shrink)}')


def checklist(id: str, labels: list, values: list = None, initial=None, header=None):
    options = create_options(labels, values)

    kwargs = {
        'id': id,
        'options': options,
        'inline': True,
        'className': 'm-1'
    }

    if initial is not None:
        if isinstance(initial, int):
            initial = [initial]
        kwargs['value'] = [options[i]['value'] for i in initial]

    container_children = []
    if header is not None:
        container_children.append(dbc.Label(header))
    container_children.append(dbc.Checklist(**kwargs))
    return dbc.FormGroup(container_children, className='m-1')


def radios(id: str, labels: list, values: list = None, initial=None):
    options = create_options(labels, values)
    kwargs = {
        'id': id,
        'options': options,
        'inline': True,
        'className': 'm-1'
    }

    if initial is not None:
        if isinstance(initial, int):
            kwargs['value'] = options[initial]['value']

    return dbc.FormGroup(dbc.RadioItems(**kwargs), className='m-1')


def inputs(titles: Union[str, List[str]], ids: Optional[Union[str, List[str]]] = None, input_type='number'):
    if isinstance(titles, str):
        titles = [titles]

    if ids is None:
        ids = [_value_from_label(t) + '-input' for t in titles]
    elif isinstance(ids, str):
        ids = [ids]

    comps = [
        dbc.FormGroup([
            dbc.Label(t),
            dbc.Input(id=i, type=input_type)
        ], className='m-0') for i, t in zip(ids, titles)
    ]

    return row(comps)


def card(id: str, title: str = None, text: str = None, body_layout: list = None):
    if title is not None and text is not None:
        body_layout = [
            html.H4(id=id+'-title', children=title, className='card-title'),
            html.P(id=id+'-text', children=text, className='card-text')
        ]
    return dbc.Card(
        [
            dbc.CardBody(body_layout)
        ],
        id=id
    )


def date_range_picker(id: str, clearable: bool = False):
    return dcc.DatePickerRange(id=id, clearable=clearable, className='d-flex align-self-center')


def spinner(spinner_comp_id: str, size='lg'):
    return dbc.Col(
        dbc.Spinner(
            hidden_div(spinner_comp_id),
            size=size,
            color='#293E4F',
            spinner_style={'margin': '4px'}
        ), className='m-1', style={'justify-content': 'flex-start'})


def table(id, columns, data=None, style_cell=None, style_table=None, **kwargs):
    raise NotImplementedError()
    table = dt.DataTable(id=id, columns=columns, data=data,
                         style_cell=style_cell, style_table=style_table, **kwargs)
    return html.Div([table], className='container col m10 m10')


def progress(id: str):
    return dbc.Progress(id=id)


# ----------------------------------------------------------
#   Layout components
# ----------------------------------------------------------
def container(children: list = None, id: str = None, fluid: bool = True, **kwargs):
    return dbc.Container(children, id=id, fluid=fluid, className='p-0', **kwargs)


def row(children, margin=1, padding=0, **kwargs):
    if 'className' not in kwargs:
        kwargs['className'] = f'm-{margin} p-{padding} d-flex align-items-end'
    else:
        classname = kwargs['className']
        if 'm-' not in classname:
            classname = f'm-{margin} ' + classname
        if 'p-' not in classname:
            classname = f'p-{padding} ' + classname
        kwargs['className'] = classname
    if 'style' not in kwargs:
        kwargs['style'] = {'flex-wrap': 'nowrap'}

    return dbc.Row(children, **kwargs)


def col(children: list, margin=1, padding=0, **kwargs):
    if 'className' not in kwargs:
        kwargs['className'] = f'm-{margin} p-{padding}'
    else:
        classname = kwargs['className']
        if 'm-' not in classname:
            classname = f'm-{margin} ' + classname
        if 'p-' not in classname:
            classname = f'p-{padding} ' + classname
        kwargs['className'] = classname

    return dbc.Col(children, **kwargs)


def div(children: list = None, id: str = None, hidden: bool = False):
    kwargs = {k: v for k, v in locals().items() if v is not None}
    return html.Div(**kwargs)


# ----------------------------------------------------------
#   Control Flow
# ----------------------------------------------------------
def interval(id: str, interval: int, n_intervals: int = 0, disabled: bool = True):
    """
    Creates an interval components that will be triggered each 'interval' milliseconds

    Args:
        id: Id of the component
        interval: How often the components will trigger, in milliseconds
        n_intervals: Initial start value for number of triggers
        disabled: If the interval is active or not
    Returns:
        dcc.Interval component
    """
    return dcc.Interval(id=id, interval=interval, n_intervals=n_intervals, disabled=disabled)


# ----------------------------------------------------------
#   Basic html components
# ----------------------------------------------------------
def hidden_div(id, children=None):
    return html.Div(children=children, id=id, style={'display': 'none'})


# ----------------------------------------------------------
#   Helpers
# ----------------------------------------------------------
def create_options(labels, values=None):
    if values is not None:
        options = [{'label': l, 'value': v} for l, v in zip(labels, values)]
        return options

    options = []
    for label in labels:
        if not isinstance(label, str):
            raise ValueError(f'Labels must be strings was {type(label)}')
        options.append({'label': label, 'value': _value_from_label(label)})
    return options


def _value_from_label(label):
    return label.lower().replace(' ', '-').replace('/', '-')
