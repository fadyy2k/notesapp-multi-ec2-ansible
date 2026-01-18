# NotesApp (Multi-EC2) — Ansible + AWS + Flask

![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?logo=ansible&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-232F3E?logo=amazonaws&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?logo=flask&logoColor=white)

A simple **Notes** application deployed on **two EC2 instances** using **Ansible**:

- **APP EC2**: Nginx → Gunicorn → Flask UI
- **DB EC2**: Gunicorn → Flask DB-API → SQLite
- Optional: automated **daily DB backups** on the DB instance via cron

---

## Architecture

> If you uploaded `architecture.png` to the repo root, this image will render automatically on GitHub.

![Architecture Diagram](architecture.png)

---

## What’s in this repo

```
notesapp-multi-ec2-ansible/
├─ ansible.cfg
├─ inventory/
│  └─ hosts.ini
├─ playbook-app.yml
├─ playbook-db.yml
├─ playbook-db-backup.yml
├─ roles/
│  ├─ app_ui/
│  ├─ db_api/
│  └─ db_backup/
├─ API_EXAMPLES.md
└─ architecture.png
```

---

## Prerequisites

- **AWS EC2**: 2 instances in the same VPC (recommended: same subnet or routable subnets)
  - **notesapp-app** (public access for users)
  - **notesapp-db** (private access recommended; reachable from app/control)
- **Security Groups (recommended)**:
  - APP SG:
    - Inbound: **80/tcp** from `0.0.0.0/0` (or your IP)
    - Inbound: **22/tcp** from your IP (admin)
  - DB SG:
    - Inbound: **22/tcp** from control node (or your IP / APP SG)
    - Inbound: **5000/tcp** **ONLY** from APP private IP / APP SG (recommended)
- **Control node** (where you run Ansible):
  - Amazon Linux / Linux host with:
    - `ansible`
    - `python3`
    - SSH access to both instances using the same key pair (or per-host keys configured)

---

## 1) Configure inventory

Edit `inventory/hosts.ini` to point to **private IPs** (recommended inside VPC):

```ini
[db]
notesapp-db ansible_host=<DB_PRIVATE_IP> ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/<KEY>.pem

[app]
notesapp-app ansible_host=<APP_PRIVATE_IP> ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/<KEY>.pem
```

Quick connectivity check:

```bash
ansible all -m ping
```

---

## 2) Deploy DB API (SQLite lives on the DB EC2)

```bash
ansible-playbook playbook-db.yml
```

Verify from control node (replace `<DB_PRIVATE_IP>` if needed):

```bash
curl -s http://<DB_PRIVATE_IP>:5000/health
curl -s http://<DB_PRIVATE_IP>:5000/notes | head
```

---

## 3) Deploy the App UI (public website)

```bash
ansible-playbook playbook-app.yml
```

Verify locally on the APP instance:

```bash
ansible app -b -m shell -a "curl -s -o /dev/null -w 'HTTP=%{http_code}\n' http://127.0.0.1:8000/health"
```

Verify via public IP (or DNS) from your machine:

```bash
curl -s -o /dev/null -w "HTTP=%{http_code}\n" http://<APP_PUBLIC_IP>/
curl -s http://<APP_PUBLIC_IP>/health
```

---

## 4) Configure DB backups (DB EC2)

This role installs **cronie**, creates a backup script, and schedules a daily cron job.

```bash
ansible-playbook playbook-db-backup.yml
```

Run a manual backup test:

```bash
ansible db -b -m shell -a "/usr/local/bin/notesdb-backup.sh && ls -lh /var/backups/notesdb | tail"
```

Defaults (can be overridden in `roles/db_backup/defaults/main.yml`):
- Backup dir: `/var/backups/notesdb`
- Keep: `14` backups
- Time: `08:00`

---

## API examples

See: **API_EXAMPLES.md**

- DB API endpoints: `/health`, `/notes`, `/notes/<id>`
- UI endpoints: `/`, `/health`, `/add`, `/delete/<id>`, `/api/note/<id>`

---

## Troubleshooting

### App returns `502 Bad Gateway`
Check the app service and logs:

```bash
ansible app -b -m shell -a "systemctl status notesapp --no-pager -l | sed -n '1,120p'"
ansible app -b -m shell -a "journalctl -u notesapp -n 120 --no-pager"
ansible app -b -m shell -a "systemctl status nginx --no-pager -l | sed -n '1,80p'"
```

### UI can’t reach DB API
From APP instance, test DB connectivity:

```bash
ansible app -b -m shell -a "curl -s http://<DB_PRIVATE_IP>:5000/health"
```

If it fails:
- Confirm DB SG inbound allows **5000/tcp** from APP
- Confirm DB service is running:
  ```bash
  ansible db -b -m shell -a "systemctl status notesdb --no-pager -l | sed -n '1,120p'"
  ```

---

## Suggested next improvements (optional)

- Put the **DB EC2 in a private subnet** with no public IP
- Add **HTTPS** on the APP EC2 (Let’s Encrypt via Certbot)
- Add monitoring (CloudWatch agent / Prometheus) and centralized logs
- Add basic rate limiting / WAF for public endpoint

---

## License

For training/lab use. Add a license if you plan to distribute publicly.
