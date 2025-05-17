# Hypercorn config for running FastAPI app

bind = ["0.0.0.0:8000"]
workers = 1
accesslog = "-"
errorlog = "-"
loglevel = "info"
