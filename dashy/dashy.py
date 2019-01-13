from functools import wraps

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from dashy import config as cfg
from dashy import layout_builder as lb
from dashy import theme

APP = None


def tabs(labels: list, values: list = None) -> html.Div:
    children = []
    children.append(dcc.Tab(label='Test', value='test',
                            className='tab', selected_className='tab--selected'))
    children.append(dcc.Tab(label='Tabs', value='tabs',
                            className='tab', selected_className='tab--selected'))

    return dcc.Tabs(id='tabs-example', children=children, className='tabs')


def create_app(layout: list = None, theme=theme.StandardTheme, assets_folder: str = None):
    """
    Create an dashy app

    Args:
        layout: UI layout to be display by the app
        assets_folder: Path to all assets files to be used
    Returns:
        A DashyApp object
    """

    if layout is None:
        layout = lb.demo_layout()

    if assets_folder is None:
        assets_folder = cfg.ASSETS_PATH

    app = DashyApp(
        theme=theme, 
        name=__name__, 
        assets_url_path=assets_folder,
        external_scripts=cfg.EXTERNAL_SCRIPTS,
        external_stylesheets=cfg.EXTERNAL_STYLESHEETS,
    )

    app.layout = html.Div(layout)
    APP = app

    return app


class DashyApp(dash.Dash):
    """
    Small wrapper class for dash.Dash class
    """
    def __init__(self, theme, **kwargs):
        super(DashyApp, self).__init__(**kwargs)

        self.theme = theme()

    def run(self, debug=False, **kwargs):

        # Generate css files for theme
        self.theme.compile()

        # Start server
        self.run_server(debug=debug, **kwargs)
