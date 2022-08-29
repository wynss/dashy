from enum import Enum
from typing import List, Union, Optional, Any

from dash import html
from dash import dcc
from dash.development.base_component import Component
import dash_bootstrap_components as dbc
from plotly.graph_objects import Figure

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


class Size(Enum):
    SM = 'sm'
    MD = 'md'
    LG = 'lg'

    @staticmethod
    def class_name() -> str:
        return 'size'


class Placement(Enum):
    AUTO = 'auto'
    AUTO_START = 'auto-start'
    AUTO_END = 'auto-end'
    TOP = 'top'
    TOP_START = 'top-start'
    TOP_END = 'top-end'
    RIGHT = 'right'
    RIGHT_START = 'right-start'
    RIGHT_END = 'right-end'
    BOTTOM = 'bottom'
    BOTTOM_START = 'bottom-start'
    BOTTOM_END = 'bottom-end'
    LEFT = 'left'
    LEFT_START = 'left-start'
    LEFT_END = 'left-end'

    @staticmethod
    def class_name() -> str:
        return 'placement'


class Trigger(Enum):
    HOVER = 'hover'
    CLICK = 'click'
    FOCUS = 'focus'
    LEGACY = 'legacy'

    @staticmethod
    def class_name() -> str:
        return 'trigger'


# ----------------------------------------------------------
#   UI components
# ----------------------------------------------------------
def navbar(title: str, fluid=True, color='primary', dark=False, buttons: List[str] = None) -> dbc.NavbarSimple:
    children = []
    if buttons is not None:
        for b in buttons:
            children.append(dbc.NavItem(dbc.NavLink(b, id=_value_from_label(b))))

    return dbc.NavbarSimple(children, brand=title, fluid=fluid, dark=dark, color=color)


def tabs(
    labels: List[str],
    id: str,
    content_id: Optional[str],
    tab_ids: Optional[List[str]] = None,
    active_tab: Optional[Union[str, int]] = None
) -> dbc.Container:
    if tab_ids is None:
        tab_ids = [label.lower().replace(' ', '-') for label in labels]

    tab_element_kwargs = {
        'children': [
            dbc.Tab(label=label, tab_id=tab_id) for label, tab_id in zip(labels, tab_ids)
        ],
        'id': id,
    }

    if active_tab is not None:
        if isinstance(active_tab, int):
            active_tab = tab_ids[active_tab]
        tab_element_kwargs['active_tab'] = active_tab

    tab_element = dbc.Tabs(**tab_element_kwargs)

    if content_id is None:
        content_id = 'tab-content'

    return container(id='tab-container', children=[tab_element, container(id=content_id, fluid=True)], fluid=True)


def modal(header, id: str, body_layout=None, footer_layout=None, size='lg', scrollable=True):
    return dbc.Modal([
        dbc.ModalHeader(header, id=id + '-header'),
        dbc.ModalBody(body_layout, id=id + '-body'),
        dbc.ModalFooter(footer_layout, id=id + '-footer')
    ], id=id, size=size, scrollable=scrollable)


def button(
        text: str,
        id: str,
        color: str = 'primary',
        spinner_div_id: Optional[str] = None,
        n_clicks: int = 0,
        popover_header: Optional[str] = None,
        popover_body: Any = None,
        popover_trigger: Trigger = Trigger.HOVER,
        popover_placement: Placement = Placement.RIGHT,
        popover_delay: Optional[dict[str, int] | int] = None
) -> html:
    """ A Button

    Args:
        text (str): Text that will be shown on the button
        id (str): Id of the button
        color (str, optional): Color of the button. Defaults to 'primary'.
        spinner_div_id (_type_, optional): The div that will control when the spinner is shown. Defaults to None.
        n_clicks (int, optional): Number of times the button has been clicked. Defaults to 0.
        popover_header (Optional[str], optional): Popover header. Defaults to None.
        popover_body (Any, optional): Popover body. Defaults to None.
        popover_trigger (Optional[str], optional): Type of popover. Defaults to None.
        popover_placement (str, optional): Popover placement. Defaults to None.
        popover_delay: Delay for showing/hiding the popover.

    Raises:
        ValueError: If not all pop over values are passed

    Returns:
        Div element containing the button and its elements
    """

    kwargs: dict[str, Any] = {
        'id': id,
        'color': color,
        'n_clicks': n_clicks,
        'active': 0,
    }

    # handle spinner
    if spinner_div_id:
        kwargs['children'] = row([
            col(text, margin=0),
            col(spinner(spinner_div_id, size=Size.SM), margin_left=3),
        ], margin=0)
    else:
        kwargs['children'] = text

    ret = [dbc.Button(**kwargs)]

    # Handle popover
    if popover_header is not None or popover_body is not None:
        pop_kwargs = {
            'children': [
                dbc.PopoverHeader(popover_header) if popover_header else None,
                dbc.PopoverBody(popover_body) if popover_body else None
            ],
            'target': id,
            Trigger.class_name(): popover_trigger.value,
            Placement.class_name(): popover_placement.value,
        }

        if popover_delay is not None:
            if isinstance(popover_delay, int):
                popover_delay = {'show': popover_delay, 'hide': popover_delay}
            elif isinstance(popover_delay, dict):
                if 'hide' not in popover_delay or 'show' not in popover_delay:
                    raise ValueError("Popover delay dict must contain 'show' and 'hide'.")
            else:
                raise ValueError("Popover delay must be a 'dict' or an 'int'.")

            pop_kwargs['delay'] = popover_delay

        popover = dbc.Popover(**pop_kwargs)
        ret.append(popover)

    return col(ret)


