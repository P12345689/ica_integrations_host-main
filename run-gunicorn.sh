#!/bin/bash
# Author: Mihai Criveti <crmihai1@ie.ibm.com>
# Description: Run gunicorn production server

cat << EOF
▜▘▛▀▖▙▗▌ ▞▀▖▞▀▖▙ ▌▞▀▖▌ ▌▌ ▀▛▘▜▘▙ ▌▞▀▖
▐ ▙▄▘▌▘▌ ▌  ▌ ▌▌▌▌▚▄ ▌ ▌▌  ▌ ▐ ▌▌▌▌▄▖
▐ ▌ ▌▌ ▌ ▌ ▖▌ ▌▌▝▌▖ ▌▌ ▌▌  ▌ ▐ ▌▝▌▌ ▌
▀▘▀▀ ▘ ▘ ▝▀ ▝▀ ▘ ▘▝▀ ▝▀ ▀▀▘▘ ▀▘▘ ▘▝▀

▜▘▙ ▌▀▛▘▛▀▘▞▀▖▛▀▖▞▀▖▀▛▘▜▘▞▀▖▙ ▌▞▀▖
▐ ▌▌▌ ▌ ▙▄ ▌▄▖▙▄▘▙▄▌ ▌ ▐ ▌ ▌▌▌▌▚▄
▐ ▌▝▌ ▌ ▌  ▌ ▌▌▚ ▌ ▌ ▌ ▐ ▌ ▌▌▝▌▖ ▌
▀▘▘ ▘ ▘ ▀▀▘▝▀ ▘ ▘▘ ▘ ▘ ▀▘▝▀ ▘ ▘▝▀
EOF

GUNICORN_WORKERS=${GUNICORN_WORKERS:-8}
GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-120}

gunicorn -c gunicorn.config.py \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers ${GUNICORN_WORKERS} \
    --timeout ${GUNICORN_TIMEOUT} \
    --access-logfile - \
    --error-logfile - \
    'app.server:app'
