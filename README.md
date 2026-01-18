# NotesApp – Multi-EC2 Deployment with Ansible on AWS

A production-ready **Notes Application** deployed on AWS using **Ansible**, demonstrating a clean **multi-tier architecture** with separate EC2 instances for the **UI** and **Database API**, automated backups, and a modern Flask + Nginx stack.

This project is designed as a **DevOps / Cloud engineering showcase**, focusing on automation, separation of concerns, and operational best practices.

---

## 🧠 Project Overview

**NotesApp** allows users to create, edit, and delete notes through a web interface.  
Behind the scenes, the system is split into multiple layers:

- **App EC2**: Flask UI + Gunicorn + Nginx  
- **DB EC2**: Flask REST API + SQLite  
- **Automation**: Ansible roles & playbooks  
- **Backups**: Automated SQLite backups with retention

No manual server configuration is required after provisioning.

---

## 🏗️ Architecture

User Browser  
→ Nginx (App EC2)  
→ Flask UI (Gunicorn)  
→ Flask DB API (DB EC2)  
→ SQLite Database  
→ Automated Backups

---

## ⚙️ Tech Stack

- AWS EC2 (Amazon Linux 2023)
- Ansible
- Flask
- Gunicorn
- Nginx
- SQLite
- Systemd
- Cron

---

## 📁 Repository Structure

```
notesapp-multi-ec2-ansible/
├── inventory/
├── roles/
│   ├── app_ui/
│   ├── db_api/
│   └── db_backup/
├── playbook-app.yml
├── playbook-db.yml
├── playbook-db-backup.yml
└── ansible.cfg
```

---

## 🚀 Deployment Steps

### 1. Clone Repository

```bash
git clone https://github.com/fadyy2k/notesapp-multi-ec2-ansible.git
cd notesapp-multi-ec2-ansible
```

### 2. Configure Inventory

Edit `inventory/hosts.ini` with your EC2 private IPs.

### 3. Deploy Database API

```bash
ansible-playbook playbook-db.yml
```

### 4. Configure Backups

```bash
ansible-playbook playbook-db-backup.yml
```

### 5. Deploy App UI

```bash
ansible-playbook playbook-app.yml
```

Open the app in your browser using the App EC2 public IP.

---

## 🔌 API Endpoints

- `GET /health`
- `GET /notes`
- `POST /notes`
- `PUT /notes/<id>`
- `DELETE /notes/<id>`

---

## 💾 Backup Strategy

- Daily SQLite backup
- Gzip compression
- 14-day retention
- Stored under `/var/backups/notesdb`

---

## 🔐 Security Notes

- DB API accessible only via private IP
- UI is the only public-facing service
- SSH key-based authentication
- No shared storage

---

## 📌 Future Improvements

- HTTPS (Let’s Encrypt)
- CI/CD with GitHub Actions
- Authentication
- RDS migration
- Terraform provisioning

---

## 👤 Author

**Fady Mounir**  
GitHub: https://github.com/fadyy2k

---

## 📄 License

MIT License
