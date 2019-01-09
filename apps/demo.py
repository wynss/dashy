import sys
import os

cwd = os.getcwd()
sys.path.append(os.path.join(cwd))

import dashy as dy
import dashy.components as cp
import dashy.layout_builder as lb
import numpy as np


x = np.arange(10)
y = np.arange(10) + np.random.rand(10)

layout = [
    cp.header('Demo App'),
    lb.col([
        cp.button('A Button', id='my-button'),
        lb.row([
            cp.line(title='A Line Plot', x=x, y=y, height=800),
            cp.scatter(title='Scatter Plot', x=x, y=y)
        ])
    ])
]

app = dy.create_app(layout=layout)


# TODO: Idea for callbacks
# @dy.callback(('line-plot', 'figure'), [('my-button', 'click')])
# def update_scatter(click):
#      pass

# Callback with no output
# @dy.callback_no(['my-button'])
# def button_clicked():
#    pass


if __name__ == '__main__':
    app.run(debug=True)
