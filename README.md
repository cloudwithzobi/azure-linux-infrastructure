# Azure Linux Infrastructure

A production-style Linux server deployment on Azure, built entirely with Infrastructure as Code.
Built to simulate a production-ready Linux server with security hardening, automated monitoring, and CI/CD-driven infrastructure deployment.

## Architecture
```
User (Browser)
   ↓
Azure Public IP
   ↓
NSG (22, 80, 443)
   ↓
VM (Ubuntu)
   ↓
UFW Firewall
   ↓
Nginx (Reverse Proxy)
   ↓
Docker Container (App)
   ↓
Monitoring & Security
   - fail2ban
   - auditd
   - custom scripts

Internet → Azure NSG → UFW Firewall → Nginx → Docker → fail2ban → auditd
```

## What I Built

### Infrastructure (Terraform)
- Ubuntu 22.04 VM on Azure (Canada Central)
- Virtual Network with dedicated subnet (10.0.0.0/16)
- Network Security Group — ports 22, 80, 443
- Static public IP
- Full deployment via `terraform plan` and `terraform apply`

### Linux Hardening
- **UFW Firewall** — deny all incoming except SSH, HTTP, HTTPS
- **fail2ban** — automatic IP banning after 5 failed SSH attempts
- **auditd** — logging authentication events, user changes, sudo commands, 
  SSH config changes

### Nginx Reverse Proxy
- Nginx installed and configured as a reverse proxy
- Dockerized application running on internal port 8080
- Nginx forwards all port 80 traffic to the container
- Verified end-to-end traffic flow from browser to container

### Automation Scripts
| Script | Purpose |
|--------|---------|
| `healthcheck.sh` | Checks Nginx, Docker container, and HTTP response |
| `disk_alert.sh` | Alerts when disk usage exceeds 80% threshold |
| `log_rotation.sh` | Compresses logs older than 7 days, deletes after 30 |
| `service_monitor.py` | Monitors critical services, auto-restarts if down |
| `resource_monitor.py` | Reports CPU, memory, and disk usage |
| `cleanup.py` | Removes old temp files, logs, and unused Docker images |

### Configuration Management (Ansible)
- Ansible playbook configures server from local machine — no manual SSH required
- Installs essential packages, creates deploy user with sudo access
- Configures UFW rules, ensures fail2ban and auditd are running
- **Idempotent** — safe to run multiple times, corrects any configuration drift

### CI/CD Pipeline (GitHub Actions)
- Triggers automatically on every push to main branch
- Runs: `terraform init` → `fmt check` → `validate` → `plan`
- Azure authentication via Service Principal and GitHub Secrets
- No credentials stored in code

## Tech Stack
- **Cloud:** Microsoft Azure
- **IaC:** Terraform 1.14.8
- **OS:** Ubuntu 22.04 LTS
- **Web Server:** Nginx
- **Containers:** Docker
- **Automation:** Bash, Python 3
- **Config Management:** Ansible 2.16
- **CI/CD:** GitHub Actions
- **Security:** UFW, fail2ban, auditd

## Real Errors I Hit and Fixed

### 1. WSL Filesystem Permission Error
**Problem:** `terraform init` failed with `chmod: operation not permitted`  
**Root cause:** Terraform was running from `/mnt/c/` (Windows filesystem) 
which doesn't support Linux file permissions  
**Fix:** Moved project to WSL filesystem (`~/`) where permissions work correctly  
**Lesson:** Always run Terraform from the Linux filesystem in WSL, never from `/mnt/c/`

### 2. Azure VM SKU Capacity Error
**Problem:** `terraform apply` failed — `Standard_B1s` not available in Canada Central  
**Root cause:** Azure capacity constraints on older B-series VMs  
**Fix:** Queried available SKUs with `az vm list-skus`, switched to `Standard_B2als_v2`  
**Lesson:** Always verify SKU availability before assuming a VM size is available

### 3. Docker Port Mismatch
**Problem:** `curl http://localhost:3000` returned connection reset  
**Root cause:** Container was listening on port 8080, not 3000 as assumed  
**Fix:** Checked `docker logs myapp`, identified correct port, recreated container 
with `-p 3000:8080`  
**Lesson:** Always check container logs before assuming a port mapping is correct

### 4. CI/CD Pipeline Timeout
**Problem:** First pipeline run hung for 18 minutes waiting for input  
**Root cause:** `terraform.tfvars` excluded from Git — Terraform had no variable values  
**Fix:** Passed variables directly in the pipeline using `-var` flags  
**Lesson:** Never rely on local `.tfvars` files in CI/CD — pass variables explicitly

## Project Structure
├── .github/
│   └── workflows/
│       └── terraform.yml    # CI/CD pipeline
├── ansible/
│   ├── inventory.ini        # Server inventory
│   └── playbook.yml         # Configuration playbook
├── scripts/
│   ├── healthcheck.sh       # Service health monitoring
│   ├── disk_alert.sh        # Disk usage alerting
│   ├── log_rotation.sh      # Automated log cleanup
│   ├── service_monitor.py   # Service monitoring and auto-restart
│   ├── resource_monitor.py  # CPU/memory/disk reporting
│   └── cleanup.py           # System cleanup automation
├── main.tf                  # Azure infrastructure
├── variables.tf             # Input variables
├── outputs.tf               # Output values
└── .gitignore               # Excludes sensitive files

## How to Deploy

### Prerequisites
- Azure CLI installed and authenticated
- Terraform >= 1.0
- SSH key pair generated

### Deploy Infrastructure
```bash
terraform init
terraform plan -var="resource_group_name=rg-phase1-linux" \
               -var="vm_name=vm-phase1-ubuntu" \
               -var="ssh_public_key_path=~/.ssh/azure_phase1.pub" \
               -var="vm_size=Standard_B2als_v2"
terraform apply
```

### Configure Server
```bash
cd ansible
ansible-playbook -i inventory.ini playbook.yml
```

### Run Health Check
```bash
ssh -i ~/.ssh/azure_phase1 azureuser@<PUBLIC_IP>
cd ~/scripts && ./healthcheck.sh
```

## Incident Runbook
See [RUNBOOK.md](RUNBOOK.md) for documented incidents and resolution procedures.

## Author
**Zohaib Syed (Zobi)**  
Cloud Infrastructure Engineer | Calgary, AB  
[LinkedIn](https://linkedin.com/in/zohaibsyed365) | 
[GitHub](https://github.com/cloudwithzobi)
