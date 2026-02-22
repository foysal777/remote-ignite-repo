#!/bin/bash

# ================= CONFIG =================
PROJECT_DIR="/usr/bin/var/www/ignite-backend"
BRANCH="main"
LOG_FILE="/usr/bin/var/www/ignite-backend.log"
# ==========================================

echo "----------------------------------------" >> "$LOG_FILE"
echo "$(date) : Checking branch '$BRANCH' for updates" >> "$LOG_FILE"

cd "$PROJECT_DIR" || exit 1

git checkout "$BRANCH" >> "$LOG_FILE" 2>&1
git fetch origin "$BRANCH" >> "$LOG_FILE" 2>&1

LOCAL_HASH=$(git rev-parse "$BRANCH")
REMOTE_HASH=$(git rev-parse "origin/$BRANCH")

if [ "$LOCAL_HASH" != "$REMOTE_HASH" ]; then
    echo "$(date) : Changes detected. Deploying..." >> "$LOG_FILE"

    git pull origin "$BRANCH" >> "$LOG_FILE" 2>&1

    docker compose down >> "$LOG_FILE" 2>&1
    docker compose up -d --build >> "$LOG_FILE" 2>&1

    # ================= DISK CHECK & DOCKER PRUNE =================
    DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

    echo "$(date) : Disk usage is ${DISK_USAGE}%" >> "$LOG_FILE"

    if [ "$DISK_USAGE" -ge 70 ]; then
        echo "$(date) : Disk usage >= 70%. Running docker prune..." >> "$LOG_FILE"
        docker system prune -f --volumes >> "$LOG_FILE" 2>&1
    else
        echo "$(date) : Disk usage below 70%. Skipping docker prune." >> "$LOG_FILE"
    fi
    # =============================================================

    docker exec ignite-backend python manage.py collectstatic --noinput >> "$LOG_FILE" 2>&1
    docker exec ignite-backend python manage.py migrate >> "$LOG_FILE" 2>&1

    echo "$(date) : Deployment successful." >> "$LOG_FILE"
else
    echo "$(date) : No changes found." >> "$LOG_FILE"
fi

