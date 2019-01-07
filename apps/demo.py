import sys
import os

cwd = os.getcwd()
sys.path.append(os.path.join(cwd))

import dashy as dy
import dashy.components as cp
import dashy.layout_builder as lb
import numpy as np


layout = [
    cp.header('Demo App'),
    lb.wrap([
        cp.button('A Button', id='my-button'),
        cp.line(title='A Line Plot', x=np.arange(10), y=np.arange(10) + np.random.rand(10), id='line-plot')
    ], direction='col')
]

app = dy.create_app(layout=layout)


# TODO: Idea for callbacks
# @dy.callback(('line-plot', 'figure'), [('my-button', 'click')])
# def update_scatter():
#      pass


if __name__ == '__main__':
    app.run(debug=True)
