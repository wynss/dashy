import sys
import os

cwd = os.getcwd()
sys.path.append(os.path.join(cwd))

from dashy import dashy as dy


app = dy.create_app()

if __name__ == '__main__':
    app.run_server(debug=True)
