#!/usr/bin/env python3

# Resource Monitor Script
# Reports CPU, memory, and disk usage

import psutil
import datetime

def main():
    print("===============================")
    print(f"  Resource Monitor - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("===============================")

    # CPU Usage
    cpu = psutil.cpu_percent(interval=1)
    if cpu > 80:
        print(f"⚠️  CPU:    {cpu}% (HIGH)")
    else:
        print(f"✅ CPU:    {cpu}%")

    # Memory Usage
    mem = psutil.virtual_memory()
    if mem.percent > 80:
        print(f"⚠️  Memory: {mem.percent}% used of {round(mem.total / (1024**3), 1)}GB (HIGH)")
    else:
        print(f"✅ Memory: {mem.percent}% used of {round(mem.total / (1024**3), 1)}GB")

    # Disk Usage
    disk = psutil.disk_usage('/')
    if disk.percent > 80:
        print(f"⚠️  Disk:   {disk.percent}% used of {round(disk.total / (1024**3), 1)}GB (HIGH)")
    else:
        print(f"✅ Disk:   {disk.percent}% used of {round(disk.total / (1024**3), 1)}GB")

    print("===============================")

if __name__ == "__main__":
    main()
