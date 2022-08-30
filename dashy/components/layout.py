from typing import Optional, Union

from dash.development.base_component import Component
from dash import html
import dash_bootstrap_components as dbc

from .helpers import get_margin_class, get_padding_class


def container(
    children: list = None, 
    fluid: bool = True, 
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
) -> dbc.Container:
    kwargs = {
        'className': (
            f'{get_margin_class(margin, margin_top, margin_bottom, margin_left, margin_right)} '
            f'{get_padding_class(padding, padding_top, padding_bottom, padding_left, padding_right)}'
        ),
        **kwargs
    }
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
    auto_size: bool = True,
    **kwargs
) -> dbc.Row:
    kwargs = {
        'className': (
            f"{get_margin_class(margin, margin_top, margin_bottom, margin_left, margin_right)} "
            f"{get_padding_class(padding, padding_top, padding_bottom, padding_left, padding_right)} "
            f"{'row-auto' if auto_size else ''} d-flex align-items-center"
        ),
        **kwargs
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
    auto_size: bool = True,
    **kwargs
) -> dbc.Col:
    kwargs = {
        'className': (
            f"{get_margin_class(margin, margin_top, margin_bottom, margin_left, margin_right)} "
            f"{get_padding_class(padding, padding_top, padding_bottom, padding_left, padding_right)} "
            f"{'col-auto' if auto_size else ''} d-flex flex-column align-items-start"
        ),
        **kwargs
    }
    return dbc.Col(children, **kwargs)


def div(children: Optional[Union[list, str, int, float]] = None, id: str = None, hidden: bool = False):
    kwargs = {k: v for k, v in locals().items() if v is not None}
    return html.Div(**kwargs)