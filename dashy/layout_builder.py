import numpy as np
import dash_html_components as html

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


def wrap(components:list, direction: str = 'row'):

    for c in components:

        # remove container class
        css_classes = c.className.split(' ')
        if 'curved' in css_classes:
            css_classes.remove('curved')
        c.className = ' '.join(css_classes)

    css_class = f'container curved {direction} m10 p10'
    return html.Div(components, className=css_class)
