import logging
from functools import wraps

import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dashy import config as cfg
from dashy import layout_builder as lb
from dashy import theme

logging.basicConfig(format='%(levelname)s %(asctime)-15s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
    global APP
    APP = app

    return app


class DashyApp(dash.Dash):
    """
    Small wrapper class for dash.Dash class
    """
    def __init__(self, theme, **kwargs):
        super(DashyApp, self).__init__(**kwargs)

        self.theme = theme()

        self.hidden_div_count = 0

    def run(self, debug=False, **kwargs):

        # Generate css files for theme
        self.theme.compile()

        # Start server
        self.run_server(debug=debug, **kwargs)

    def bind(self, inputs, output=None):
        if output is None:
            self.hidden_div_count += 1
            output_id = f'auto-hidden-{self.hidden_div_count}'
            output_element = 'children'
            self.layout.children.append(html.Div(id=output_id, style={'display': 'none'}))
        else:
            output_id, output_action = output

        if not isinstance(inputs, tuple) and isinstance(inputs, list):
            raise ValueError("'inputs' needs to be a tuple or a list of tuples")
        elif isinstance(inputs, tuple):
            inputs = [inputs]

        input_list = []
        for i in inputs:
            if not isinstance(i, tuple):
                raise ValueError(f'input must be tuple was: {type(i)}')
            if len(i) != 2:
                raise ValueError('input must contain exactly 2 strings')

            input_id, input_action = i
            input_list.append(Input(input_id, input_action))

        def decorator_callback(func):
            @self.callback(Output(output_id, output_element), input_list)
            def dash_update(*args, **kwargs):
                return func(*args, **kwargs)

            # For completeness
            wraps(func)

            def wrapper():
                return None
            return wrapper

        return decorator_callback
