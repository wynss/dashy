import sys
import os

import numpy as np
import dashy as dy
import dashy.components as cp
import dashy.layout_builder as lb
from dashy import theme


x = np.arange(10)
y = np.arange(10) + np.random.rand(10)

layout = [
    cp.header('Demo App'),
    lb.col([
        cp.button('A Button', id='my-button'),
        lb.row([
            cp.line(title='A Line Plot', x=x, y=y, height=500),
            cp.scatter(title='Scatter Plot', x=x, y=y, height=500)
        ])
    ])
]

app = dy.create_app(layout=layout, theme=theme.StandardTheme)


if __name__ == '__main__':
    app.run(debug=True)