def button_group(id: str, names: List[str], ids: Optional[List[str]] = None, color='primary'):
    if ids is None:
        ids = [f'{_value_from_label(n)}-button' for n in names]
    return dbc.ButtonGroup([button(n, id, className='', color=color) for n, id in zip(names, ids)], id=id)


def graph(id: str, figure: Optional[Figure] = None, hide=False):
    kwargs = {}
    if figure is not None:
        kwargs['figure'] = figure

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
            html.H4(id=id + '-title', children=title, className='card-title'),
            html.P(id=id + '-text', children=text, className='card-text')
        ]
    return col(dbc.Card([dbc.CardBody(body_layout)], id=id))


def date_range_picker(id: str, clearable: bool = False):
    return dcc.DatePickerRange(id=id, clearable=clearable, className='d-flex align-self-center')


def spinner(spinner_comp_id: str, size: Size):
    return dbc.Spinner(
        children=hidden_div(spinner_comp_id),
        size=size.value,
        spinner_class_name="flex-shrink-0"
    )


def progress(id: str):
    return dbc.Progress(id=id)


# ----------------------------------------------------------
#   Layout components
# ----------------------------------------------------------
def container(children: list = None, fluid: bool = True, **kwargs):
    return dbc.Container(children, fluid=fluid, **kwargs)


def row(
    children: Union[list, str, Component],
    margin: int = 1,
    margin_right: int = None,
    margin_left: int = None,
    margin_top: int = None,
    margin_bottom: int = None,
    padding: int = 0, 
    padding_right: int = None,
    padding_left: int = None,
    padding_top: int = None,
    padding_bottom: int = None,
    **kwargs
) -> dbc.Row:
    kwargs = {
        'className': (
            f'{_get_margin(margin, margin_top, margin_bottom, margin_left, margin_right)} '
            f'{_get_padding(padding, padding_top, padding_bottom, padding_left, padding_right)} '
            f'row-auto d-flex align-items-center'
        )
    }
    return dbc.Row(children, **kwargs)


def col(
    children: Union[list, str, Component],
    margin: int = 1,
    margin_right: Optional[int] = None,
    margin_left: Optional[int] = None,
    margin_top: Optional[int] = None,
    margin_bottom: Optional[int] = None,
    padding: int = 0, 
    padding_right: int = None,
    padding_left: int = None,
    padding_top: int = None,
    padding_bottom: int = None,
    **kwargs
) -> dbc.Col:
    kwargs = {
        'className': (
            f'{_get_margin(margin, margin_top, margin_bottom, margin_left, margin_right)} '
            f'{_get_padding(padding, padding_top, padding_bottom, padding_left, padding_right)} '
            f'col-auto d-flex align-items-center'
        )
    }
    return dbc.Col(children, **kwargs)


def div(children: Optional[Union[list, str, int, float]] = None, id: str = None, hidden: bool = False):
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


def _get_margin(margin: int, margin_top: int, margin_bottom: int, margin_left: int, margin_right: int) -> str:
    """
    Create the bootstrap margin class. If any side is specified
    """
    margins = [margin_top, margin_bottom, margin_left, margin_right]
    return f'm-{margin} ' + ' '.join([f'{k}-{v}' for k, v in zip(['mt', 'mb', 'ms', 'me'], margins) if v is not None])


def _get_padding(padding: int, padding_top: int, padding_bottom: int, padding_left: int, padding_right: int) -> str:
    """
    Create the bootstrap margin class. If any side is specified
    """
    paddings = [padding_top, padding_bottom, padding_left, padding_right]
    return f'p-{padding} ' + ' '.join([f'{k}-{v}' for k, v in zip(['pt', 'pb', 'ps', 'pe'], paddings) if v is not None])
