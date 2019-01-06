import sys
import os

cwd = os.getcwd()
sys.path.append(os.path.join(cwd))

from dashy import dashy as dy


app = dy.create_app()


# TODO: Idea for callbacks
# @dy.callback(('scatter-graph', 'figure'), [('my-button', 'click')])
# def update_scatter():
#     pass


if __name__ == '__main__':
    app.run(debug=True)
