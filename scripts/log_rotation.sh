#!/bin/bash

# Log Rotation Script
# Compresses logs older than 7 days and deletes logs older than 30 days

LOG_DIR="/var/log"
ARCHIVE_DIR="/var/log/archive"
MAX_AGE_DELETE=30
MAX_AGE_COMPRESS=7

echo "==============================="
echo "  Log Rotation - $(date)"
echo "==============================="

# Create archive directory if it doesn't exist
sudo mkdir -p $ARCHIVE_DIR

# Compress logs older than 7 days
echo "Compressing logs older than ${MAX_AGE_COMPRESS} days..."
COMPRESSED=0
sudo find $LOG_DIR -maxdepth 1 -name "*.log" -mtime +$MAX_AGE_COMPRESS ! -name "*.gz" | while read file; do
    sudo gzip "$file"
    COMPRESSED=$((COMPRESSED + 1))
    echo "  Compressed: $file"
done

# Delete compressed logs older than 30 days
echo "Deleting logs older than ${MAX_AGE_DELETE} days..."
sudo find $LOG_DIR -name "*.gz" -mtime +$MAX_AGE_DELETE -exec rm {} \;

echo "✅ Log rotation complete"
echo "==============================="
