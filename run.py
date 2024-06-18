
import os
import webbrowser
import socket
from app import FlaskApp

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

if __name__ == "__main__":
    app = FlaskApp().create_app()
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    webbrowser.open(url)
    app.run(port=port)
