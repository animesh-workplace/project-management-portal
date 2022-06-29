## Project Management Portal

### For developers

> Running reloading backend server
```python3
gunicorn backend.asgi:application -b 0.0.0.0:8004 -k uvicorn.workers.UvicornWorker --reload 
```
or
```python3
gunicorn backend.asgi:application -b 0.0.0.0:8004 -k uvicorn.workers.UvicornWorker --log-level debug --reload 
```