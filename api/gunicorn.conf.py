### Gunicorn configuration ###
# We use Gunicorn as our WSGI server, but we will set the worker class to Uvicorn
# so really it is ASGI anyway...

# Configure logging.
loglevel = "INFO"
# This configuration WILL fail outside of Compose unless you create these dirs,
# and also chown properly.
errorlog = "/var/log/csb/error.log"
accesslog = "/var/log/csb/access.log"

# Bind to port 8081 and allow up to 2048 pending connections.
bind = ["0.0.0.0:8081"]
backlog = 2048

# Set worker to use uvicorn.
worker_class = "uvicorn.workers.UvicornWorker"

# Configure workers.
workers = 4

# If radio silence from the worker exceeds this number of seconds, replace it with a fresh instance.
timeout = 20

# Maximum number of seconds to wait for the next request in a keep-alive connection.
keepalive = 5
