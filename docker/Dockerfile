#!/bin/sh

FROM gitea/gitea:1

USER git

# RUN gitea admin user create --admin --username $ADMIN_USER --password $ADMIN_PASSWORD --email $ADMIN_EMAIL --must-change-password=false
RUN gitea admin user create --admin --username gitadmin --password password --email admin@example.com --must-change-password=false

USER root

EXPOSE	3000 22