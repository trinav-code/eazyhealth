#!/bin/bash
# Setup script for EazyHealth automated briefing generation

echo "Setting up EazyHealth automated briefing generation..."
echo ""

# Create the cron job entry
CRON_JOB="0 12 * * * cd /Users/trinav/personal/eazyhealth/backend && /usr/bin/python3 scheduler.py >> /tmp/eazyhealth-scheduler.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "eazyhealth-scheduler"; then
    echo "⚠️  Cron job already exists!"
    echo "Current cron jobs:"
    crontab -l | grep eazyhealth
    echo ""
    read -p "Do you want to replace it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
    # Remove old cron job
    crontab -l | grep -v eazyhealth-scheduler | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job installed successfully!"
echo ""
echo "Schedule: Every day at 12:00 PM"
echo "Log file: /tmp/eazyhealth-scheduler.log"
echo ""
echo "To view your cron jobs:"
echo "  crontab -l"
echo ""
echo "To view scheduler logs:"
echo "  tail -f /tmp/eazyhealth-scheduler.log"
echo ""
echo "To remove the cron job:"
echo "  crontab -e"
echo "  (then delete the eazyhealth-scheduler line)"
echo ""
echo "⚠️  IMPORTANT: Make sure your backend server is running at localhost:8000"
echo "   when the scheduler runs (12 PM daily)"
echo ""
