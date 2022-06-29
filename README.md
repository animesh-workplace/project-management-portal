## Project Management Portal

### For developers

> Running reloading backend server
`gunicorn backend.asgi:application -b 0.0.0.0:8004 -k uvicorn.workers.UvicornWorker --reload `
or
`gunicorn backend.asgi:application -b 0.0.0.0:8004 -k uvicorn.workers.UvicornWorker --log-level debug --reload `