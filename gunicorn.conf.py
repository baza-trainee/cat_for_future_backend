from multiprocessing import cpu_count
import os

bind = f"0.0.0.0:{os.environ.get('BACKEND_PORT')}"
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
capture_output = True
loglevel = "warning"
