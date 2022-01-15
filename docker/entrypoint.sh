#!/bin/bash

# ATTEMPT=0
# MAX_ATTEMPT=20
# while true; do
#     sleep 1
#     ATTEMPT=$(($ATTEMPT + 1))
#     STATUS_CODE=$(curl -LI localhost:3000 -o /dev/null -w '%{http_code}\n' -s)
#     if [ $STATUS_CODE = "200" ]; then
#         echo "Gitea is ready"
#         echo "Create Gitea admin"
#         gitea admin user --admin create --username $ADMIN_USER --password $ADMIN_PASSWORD --email $ADMIN_EMAIL --must-change-password=false
#         exit 0
#     elif [ $ATTEMPT = $MAX_ATTEMPT ]; then
#         exit 1
#     fi;
# done & /usr/bin/entrypoint