import sys
import os

# Add your project directory to the sys.path
sys.path.insert(0, '/home/ubuntu/ko-nnect/python-website')

# Activate the virtual environment
activate_this = '/home/ubuntu/ko-nnect/python-website/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import your Flask application
from main import app as application  # Change 'main' to the name of your Flask app module
