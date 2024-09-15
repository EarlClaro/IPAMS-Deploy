import os
import sys

from waitress import serve
from ipams.wsgi import application


print("Starting server...")
if __name__ == '__main__':
    serve(application, host='192.168.34.127', port='8000')