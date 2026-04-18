#!/usr/bin/env python3

# Service Monitor Script
# Checks if critical services are running and restarts them if down

import subprocess
import datetime

SERVICES = ["nginx", "docker", "fail2ban", "auditd"]

def check_service(service):
    result = subprocess.run(
        ["systemctl", "is-active", service],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() == "active"

def restart_service(service):
    subprocess.run(["sudo", "systemctl", "restart", service])

def main():
    print("===============================")
    print(f"  Service Monitor - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("===============================")

    for service in SERVICES:
        if check_service(service):
            print(f"✅ {service}: RUNNING")
        else:
            print(f"❌ {service}: DOWN — attempting restart...")
            restart_service(service)
            if check_service(service):
                print(f"✅ {service}: RESTARTED successfully")
            else:
                print(f"🚨 {service}: FAILED to restart — manual intervention needed")

    print("===============================")

if __name__ == "__main__":
    main()
