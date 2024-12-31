#!/bin/sh

# Substitute environment variables in our custom config, then write
# that configuration to Nginx configuration directory.
envsubst < /etc/nginx/conf.d/csb.conf.template > /etc/nginx/conf.d/csb.conf

# Execute nginx.
nginx -g 'daemon off;'