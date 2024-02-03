from multiprocessing import cpu_count
import os

bind = f"0.0.0.0:{os.environ.get('BACKEND_PORT')}"
workers = (cpu_count() * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"
capture_output = True
loglevel = "debug"
