import os
import sys

# https://stackoverflow.com/questions/53248417/python-pytest-importing-modules-which-import-local-modules
sys.path.append(os.path.dirname(os.path.realpath(__file__)))