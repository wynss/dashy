import logging
from functools import wraps

import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dashy import config as cfg
from dashy import layout_builder as lb
from dashy import components as cp
from dashy import themes

logging.basicConfig(format='%(levelname)s %(asctime)-15s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_app(layout: list = None, theme=themes.StandardTheme, assets_folder: str = None):
    """
    Create an dashy app

    Args:
        layout: UI layout to be display by the app
        theme: UI Theme to be used
        assets_folder: Path to all assets files to be used
    Returns:
        A DashyApp object
    """

    if layout is None:
        layout = lb.demo_layout()

    if assets_folder is None:
        assets_folder = str(cfg.ASSETS_PATH)

    app = DashyApp(
        theme=theme,
        layout=layout,
        name=__name__,
        assets_folder=assets_folder,
        external_scripts=cfg.EXTERNAL_SCRIPTS,
        external_stylesheets=cfg.EXTERNAL_STYLESHEETS
    )

    return app


class DashyApp(dash.Dash):
    """
    Small wrapper class for dash.Dash class
    """
    def __init__(self, theme, layout: list, **kwargs):
        super(DashyApp, self).__init__(**kwargs)

        if isinstance(theme, str):
            if theme == 'torchboard':
                self.theme = themes.TorchBoardTheme()
                layout.insert(0, cp.header('TorchBoard', logo=str(cfg.ASSETS_PATH / 'pytorch-logo-150px.png')))
        else:
            self.theme = theme()

        self.hidden_div_count = 0

        self.layout = html.Div(layout)

    def run(self, debug=False, **kwargs):

        # Generate css files for theme
        self.theme.compile()

        # Start server
        self.run_server(debug=debug, **kwargs)

    def bind(self, inputs, output=None, states=None):

        # Handle outputs
        if output is None:
            self.hidden_div_count += 1
            output_id = f'auto-hidden-{self.hidden_div_count}'
            output_element = 'children'
            self.layout.children.append(html.Div(id=output_id, style={'display': 'none'}))
        else:
            if not isinstance(output, tuple):
                raise ValueError("'output' needs to be a tuple")
            if not len(output) == 2:
                raise ValueError('output must contain exactly 2 strings')
            output_id, output_element = output

        # Handle inputs
        if not isinstance(inputs, tuple) and not isinstance(inputs, list):
            raise ValueError("'inputs' needs to be a tuple or a list of tuples")
        elif isinstance(inputs, tuple):
            inputs = [inputs]

        input_list = []
        for i in inputs:
            if not isinstance(i, tuple):
                raise ValueError(f'a state must be tuple was: {type(i)}')
            if len(i) != 2:
                raise ValueError('a state must contain exactly 2 strings')

            input_id, input_element = i
            input_list.append(Input(input_id, input_element))

        # handle states
        state_list = []
        if states is not None:

            if not isinstance(states, tuple) and not isinstance(states, list):
                raise ValueError("'states' needs to be a tuple or a list of tuples")
            elif isinstance(states, tuple):
                states = [states]

            for s in states:
                if not isinstance(s, tuple):
                    raise ValueError(f'a state must be tuple was: {type(s)}')
                if len(s) != 2:
                    raise ValueError('a state must contain exactly 2 strings')
                state_id, state_element = s
                state_list.append(State(state_id, state_element))

        def decorator_callback(func):
            # Create real Dash callback
            @self.callback(output=Output(output_id, output_element), inputs=input_list, state=state_list)
            def dash_update(*args, **kwargs):
                components = func(*args, **kwargs)
                components = self.apply_theme(components)
                return components

            # For completeness
            wraps(func)
            def wrapper():
                return None
            return wrapper

        return decorator_callback

    def apply_theme(self, components):
        """
        Recursively apply theme to components

        Args:
            components: list of components

        Returns:
            components or None
        """
        if components is None:
            return

        for comp in components:
            if isinstance(comp, dcc.Graph):
                # Add theme colors to layout
                comp.figure.layout.paper_bgcolor = self.theme.background_color
                comp.figure.layout.plot_bgcolor = self.theme.background_color
                comp.figure.layout.font['color'] = self.theme.white
                comp.figure.layout.xaxis['color'] = self.theme.white
                comp.figure.layout.xaxis['gridcolor'] = self.theme.main_color
                comp.figure.layout.xaxis['linecolor'] = self.theme.main_color
                comp.figure.layout.yaxis['color'] = self.theme.white
                comp.figure.layout.yaxis['gridcolor'] = self.theme.main_color
                comp.figure.layout.yaxis['linecolor'] = self.theme.main_color

                for d in comp.figure.data:
                    if isinstance(d, go.Scatter):
                        if d.mode == 'lines':
                            d.line['color'] = self.theme.graph_main_color
            elif hasattr(comp, 'children'):
                self.apply_theme(comp.children)
        return components
