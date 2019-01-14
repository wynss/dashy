import sys
import os

# Append path to dashy folder
sys.path.append(os.path.join(os.sep, *__file__.split(os.sep)[:-2]))

from dashy.dashy import *
