# Calibre-Web Disk I/O Error Fix Guide

## Problem Summary
Calibre-Web is experiencing a critical SQLite disk I/O error that prevents the application from starting properly.

## Error Details
- **Primary Error**: `sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) disk I/O error`
- **Affected Component**: User database query in `/app/calibre-web/cps/ub.py`
- **Secondary Issues**: Logging system failures due to disk I/O problems

## Step-by-Step Troubleshooting

### 1. Check Disk Space
```bash
# Check available disk space
df -h

# Check disk usage in the Calibre-Web directory
du -sh /app/calibre-web/

# Check for large files that might be consuming space
find /app/calibre-web/ -type f -size +100M -exec ls -lh {} \;
```

### 2. Check Database File Integrity
```bash
# Navigate to Calibre-Web directory
cd /app/calibre-web/

# Find the database file (usually app.db or similar)
find . -name "*.db" -o -name "*.sqlite" -o -name "*.sqlite3"

# Check database file permissions
ls -la *.db

# Verify database integrity (if sqlite3 is available)
sqlite3 app.db "PRAGMA integrity_check;"
```

### 3. Check File System Health
```bash
# Check file system for errors
dmesg | grep -i error

# Check for disk health (if smartctl is available)
smartctl -a /dev/sda  # Replace with your disk device

# Check for I/O errors in system logs
journalctl -f | grep -i "i/o error"
```

### 4. Database Recovery Steps

#### Option A: Backup and Recreate Database
```bash
# Create backup of current database
cp app.db app.db.backup.$(date +%Y%m%d_%H%M%S)

# Try to repair the database
sqlite3 app.db.backup "VACUUM;"
sqlite3 app.db.backup "REINDEX;"

# If repair fails, you may need to recreate from backup
```

#### Option B: Reset User Database (if you have backups)
```bash
# Stop Calibre-Web
docker stop calibre-web  # or however you stop the service

# Backup current database
cp /path/to/calibre-web/app.db /path/to/backup/

# Restore from a known good backup
cp /path/to/backup/good_app.db /path/to/calibre-web/app.db

# Restart Calibre-Web
docker start calibre-web
```

### 5. Fix Logging Issues
The logging errors indicate the log files are also affected by disk I/O issues:

```bash
# Check log file permissions and space
ls -la /app/calibre-web/logs/
du -sh /app/calibre-web/logs/

# Clear or rotate log files if they're too large
find /app/calibre-web/logs/ -name "*.log" -size +100M -exec truncate -s 0 {} \;

# Or move old logs
find /app/calibre-web/logs/ -name "*.log.*" -mtime +7 -delete
```

### 6. Docker-Specific Solutions (if using Docker)

#### Check Docker Storage
```bash
# Check Docker disk usage
docker system df

# Clean up Docker resources
docker system prune -a

# Check if Docker storage driver is causing issues
docker info | grep "Storage Driver"
```

#### Rebuild Container
```bash
# Stop and remove the container
docker stop calibre-web
docker rm calibre-web

# Rebuild with fresh volumes
docker run -d \
  --name calibre-web \
  -v /path/to/books:/books \
  -v /path/to/config:/config \
  -p 8083:8083 \
  linuxserver/calibre-web
```

### 7. System-Level Solutions

#### Check for Hardware Issues
```bash
# Monitor disk I/O
iostat -x 1

# Check for disk errors
dmesg | grep -i "ata\|sata\|scsi"

# Monitor system resources
htop
```

#### File System Repair
```bash
# Unmount the affected filesystem (if possible)
umount /dev/sda1  # Replace with your device

# Run file system check
fsck /dev/sda1

# Remount
mount /dev/sda1 /mount/point
```

## Prevention Measures

### 1. Regular Backups
```bash
# Create automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /app/calibre-web/app.db /backup/calibre-web_$DATE.db
find /backup/ -name "calibre-web_*.db" -mtime +30 -delete
```

### 2. Disk Space Monitoring
```bash
# Add to crontab for regular monitoring
0 */6 * * * df -h | awk '$5 > "80%" {print "Disk space warning: " $0}' | mail -s "Disk Alert" admin@example.com
```

### 3. Database Maintenance
```bash
# Regular database optimization
sqlite3 /app/calibre-web/app.db "VACUUM; ANALYZE;"
```

## Emergency Recovery

If the database is completely corrupted and you have no backups:

1. **Stop the service immediately**
2. **Check for any auto-backups in the Calibre-Web directory**
3. **Look for backup files with extensions like .bak, .backup, .old**
4. **If no backups exist, you may need to reinstall and reconfigure Calibre-Web**

## Contact Information

If you need additional help:
- Check Calibre-Web GitHub issues: https://github.com/janeczku/calibre-web/issues
- Review system logs: `journalctl -u calibre-web -f`
- Monitor disk health regularly

## Notes

- Always backup your database before attempting repairs
- Consider using a more robust database like PostgreSQL for production environments
- Implement regular monitoring and alerting for disk space and I/O errors
- Keep multiple backups in different locations