import os
from dotenv import load_dotenv
from backend.__init__ import __version__

load_dotenv(".env")
bind = f"{os.getenv('BASE_HOST')}:{os.getenv('BASE_PORT')}"
worker_class = "uvicorn.workers.UvicornWorker"


def on_starting(server):
    print(f"Project version: {__version__}")
