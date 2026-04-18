#!/usr/bin/env python3

# Cleanup Script
# Removes old temp files, old logs, and unused Docker images

import os
import subprocess
import datetime

def get_folder_size(path):
    result = subprocess.run(
        ["du", "-sh", path],
        capture_output=True,
        text=True
    )
    return result.stdout.split()[0] if result.stdout else "unknown"

def cleanup_tmp_files():
    print("Cleaning /tmp files older than 7 days...")
    result = subprocess.run(
        ["sudo", "find", "/tmp", "-type", "f", "-mtime", "+7", "-delete"],
        capture_output=True,
        text=True
    )
    print("✅ /tmp cleanup complete")

def cleanup_old_logs():
    print("Cleaning log files older than 30 days...")
    result = subprocess.run(
        ["sudo", "find", "/var/log", "-type", "f", "-name", "*.gz", "-mtime", "+30", "-delete"],
        capture_output=True,
        text=True
    )
    print("✅ Old log cleanup complete")

def cleanup_docker():
    print("Pruning unused Docker images...")
    result = subprocess.run(
        ["sudo", "docker", "image", "prune", "-f"],
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(f"  {result.stdout.strip()}")
    print("✅ Docker cleanup complete")

def main():
    print("===============================")
    print(f"  Cleanup Script - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("===============================")

    disk_before = get_folder_size("/")
    print(f"Disk usage before: {disk_before}")
    print("")

    cleanup_tmp_files()
    cleanup_old_logs()
    cleanup_docker()

    print("")
    disk_after = get_folder_size("/")
    print(f"Disk usage after:  {disk_after}")
    print("===============================")

if __name__ == "__main__":
    main()
