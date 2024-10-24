# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti <crmihai1@ie.ibm.com>
Description: GUNICORN CONFIGURATION
Reference: https://docs.gunicorn.org/en/stable/settings.html
Notes:
- Set bind = "0.0.0.0:8080" to set the IP (all) and port (8080)
- Set a timeout to avoid worker timeout in containers, as the workers
will have to wait a long time for queries to IBM Consulting Assistants
Reference: https://stackoverflow.com/questions/10855197/frequent-worker-timeout
"""

# import multiprocessing
bind = "0.0.0.0:8080"  # Bind addres / port
workers = 6  # A positive integer generally in the 2-4 x $(NUM_CORES)
timeout = 120  # Set a timeout of 120
loglevel = "info"  # debug info warning error critical
max_requests = 5000  # The maximum number of requests a worker will process before restarting
max_requests_jitter = 60  # The maximum jitter to add to the max_requests setting.

# Server model: https://docs.gunicorn.org/en/stable/design.html
# worker-class = "eventlet" #  Requires eventlet >= 0.24.1, pip install gunicorn[eventlet]
# worker-class = "gevent"   #  Requires gevent >= 1.4, pip install gunicorn[gevent]
# worker_class = "tornado"  #  Requires tornado >= 0.2, pip install gunicorn[tornado]
# threads = 2       # A positive integer generally in the 2-4 x $(NUM_CORES) range.
# gevent

# pidfile = '/tmp/gunicorn-pidfile'
# errorlog = '/tmp/gunicorn-errorlog'
# accesslog = '/tmp/gunicorn-accesslog'
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# certfile = 'certs/cert.pem'
# keyfile  = 'certs/key.pem'
# ca-certs = '/etc/ca_bundle.crt'
