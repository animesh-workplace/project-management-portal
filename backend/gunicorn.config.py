from backend.__init__ import __version__

bind = "0.0.0.0:8004"
worker_class = "uvicorn.workers.UvicornWorker"


def on_starting(server):
    print(f"Project version: {__version__}")
