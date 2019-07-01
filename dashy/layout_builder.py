import numpy as np
import dash_html_components as html
import dash_core_components as dcc

from dashy import components as cp


def demo_layout():

    layout = [
        cp.header('Dashy'),
        cp.text('Dashy is an interactive visualization framework built on top of Dash.', font_size=14),
        cp.text('Examples', font_size=30),
        wrap([
            cp.text('Scatter plot', font_size=24, tight=True),
            cp.text('Code', font_size=18, align='left', tight=True),
            cp.code(src="""
            from dashy import dashy as dy
            from dashy import components as cp

            layout = [
                cp.scatter(title='Random Scatter', x=np.random.rand(100), y=np.random.rand(100))
            ]

            app = dy.create_app(layout)
            app.run_server()
            """, tight=True),
            cp.text('Output', font_size=18, align='left', tight=True),
            cp.scatter(title='Random Scatter', x=np.random.rand(100),
                       y=np.random.rand(100))
        ], direction='col')
    ]

    return layout


def row(components: list, loading_state: bool = False):
    """
    Helper for wrapping components into a column. See doc for function 'wrap'.
    """
    return wrap(components, direction='row', loading_state=loading_state)


def col(components: list, loading_state: bool = False):
    """
    Helper for wrapping components into a row. See doc for function 'wrap'.
    """
    return wrap(components, direction='col', loading_state=loading_state)


def wrap(components: list, direction: str = 'row', loading_state: bool = False):
    """
    Wraps components together either in a row or in a column.
    The returned component is a flexbox container containing the passed
    components.

    Args:
        components: List with components to wrap
        direction: Wrap to a row or column
        loading_state: If the container should react to loading states of its child components
    """

    _remove_container_class(components)

    css_class = f'container curved {direction} m10 p10'
    div = html.Div(components, className=css_class)
    if loading_state:
        div = cp.add_loading_state(div)
    return div


def _remove_container_class(components):
    for c in components:
        if isinstance(c, dcc.Loading):
            _remove_container_class(c.children)
        else:
            css_classes = c.className.split(' ')
            if 'curved' in css_classes:
                css_classes.remove('curved')
            c.className = ' '.join(css_classes)
