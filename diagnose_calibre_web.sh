#!/bin/bash

# Calibre-Web Disk I/O Diagnostic Script
# Run this script to diagnose the disk I/O error

echo "=== Calibre-Web Disk I/O Diagnostic ==="
echo "Date: $(date)"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Warning: Not running as root. Some checks may fail."
    echo ""
fi

# 1. Check disk space
echo "1. Checking disk space..."
echo "=========================="
df -h
echo ""

# 2. Check if Calibre-Web directory exists and its size
echo "2. Checking Calibre-Web directory..."
echo "===================================="
if [ -d "/app/calibre-web" ]; then
    echo "✅ Calibre-Web directory found at /app/calibre-web"
    du -sh /app/calibre-web/
    echo ""
    
    # Check for database files
    echo "3. Looking for database files..."
    echo "================================"
    find /app/calibre-web/ -name "*.db" -o -name "*.sqlite" -o -name "*.sqlite3" 2>/dev/null
    echo ""
    
    # Check database file permissions
    echo "4. Checking database file permissions..."
    echo "========================================"
    for db_file in $(find /app/calibre-web/ -name "*.db" -o -name "*.sqlite" -o -name "*.sqlite3" 2>/dev/null); do
        echo "File: $db_file"
        ls -la "$db_file"
        echo "Size: $(du -h "$db_file" | cut -f1)"
        echo ""
    done
    
    # Check log files
    echo "5. Checking log files..."
    echo "========================"
    if [ -d "/app/calibre-web/logs" ]; then
        ls -la /app/calibre-web/logs/
        echo ""
        echo "Log directory size:"
        du -sh /app/calibre-web/logs/
        echo ""
    else
        echo "❌ Log directory not found at /app/calibre-web/logs"
        echo ""
    fi
else
    echo "❌ Calibre-Web directory not found at /app/calibre-web"
    echo "Checking common alternative locations..."
    for alt_path in "/opt/calibre-web" "/var/lib/calibre-web" "/home/*/calibre-web"; do
        if [ -d "$alt_path" ]; then
            echo "✅ Found at: $alt_path"
            du -sh "$alt_path"
        fi
    done
    echo ""
fi

# 3. Check system I/O errors
echo "6. Checking system I/O errors..."
echo "================================"
dmesg | grep -i "i/o error" | tail -10
echo ""

# 4. Check for disk health issues
echo "7. Checking disk health..."
echo "=========================="
if command -v smartctl &> /dev/null; then
    for disk in /dev/sda /dev/sdb /dev/sdc; do
        if [ -b "$disk" ]; then
            echo "Checking $disk..."
            smartctl -H "$disk" 2>/dev/null | grep -E "(SMART|Health|Status)"
        fi
    done
else
    echo "⚠️  smartctl not available. Install smartmontools for disk health checks."
fi
echo ""

# 5. Check Docker status (if applicable)
echo "8. Checking Docker status..."
echo "============================"
if command -v docker &> /dev/null; then
    echo "Docker version:"
    docker --version
    echo ""
    echo "Docker disk usage:"
    docker system df 2>/dev/null || echo "❌ Cannot get Docker disk usage"
    echo ""
    echo "Running containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "❌ Cannot list containers"
else
    echo "ℹ️  Docker not installed or not in PATH"
fi
echo ""

# 6. Check system resources
echo "9. Checking system resources..."
echo "==============================="
echo "Memory usage:"
free -h
echo ""
echo "CPU load:"
uptime
echo ""
echo "Disk I/O (if iostat available):"
if command -v iostat &> /dev/null; then
    iostat -x 1 1
else
    echo "⚠️  iostat not available. Install sysstat for I/O monitoring."
fi
echo ""

# 7. Check for large files that might be causing issues
echo "10. Checking for large files..."
echo "================================"
echo "Files larger than 100MB in /app/calibre-web (if exists):"
if [ -d "/app/calibre-web" ]; then
    find /app/calibre-web/ -type f -size +100M -exec ls -lh {} \; 2>/dev/null | head -10
else
    echo "❌ Calibre-Web directory not found"
fi
echo ""

# 8. Check file system errors
echo "11. Checking file system errors..."
echo "=================================="
echo "Recent system errors:"
journalctl --since "1 hour ago" | grep -i "error\|fail\|corrupt" | tail -10
echo ""

# 9. Recommendations
echo "12. Recommendations..."
echo "====================="
echo "Based on the above checks, here are the most likely solutions:"
echo ""
echo "🔧 IMMEDIATE ACTIONS:"
echo "1. If disk space is low (< 10% free):"
echo "   - Clean up unnecessary files"
echo "   - Remove old log files"
echo "   - Consider moving large files to external storage"
echo ""
echo "2. If database files are corrupted:"
echo "   - Stop Calibre-Web service"
echo "   - Backup current database files"
echo "   - Try database repair with: sqlite3 app.db 'VACUUM; REINDEX;'"
echo "   - Restore from backup if repair fails"
echo ""
echo "3. If Docker storage is full:"
echo "   - Run: docker system prune -a"
echo "   - Consider rebuilding the container"
echo ""
echo "4. If hardware issues detected:"
echo "   - Check disk health with smartctl"
echo "   - Consider replacing failing hardware"
echo "   - Run file system check: fsck"
echo ""
echo "📋 PREVENTION:"
echo "- Set up regular database backups"
echo "- Monitor disk space usage"
echo "- Implement log rotation"
echo "- Use monitoring tools for early detection"
echo ""

echo "=== Diagnostic Complete ==="
echo "For more detailed help, refer to the calibre-web-disk-io-fix.md file"