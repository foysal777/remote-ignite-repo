#!/bin/bash

# ================= CONFIG =================
PROJECT_DIR="/usr/bin/var/www/ignite-backend"
BRANCH="main"
LOG_FILE="/var/log/ignite-auto-deploy.log"
# ==========================================

echo "----------------------------------------" >> $LOG_FILE
echo "$(date) : Checking branch '$BRANCH' for updates" >> $LOG_FILE

cd $PROJECT_DIR || exit 1

# Ensure correct branch
git checkout $BRANCH >> $LOG_FILE 2>&1

# Fetch updates
git fetch origin $BRANCH >> $LOG_FILE 2>&1

LOCAL_HASH=$(git rev-parse $BRANCH)
REMOTE_HASH=$(git rev-parse origin/$BRANCH)

if [ "$LOCAL_HASH" != "$REMOTE_HASH" ]; then
    echo "$(date) : Changes detected. Deploying..." >> $LOG_FILE

    git pull origin $BRANCH >> $LOG_FILE 2>&1

    docker compose down >> $LOG_FILE 2>&1
    docker compose up -d --build >> $LOG_FILE 2>&1

    docker exec ignite-backend python manage.py collectstatic --noinput >> $LOG_FILE 2>&1
    docker exec ignite-backend python manage.py migrate >> $LOG_FILE 2>&1

    echo "$(date) : Deployment successful." >> $LOG_FILE
else
    echo "$(date) : No changes found." >> $LOG_FILE
fi

