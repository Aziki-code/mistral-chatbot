"""
Gunicorn configuration for AzikiAI Chatbot
Production WSGI server settings
"""

import os
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# SSL/TLS Configuration
certfile = os.path.join(os.path.dirname(__file__), "cert.pem")
keyfile = os.path.join(os.path.dirname(__file__), "key.pem")

# Logging
accesslog = os.path.join(os.path.dirname(__file__), "logs", "gunicorn-access.log")
errorlog = os.path.join(os.path.dirname(__file__), "logs", "gunicorn-error.log")
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "azikiai-chatbot"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
