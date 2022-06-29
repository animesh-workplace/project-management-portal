## Project Management Portal

### For developers

> Running reloading backend server
```python3
gunicorn backend.asgi:application -c gunicorn.config.py --reload 
```
or
```python3
gunicorn backend.asgi:application -c gunicorn.config.py --log-level debug --reload 
```