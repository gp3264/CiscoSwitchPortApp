
import os
import random
import webbrowser
import socket
from app import FlaskApp
import warnings

##def find_free_port():
##    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
##        s.bind(('', 0))
##        return s.getsockname()[1]

def find_free_port():
    while True:
        port = random.randint(49152, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port

# Create an instance of the Flask application
app_instance = FlaskApp().create_app()

if __name__ == "__main__":
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    webbrowser.open(url)    
    app_instance.run(port=port)
