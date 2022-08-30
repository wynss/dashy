from typing import List, Union, Optional, Any

from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from plotly.graph_objects import Figure

from .attributes import Size, InputType, Color, Trigger, Placement, SliderUpateMode
from .layout import container, row, col
from .helpers import value_from_label, create_options


def navbar(
        title: str,
        fluid=True,
        color: Color = Color.PRIMARY,
        dark=False,
        links: List[str] = None
) -> dbc.NavbarSimple:
    """A Navbar

    Args:
        title (str): Title of the Navbar
        fluid (bool, optional): If True the contents of the navbar will fill the available horizontal space. Defaults to True.
        color (Color, optional): Color of the navbar. Defaults to Color.PRIMARY.
        dark (bool, optional): If True the text in the children of the Navbar to use light colors for contrast/visibility.
                               Defaults to False.
        links (List[str], optional): List of links to add. Defaults to None.

    Returns:
        NavbarSimple component
    """
    children = []
    if links is not None:
        for b in links:
            children.append(dbc.NavItem(dbc.NavLink(b, id=value_from_label(b))))

    return dbc.NavbarSimple(children, brand=title, fluid=fluid, dark=dark, color=color.value)


def tabs(
        labels: List[str],
        id: str,
        content_id: Optional[str],
        tab_ids: Optional[List[str]] = None,
        active_tab: Optional[Union[str, int]] = None
) -> dbc.Container:
    """Create a set of tabs to navigate between different contents.

    Args:
        labels (List[str]): Tab labels, the text that will be shown for each tab.
        id (str): Id of the tabs
        content_id (Optional[str]): Id of the content element that will be populated when switching tab.
        tab_ids (Optional[List[str]], optional): Ids for each tab, will be created if not passed. Defaults to None.
        active_tab (Optional[Union[str, int]], optional): Sets the active tab, by index or label. Defaults to None.

    Returns:
        dbc.Container: Containing the tabs
    """
    if tab_ids is None:
        tab_ids = [label.lower().replace(' ', '-') for label in labels]

    tab_element_kwargs = {
        'children': [dbc.Tab(label=label, tab_id=tab_id) for label, tab_id in zip(labels, tab_ids)],
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


def modal(
    header: str,
    id: str,
    body_layout: Optional[Any] = None,
    footer_layout: Optional[Any] = None,
    size: Size = Size.LG,
    scrollable: bool = True
) -> dbc.Modal:
    """Modal component.

    Args:
        header (str): Header for the modal
        id (str): Id of the modal
        body_layout (Optional[Any], optional): Body layout. Defaults to None.
        footer_layout (Optional[Any], optional): Footer layout. Defaults to None.
        size (Size, optional): Size of the modal. Defaults to Size.LG.
        scrollable (bool, optional): If True the modal will be able to scroll. Defaults to True.

    Returns:
        Modal component
    """
    return dbc.Modal([
        dbc.ModalHeader(header, id=id + '-header'),
        dbc.ModalBody(body_layout, id=id + '-body'),
        dbc.ModalFooter(footer_layout, id=id + '-footer')
    ], id=id, size=size.value, scrollable=scrollable)


def button(
        text: str,
        id: str,
        color: Color = Color.PRIMARY,
        n_clicks: int = 0,
        spinner_div_id: Optional[str] = None,
        popover_header: Optional[str] = None,
        popover_body: Any = None,
        popover_trigger: Trigger = Trigger.HOVER,
        popover_placement: Placement = Placement.TOP,
        popover_delay: Optional[dict[str, int] | int] = None
) -> dbc.Col:
    """ A Button

    Args:
        text (str): Text that will be shown on the button
        id (str): Id of the button
        color (str, optional): Color of the button. Defaults to 'Color.PRIMARY'.
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
        Component containing the button
    """

    kwargs: dict[str, Any] = {
        'id': id,
        'color': color.value,
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


def button_group(
    id: str,
    names: List[str],
    ids: Optional[List[str]] = None,
    color: Color = Color.PRIMARY
) -> dbc.ButtonGroup:
    """A group of buttons

    Args:
        id (str): Id of the group
        names (List[str]): List of strings that will be displayed on the buttons
        ids (Optional[List[str]], optional): Ids for each button. Defaults to None.
        color (Color, optional): Color if the buttons. Defaults to Color.PRIMARY.

    Returns:
        Button group
    """
    if ids is None:
        ids = [f'{value_from_label(n)}-button' for n in names]
    return dbc.ButtonGroup([button(n, id, color=color.value) for n, id in zip(names, ids)], id=id)


def graph(
        id: str,
        figure: Optional[Figure] = None,
        responsive: Union[str, bool] = True,
        animate: bool = False,
        mathjax: bool = False,
        hide: bool = False,
        height: Optional[int] = None
) -> dbc.Col:
    """A Graph

    Args:
        id (str): Id of the graph
        figure (Optional[Figure], optional): Plotly figure. Defaults to None.
        responsive: If True the grapth including the plotly figure will be responsive.
        animate: If the transitions should be animated using plotly.js animate function.
        mathjax: If mathjax should be loaded and used for equations.
        hide (bool, optional): If the graph should be hidden. Defaults to False.
        height: Height of the graph.

    Returns:
        Component containing the graph
    """
    kwargs = {}
    if figure is not None:
        # center title
        figure.update_layout(dict(title={'x': 0.5}))
        kwargs['figure'] = figure

    parent_style = {'align-self': 'stretch'}

    if height is not None:
        parent_style['height'] = f'{height}px'

    if hide:
        parent_style['display'] = 'none'

    return col(children=[
        dcc.Graph(id=id, **kwargs, className="w-100 h-100", animate=animate, responsive=responsive, mathjax=mathjax)
    ], style=parent_style, id=id + '-parent', margin=0, auto_size=False)


def dropdown(
        title: str,
        id: str = None,
        labels: list = None,
        initial_label=None,
        values: list = None,
        options: list = None,
        placeholder: str = None,
        clearable=True,
        searchable=False,
        multi=False,
        width=None,
        grow=False,
        shrink=False
) -> dbc.Col:
    """A Dropdown.

    Args:
        title (str): Title of the dropdown that will be displayed
        id (str, optional): Id of the dropdown. Defaults to None.
        labels (list, optional): Labels of the dropdown elements. Defaults to None.
        initial_label (_type_, optional): Inital label that will be selected. Defaults to None.
        values (list, optional): Values of the dropdown elements. Defaults to None.
        options (list, optional): Options for the dropdown. Defaults to None.
        placeholder (str, optional): Placeholder text. Defaults to None.
        clearable (bool, optional): If True the dropdown will be able to have nothing selected. Defaults to True.
        searchable (bool, optional): If True the dropdown will be searchable. Defaults to False.
        multi (bool, optional): If True the dropdown will be able to select multiple elements. Defaults to False.
        width (_type_, optional): Width of the dropdown in pixels. Defaults to None.
        grow (bool, optional): If the dropdown should be able to grow. Defaults to False.
        shrink (bool, optional): If the dropdown should be able to shrink. Defaults to False.

    Raises:
        ValueError: If 'options' and 'labels'/'values' are passed. Only one can be passed
        ValueError: If the initial label does not exists in 'options' or 'labels'.

    Returns:
        Component containing the dropdown
    """
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
                kwargs['value'] = value_from_label(labels[initial_label])
            elif isinstance(initial_label, str):
                if initial_label in labels:
                    kwargs['value'] = value_from_label(initial_label)
                else:
                    raise ValueError("'initial_label' does not exist in 'labels' list")

    if id is None:
        id = value_from_label(title) + '-drop'
    kwargs['id'] = id

    if placeholder is not None:
        kwargs['placeholder'] = placeholder

    title_div = html.Div(title)
    dropdown = dcc.Dropdown(**kwargs)

    return col(dbc.Form([title_div, dropdown]))


def checks(
        id: str,
        labels: list,
        values: list = None,
        initial: Optional[Union[str, int, list[str], list[int]]] = None,
        header: Optional[str] = None,
        inline: bool = True,
        toggles: bool = False
) -> dbc.Col:
    """Checkboxes

    Args:
        id (str): Id of the check list
        labels (list): Labels/Names of the check boxes
        values (list, optional): Values of hte checkboxes, will be created if not passed. Defaults to None.
        initial (Optional[Union[str, int]], optional): The initial value(s) for the checkboxes. Defaults to None.
        header (Optional[str], optional): Header text. Defaults to None.
        inline (bool, optional): If the checkboxes should be on a row (True) or column (False). Defaults to True.
        toggles (bool, optional): If the checkboxes chould render as toggles. Defaults to False.

    Returns:
        Component containing the checkboxes
    """
    options = create_options(labels, values)
    kwargs = {
        'id': id,
        'options': options,
        'inline': inline,
        'switch': toggles
    }

    # handle inital values
    if initial is not None:
        if not isinstance(initial, list):
            initial = [initial]

        if all([isinstance(el, str) for el in initial]):
            kwargs['value'] = [op['value'] for op in options if op['label'] in initial]
        elif all([isinstance(el, int) for el in initial]):
            kwargs['value'] = [options[i]['value'] for i in initial]
        else:
            raise ValueError("'initial' need to contain all 'str' or all 'int' if passed as a 'list'")

    container_children = []
    if header is not None:
        container_children.append(dbc.Label(header))

    container_children.append(dbc.Checklist(**kwargs))
    return col(dbc.Form(container_children))


def radios(
        id: str,
        labels: list,
        values: Optional[list] = None,
        initial: Optional[Union[str, int]] = None,
        header: Optional[str] = None,
        inline: bool = True
) -> dbc.Col:
    """Radio buttons

    Args:
        id (str): Id of the radio buttons
        labels (list): Labels/Name of the buttons
        values (Optional[list], optional): Values of the buttons, will be generate if not passed. Defaults to None.
        initial (Optional[Union[str, int]], optional): Initial value of the buttons. Defaults to None.
        header (Optional[str], optional): Header text. Defaults to None.
        inline (bool, optional): If the buttons should be on a row (True) or column (False). Defaults to True.

    Returns:
        Component containing the radio buttons
    """
    options = create_options(labels, values)
    kwargs = {
        'id': id,
        'options': options,
        'inline': inline,
    }

    # handle initial value
    if initial is not None:
        if isinstance(initial, int):
            kwargs['value'] = [options[initial]['value']]
        elif isinstance(initial, str):
            kwargs['value'] = [op['value'] for op in options if op['label'] == initial]

    container_children = []
    if header is not None:
        container_children.append(dbc.Label(header))

    container_children.append(dbc.RadioItems(**kwargs))
    return col(dbc.Form(container_children))


def inputs(
        titles: Union[str, List[str]],
        ids: Optional[Union[str, List[str]]] = None,
        input_type: Optional[Union[InputType, list[InputType]]] = None,
        size: Size = Size.MD
) -> dbc.Col:
    """An input compnent or a set of input components.

    Args:
        titles (Union[str, List[str]]): Titles of the inputs
        ids (Optional[Union[str, List[str]]], optional): Ids of the inputs. Defaults to None.
        input_type (Union[InputType, list[InputType]], optional): Type for each input. Defaults to InputType.NUMBER.
        size (Size, optional): Size of the inputs. Defaults to Size.MD.

    Raises:
        ValueError: If the 'input_type' is a list with different length than 'titles'

    Returns:
        Component containing the input components
    """

    if isinstance(titles, str):
        titles = [titles]

    if isinstance(input_type, list):
        if len(input_type) != len(titles):
            raise ValueError("Number of 'titles' and specified 'input_type' must the same.")
    elif input_type is None:
        input_type = len(titles) * [InputType.NUMBER]

    if ids is None:
        ids = [value_from_label(t) + '-input' for t in titles]
    elif isinstance(ids, str):
        ids = [ids]

    return col(
        row([
            col(dbc.Form(
                [dbc.Label(t), dbc.Input(id=i, type=it.value, size=size.value)]
            ), margin=1) for i, t, it in zip(ids, titles, input_type)
        ], margin=0),
        margin=0
    )


def slider(
    id: str,
    title: str,
    min: int,
    max: int,
    step: int,
    value: Optional[int] = None,
    marks: Optional[Union[dict[int, str], bool]] = True,
    update_mode: SliderUpateMode = SliderUpateMode.MOUSE_UP,
    tooltip: bool = False,
    tooltip_placement: Placement = Placement.BOTTOM,
    tooltip_always_visible: bool = False,
    vertical: bool = False,
    vertical_height: int = 400
) -> dbc.Col:
    """A slider

    Args:
        id: Id of the slider
        title: Title that will be displayed above the slider
        min: Min value of the slider
        max: Max value of the slider
        step: Step size between min and max range
        value: Initial value. If None 'min' will be used
        marks: Slider marks. If True marks will be generated. If None no marks will be visible.
               Can also pass a dict with custom marks
        update_mode: How the value of the slider should be updated.
        tooltip: If True a tooltip will be shown.
        tooltip_placement: Placement of the tooltip.
        tooltip_always_visible: If True the tooltip will always be shown, if False it will only show it on hover.
        vertical: If True the slider will be vertical
        vertical_height: Height in px if the slider is vertical

    Returns:
        Slider component
    """
    if value is None:
        value = min

    kwargs = dict(
        id=id,
        min=min,
        max=max,
        step=step,
        updatemode=update_mode.value,
        value=value,
        className="w-100 h-100",
        vertical=vertical,
        verticalHeight=vertical_height
    )

    if marks is None or isinstance(marks, dict):
        kwargs['marks'] = marks

    if tooltip is True:
        kwargs['tooltip'] = {
            Placement.class_name(): tooltip_placement.value,
            'always_visible': tooltip_always_visible
        }

    return col([dbc.Label(title), dcc.Slider(**kwargs)], auto_size=False)


def card(
        id: str,
        title: Optional[str] = None,
        text: Optional[str] = None,
        body_layout: Optional[list] = None,
        color: Color = Color.PRIMARY
) -> dbc.Col:
    """A card

    Args:
        id (str): Id of the card
        title (Optional[str], optional): Title of the card. Defaults to None.
        text (Optional[str], optional): Text of the card. Defaults to None.
        body_layout (Optional[list], optional): The layout of the card, will override the title and text if passed.
        color (Color, optional): _description_. Defaults to Color.PRIMARY.

    Returns:
        Component containing the Card
    """
    if body_layout is None:
        if title is not None and text is not None:
            body_layout = [
                html.H4(id=id + '-title', children=title, className='card-title'),
                html.P(id=id + '-text', children=text, className='card-text')
            ]
        else:
            raise ValueError("Must pass both 'title' and 'text' to card if 'body_layout' is not passed")

    # handle text color
    if color == Color.LIGHT:
        inverse = False
    else:
        inverse = True

    return col(dbc.Card([dbc.CardBody(body_layout)], id=id, color=color.value, inverse=inverse), margin=1)


def date_range_picker(id: str, clearable: bool = False) -> dcc.DatePickerRange:
    """A date range picker component. Used to select a date.

    Args:
        id (str): Id of the date picker.
        clearable (bool, optional): If True the date picker will be able to have nothing selected. Defaults to False.

    Returns:
        dcc.DatePickerRange
    """
    return dcc.DatePickerRange(id=id, clearable=clearable, className='d-flex align-self-center')


def spinner(spinner_comp_id: str, size: Size) -> dbc.Spinner:
    """A Spinner. Can be used to indicate that something is loading

    Args:
        spinner_comp_id (str): The id of the component that will trigger the spinner.
        size (Size): Size of the sponner

    Returns:
        dbc.Spinner
    """
    return dbc.Spinner(
        children=hidden_div(spinner_comp_id),
        size=size.value,
        spinner_class_name="flex-shrink-0"
    )


def progress(id: str) -> dbc.Progress:
    """A progress bar component.

    Args:
        id (str): Id of the progress bar

    Returns:
        dbc.Progress
    """
    return dbc.Progress(id=id)


def interval(id: str, interval: int, n_intervals: int = 0, disabled: bool = True) -> dcc.Interval:
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


def hidden_div(id: str, children: Optional[Any] = None) -> html.Div:
    """A hidden Div

    This can for example be used for storing some data when some action has been completed.

    In the background these divs are also created when a callback without in output is created.

    Args:
        id (str): Id of the div
        children (Optional[Any], optional): Children of the div. Defaults to None.

    Returns:
        A hidden html.Div
    """
    return html.Div(children=children, id=id, style={'display': 'none'})
