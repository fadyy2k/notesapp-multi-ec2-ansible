# NotesApp – Multi EC2 Deployment with Ansible (AWS)

A production-style **Flask Notes Application** deployed on **AWS EC2** using **Ansible**, following DevOps best practices:
- Separate EC2 instances for **Application UI** and **Database API**
- Automated provisioning and configuration
- Backup strategy for SQLite database
- Nginx + Gunicorn setup
- Private networking between services

---

## 🏗 Architecture

Internet
|
v
[ Nginx ]
|
[ NotesApp UI (Flask + Gunicorn) ]
|
(private VPC traffic)
|
[ Notes DB API (Flask + Gunicorn + SQLite) ]

---

## 🧩 Components

### 1️⃣ Control Node
- Amazon Linux EC2
- Ansible installed
- Manages all deployments

### 2️⃣ App EC2 (UI)
- Flask frontend
- Gunicorn
- Nginx (reverse proxy)
- Communicates with DB API via private IP

### 3️⃣ DB EC2 (API)
- Flask REST API
- SQLite database
- Gunicorn
- Daily compressed backups via cron

---

## 📁 Repository Structure

notesapp-multi-ec2/
├── inventory/
│ ├── hosts.ini.example
├── roles/
│ ├── app_ui/
│ ├── db_api/
│ ├── db_backup/
├── playbook-app.yml
├── playbook-db.yml
├── playbook-db-backup.yml
├── ansible.cfg
└── README.md
---

## 🚀 Deployment Steps

### 1️⃣ Prepare inventory
```bash
cp inventory/hosts.ini.example inventory/hosts.ini
nano inventory/hosts.ini
Set:

DB private IP

App private IP

SSH key path

2️⃣ Deploy Database API
bash
Copy code
ansible-playbook playbook-db.yml
Verify:
curl http://DB_PRIVATE_IP:5000/health

3️⃣ Configure DB Backups
ansible-playbook playbook-db-backup.yml
Manual test:
sudo /usr/local/bin/notesdb-backup.sh

4️⃣ Deploy Application UI
ansible-playbook playbook-app.yml
Open in browser:
http://APP_PUBLIC_IP

🔁 API Endpoints (DB)
Method	Endpoint	Description
GET	/health	Health check
GET	/notes	List notes
POST	/notes	Add note
GET	/notes/<id>	Get note
PUT	/notes/<id>	Update note
DELETE	/notes/<id>	Delete note

💾 Backup Strategy
Daily cron backup at 08:00

Location: /var/backups/notesdb

Format: notesdb_YYYYMMDD_HHMMSS.db.gz

Retention: last 14 backups

🔐 Security Notes
DB API is accessed via private VPC IP

SSH access restricted via Security Groups

No database exposed publicly

Nginx terminates HTTP traffic

🧠 DevOps Concepts Demonstrated
Infrastructure automation (Ansible)

Multi-tier architecture

Service isolation

Systemd services

Backup & recovery

Reverse proxy

Zero-downtime restarts

📌 Future Improvements
HTTPS (ACM + ALB)

Authentication & users

Monitoring (Prometheus / CloudWatch)

CI/CD (GitHub Actions)

Database migration to RDS

👤 Author
Fady Mounir
