# Incident Runbook — Azure Linux Infrastructure

This runbook documents real incidents encountered during operation of this 
infrastructure, including detection, investigation, root cause, fix, and 
verification steps.

---

## Incident 1 — Nginx Service Down

### Symptoms
- Website returning no response
- HTTP requests timing out

### Detection
Running `healthcheck.sh` revealed:
❌ Nginx:  DOWN
✅ myapp:  RUNNING
❌ HTTP:   NOT RESPONDING (got 000)

### Investigation
**Step 1 — Check service status:**
```bash
sudo systemctl status nginx
```
Output showed: `Active: inactive (dead)` — clean stop, not a crash

**Step 2 — Check error logs:**
```bash
sudo tail -20 /var/log/nginx/error.log
```
Output showed: No errors, no crash dump, only normal notice entries

### Root Cause
Nginx was manually stopped or killed by an external process. The clean 
"Deactivated successfully" message confirmed it was not a crash or 
misconfiguration.

### Fix
```bash
sudo systemctl start nginx
```

### Verification
```bash
./healthcheck.sh
```
✅ Nginx:  RUNNING
✅ myapp:  RUNNING
✅ HTTP:   RESPONDING (200 OK)

### Recovery Time
Approximately 4 minutes from detection to resolution

### Prevention
- fail2ban protects against unauthorized SSH access
- `service_monitor.py` automatically restarts services if they go down
- Schedule `healthcheck.sh` via cron for continuous monitoring

---

## Incident 2 — Disk Space Critical

### Symptoms
- Disk usage alert firing
- System performance potentially degraded

### Detection
Running `disk_alert.sh` revealed:
⚠️  WARNING: Disk usage is above 80%!
Current disk usage: 86%

### Investigation
**Step 1 — Find what's consuming space:**
```bash
sudo du -sh /tmp/* | sort -rh | head -10
```
Output:
21G     /tmp/bigfile.tmp
2.1G    /tmp/bigfile2.tmp

### Root Cause
Large temporary files (23GB total) left uncleaned in `/tmp`. These files 
were not automatically removed, causing disk usage to spike from 10% to 86%.

### Fix
```bash
sudo rm /tmp/bigfile.tmp /tmp/bigfile2.tmp
```

### Verification
```bash
./disk_alert.sh
```
✅ Disk usage is healthy (threshold: 80%)
Current disk usage: 10%

### Recovery Time
Approximately 2 minutes from detection to resolution

### Prevention
- `cleanup.py` automatically removes `/tmp` files older than 7 days
- Schedule `disk_alert.sh` via cron to run every hour
- Schedule `cleanup.py` via cron to run weekly

---

## Monitoring Scripts Quick Reference

| Script | Command | Purpose |
|--------|---------|---------|
| Health Check | `./healthcheck.sh` | Check Nginx, Docker, HTTP |
| Disk Alert | `./disk_alert.sh` | Check disk usage |
| Service Monitor | `python3 service_monitor.py` | Check all services |
| Resource Monitor | `python3 resource_monitor.py` | CPU/memory/disk stats |
| Cleanup | `python3 cleanup.py` | Clean temp files and images |

---

## Recommended Cron Schedule

```bash
# Run health check every 5 minutes
*/5 * * * * /home/azureuser/scripts/healthcheck.sh >> /var/log/healthcheck.log 2>&1

# Run disk alert every hour
0 * * * * /home/azureuser/scripts/disk_alert.sh >> /var/log/disk_alert.log 2>&1

# Run cleanup every Sunday at 2am
0 2 * * 0 python3 /home/azureuser/scripts/cleanup.py >> /var/log/cleanup.log 2>&1
```
