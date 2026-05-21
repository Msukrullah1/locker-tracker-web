# 🐬 AWS RDS MySQL Setup - Complete Guide (हिंदी में)

## क्यों MySQL? 

```
✅ AWS पर FREE TIER में available
✅ हल्का (lighter than PostgreSQL)
✅ बहुत popular और reliable
✅ Easy setup
✅ Perfect for 5-10 users
✅ कम memory use करता है
```

---

## ✅ Step 1: AWS RDS MySQL Instance बनाओ

### 1.1 RDS Dashboard खोलो

```
1. https://console.aws.amazon.com खोलो
2. Login करो
3. Search bar में "RDS" type करो
4. "RDS" पर click करो
5. Left sidebar में "Databases" खोलो
6. "Create database" button पर click करो
```

### 1.2 Database Creation Method

```
┌─────────────────────────────────────┐
│ ○ Standard create                   │  ← Select करो
│ ○ Easy create                       │
└─────────────────────────────────────┘
```

### 1.3 Engine Options Select करो

```
Engine type:
┌─────────────────────────────────────┐
│ ○ Amazon Aurora                     │
│ ○ MySQL                             │  ← ✅ Select करो!
│ ○ MariaDB                           │
│ ○ PostgreSQL                        │
│ ○ Oracle                            │
│ ○ Microsoft SQL Server              │
└─────────────────────────────────────┘

Engine version:
┌─────────────────────────────────────┐
│ MySQL 8.0.35 (latest)               │  ← Select करो
└─────────────────────────────────────┘
```

### 1.4 Templates

```
┌─────────────────────────────────────┐
│ ○ Production                        │
│ ○ Dev/Test                          │
│ ○ Free tier                         │  ← ✅ Select करो (FREE!)
└─────────────────────────────────────┘

⚠️ Important: "Free tier" select करना मत भूलना!
```

### 1.5 Settings

```
DB instance identifier:
┌─────────────────────────────────────┐
│ locker-tracker-mysql                │  (कोई भी नाम)
└─────────────────────────────────────┘

Credentials Settings:
┌─────────────────────────────────────┐
│ Master username: admin              │  (default: admin)
│                                       │
│ Master password:                     │
│ ✅ Auto generate password            │
│ या manually set करो                  │
│                                       │
│ Strong password (8+ characters):     │
│ Example: MyP@ssw0rd123               │
└─────────────────────────────────────┘
```

**⚠️ IMPORTANT: Password कहीं note कर लो!**

### 1.6 Instance Configuration

```
DB instance class:
┌─────────────────────────────────────┐
│ db.t3.micro                         │  ← ✅ FREE TIER
│ (2 vCPUs, 1 GB RAM)                 │
└─────────────────────────────────────┘
```

### 1.7 Storage

```
Storage type: General Purpose SSD (gp2)
Allocated storage: 20 GB              ← FREE TIER
Maximum storage: 20 GB
Storage autoscaling: ❌ DISABLED      ← Free tier में disable रखो
```

### 1.8 Connectivity

```
Virtual private cloud (VPC):
└─ Default VPC                        ← Select करो

Subnet group:
└─ default                            ← Select करो

Public access:
└─ ✅ YES                             ← IMPORTANT! ON करो
   (EC2 से connect करने के लिए जरूरी)

VPC security group:
└─ Create new
   Name: locker-mysql-sg

Availability Zone:
└─ No preference

Database port:
└─ 3306                               ← MySQL default port
```

### 1.9 Additional Configuration

```
Initial database name:
┌─────────────────────────────────────┐
│ locker_tracker                      │  ← ✅ ENTER करो!
└─────────────────────────────────────┘

⚠️ यह जरूरी है! Otherwise database नहीं बनेगा

Backup:
└─ Backup retention period: 7 days   (free tier में free)
└─ Backup window: No preference

Encryption:
└─ Encryption: ❌ Disabled            (free tier में)

Performance Insights:
└─ ❌ Disabled                        (free tier में disable रखो)

Monitoring:
└─ Enhanced monitoring: ❌ Disabled

Maintenance:
└─ Auto minor version upgrade: ✅
└─ Maintenance window: No preference

Deletion protection:
└─ ❌ Disabled                        (testing के लिए)
```

### 1.10 Create Database

```
सब check करो:
☐ MySQL 8.0
☐ Free tier
☐ db.t3.micro
☐ 20 GB storage
☐ Public access: YES
☐ Database name: locker_tracker
☐ Password noted

✅ "Create database" button click करो

⏳ Wait करो 5-10 minutes...
✅ Status: "Available" तक wait करो
```

---

## ✅ Step 2: Database Endpoint लो

### Database Ready है!

```
RDS Dashboard में अपनी database खोलो

Connectivity & security tab में देखो:
┌─────────────────────────────────────────────┐
│ Endpoint:                                    │
│ locker-tracker-mysql.xxxxxxxxxxx.            │
│ ap-south-1.rds.amazonaws.com                 │
│                                              │
│ Port: 3306                                   │
│ Username: admin                              │
│ Password: (जो set किया था)                   │
│ Database: locker_tracker                     │
└─────────────────────────────────────────────┘
```

**यह सब Copy करके कहीं save कर लो! 📝**

---

## ✅ Step 3: Security Group Configure करो

### Inbound Rules Add करो

```
1. RDS Database खोलो
2. "Connectivity & security" tab में जाओ
3. "Security" section में security group पर click करो
4. "Inbound rules" tab खोलो
5. "Edit inbound rules" click करो
```

### Rules Add करो

```
┌─────────────────────────────────────────────┐
│ Type: MYSQL/Aurora                          │
│ Protocol: TCP                               │
│ Port: 3306                                  │
│ Source: 0.0.0.0/0 (सभी IPs से)             │
│                                              │
│ या Better: EC2 की security group select करो │
└─────────────────────────────────────────────┘

✅ "Save rules" click करो
```

**Security Tip:** Production में 0.0.0.0/0 की जगह specific IPs use करो।

---

## ✅ Step 4: EC2 से MySQL Test करो

### MySQL Client Install करो

```bash
# EC2 के SSH में जाओ

# MySQL client install करो
sudo apt update
sudo apt install -y mysql-client

# Version check करो
mysql --version
```

### Database से Connect करो

```bash
# RDS से connect करो
mysql -h locker-tracker-mysql.xxxxxxxxxxx.ap-south-1.rds.amazonaws.com \
      -u admin \
      -p

# Password पूछेगा - enter करो

# अगर successful:
# mysql>

# Test commands:
mysql> SHOW DATABASES;

# Output:
# +--------------------+
# | Database           |
# +--------------------+
# | information_schema |
# | locker_tracker     |  ← आपकी database!
# | mysql              |
# | performance_schema |
# | sys                |
# +--------------------+

# Database use करो
mysql> USE locker_tracker;

# Database empty है अभी
mysql> SHOW TABLES;

# Output: Empty set

# Exit
mysql> exit;
```

**✅ Connection successful!**

---

## ✅ Step 5: Flask App MySQL के साथ Deploy करो

### Project में MySQL files copy करो

```bash
# EC2 में:
cd ~/locker-tracker-web

# Old version backup
cp app.py app_old.py 2>/dev/null

# MySQL version use करो
cp app_mysql.py app.py

# MySQL requirements install करो
pip install -r requirements-mysql.txt

# अगर errors आए तो:
sudo apt install -y python3-dev default-libmysqlclient-dev build-essential
pip install -r requirements-mysql.txt
```

---

## ✅ Step 6: Environment Variables Set करो

### .env File बनाओ

```bash
# EC2 में:
nano ~/.env
```

**Content** (अपने details डालो):

```env
# Flask Configuration
ENVIRONMENT=production
SECRET_KEY=your-super-secret-key-change-this-12345

# AWS RDS MySQL Configuration
DB_USER=admin
DB_PASSWORD=your-mysql-password-here
DB_HOST=locker-tracker-mysql.xxxxxxxxxxx.ap-south-1.rds.amazonaws.com
DB_PORT=3306
DB_NAME=locker_tracker

# Logging
LOG_LEVEL=INFO
```

**Save करो:** `Ctrl+X` → `Y` → `Enter`

---

## ✅ Step 7: Systemd Service Update करो

```bash
sudo nano /etc/systemd/system/locker-tracker.service
```

**Update करो:**

```ini
[Unit]
Description=Locker Tracker Flask App (MySQL)
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/locker-tracker-web
Environment="PATH=/home/ubuntu/locker-tracker-web/venv/bin"

# Environment variables load करो
EnvironmentFile=/home/ubuntu/.env

ExecStart=/home/ubuntu/locker-tracker-web/venv/bin/gunicorn \
          -w 4 -b 127.0.0.1:5000 app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Save करो:** `Ctrl+X` → `Y` → `Enter`

### Reload और restart करो

```bash
sudo systemctl daemon-reload
sudo systemctl restart locker-tracker
sudo systemctl status locker-tracker

# Output: "active (running)" दिखना चाहिए
```

---

## ✅ Step 8: Database Tables Create करो

### App पहली बार run होने पर automatic create होगा

```bash
# Logs देखो
sudo journalctl -u locker-tracker -f

# Output में देखना चाहिए:
# ✅ MySQL database tables created successfully
# ✅ Default users created
# ✅ Sample floors created
# ✅ Sample departments created
# ✅ Database initialization complete!

# Ctrl+C से exit करो
```

### Manually verify करो

```bash
# MySQL में login करो
mysql -h your-rds-endpoint -u admin -p

mysql> USE locker_tracker;
mysql> SHOW TABLES;

# Output:
# +---------------------------+
# | Tables_in_locker_tracker  |
# +---------------------------+
# | tbl_audit_logs            |
# | tbl_departments           |
# | tbl_employees             |
# | tbl_floors                |
# | tbl_locker_history        |
# | tbl_lockers               |
# | tbl_users                 |
# +---------------------------+

# Users check करो
mysql> SELECT user_id, user_name, user_role FROM tbl_users;

# Output:
# +-------------+----------------------+------------+
# | user_id     | user_name            | user_role  |
# +-------------+----------------------+------------+
# | superadmin  | Super Administrator  | SuperAdmin |
# | admin01     | Rajesh Kumar         | Admin      |
# | oper01      | Amit Singh           | Operator   |
# | viewer01    | Guest User           | Viewer     |
# +-------------+----------------------+------------+

mysql> exit;
```

---

## ✅ Step 9: Website Test करो

### Browser में खोलो

```
http://your-ec2-public-ip

Login:
User ID: superadmin
Password: Admin@123
```

**🎉 MySQL पर live है!**

---

## ✅ Step 10: Team को Link दो

```
सभी को share करो:

👉 http://54.123.45.67 (या आपका EC2 IP)

Login credentials:
├─ superadmin / Admin@123 (Full access)
├─ admin01 / Admin@123 (Most features)
├─ oper01 / Oper@123 (Assign/Release only)
└─ viewer01 / View@123 (View only)
```

---

## 🔄 Common MySQL Commands

### Database में Connect करो

```bash
mysql -h endpoint -u admin -p
```

### Basic Commands

```sql
-- Databases देखो
SHOW DATABASES;

-- Database select करो
USE locker_tracker;

-- Tables देखो
SHOW TABLES;

-- Table structure देखो
DESCRIBE tbl_users;

-- Data देखो
SELECT * FROM tbl_users;

-- Count करो
SELECT COUNT(*) FROM tbl_lockers;

-- Filter करो
SELECT * FROM tbl_lockers WHERE status = 'Assigned';

-- Exit करो
exit;
```

### User Add करो (MySQL में)

```sql
USE locker_tracker;

-- New user add करो (password hashed होना चाहिए)
INSERT INTO tbl_users (user_id, user_name, password, user_role, is_active)
VALUES ('newuser', 'New User Name', 'hashed_password_here', 'Operator', 1);
```

**Note:** Password app के through ही add करो (because hashing करनी पड़ेगी)।

---

## 💾 Backup & Restore (MySQL)

### Manual Backup (mysqldump)

```bash
# EC2 में:

# Backup लो
mysqldump -h endpoint -u admin -p locker_tracker > backup_$(date +%Y%m%d).sql

# Password पूछेगा - enter करो

# File देखो
ls -la backup_*.sql
```

### Restore करना

```bash
# Restore करो
mysql -h endpoint -u admin -p locker_tracker < backup_20240115.sql

# Done!
```

### Automatic Backups (RDS)

```
RDS automatically:
├─ Daily backups
├─ 7 days retention
├─ Point-in-time recovery
└─ No manual work needed
```

### Manual Snapshot

```
1. RDS Database खोलो
2. Actions → "Take snapshot"
3. Name: locker-mysql-backup-20240115
4. Create snapshot
```

---

## 🔐 Security Best Practices

### 1. Strong Password लगाओ

```sql
-- MySQL में login करो
mysql -h endpoint -u admin -p

-- Password change करो
ALTER USER 'admin'@'%' IDENTIFIED BY 'new-strong-password-123';
FLUSH PRIVILEGES;

exit;
```

### 2. Read-only User बनाओ

```sql
-- Login as admin
mysql -h endpoint -u admin -p

USE locker_tracker;

-- Create read-only user
CREATE USER 'readonly'@'%' IDENTIFIED BY 'readonly-password';
GRANT SELECT ON locker_tracker.* TO 'readonly'@'%';
FLUSH PRIVILEGES;

exit;
```

### 3. Connection Encryption (SSL)

```python
# app_mysql.py में add करो (optional):

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'ssl': {
            'ca': '/path/to/rds-combined-ca-bundle.pem'
        }
    }
}
```

---

## 🛠️ Troubleshooting

### Issue 1: Can't connect to MySQL

```
Error: "Can't connect to MySQL server"

Check करो:
1. Security group में port 3306 open है?
2. RDS endpoint सही है?
3. Public accessible: YES है?
4. Password सही है?

Test करो:
telnet your-endpoint 3306
# अगर connect होता है → security group ठीक है
```

### Issue 2: "Access denied"

```
Error: "Access denied for user 'admin'@'..'"

Solutions:
1. Username सही है? (admin)
2. Password सही है?
3. User active है?

Reset password:
RDS Dashboard → Database → Modify
└─ New master password set करो
└─ Apply immediately
```

### Issue 3: PyMySQL error

```
Error: "ModuleNotFoundError: No module named 'pymysql'"

Solution:
pip install PyMySQL cryptography
```

### Issue 4: "cryptography" error

```
Error: "cryptography is not installed"

Solution:
sudo apt install -y python3-dev build-essential
pip install cryptography
```

### Issue 5: Tables नहीं बन रहे

```bash
# EC2 में
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Tables created!')
"

# या service restart करो:
sudo systemctl restart locker-tracker
sudo journalctl -u locker-tracker -f
```

### Issue 6: Slow performance

```bash
# Connection pool tune करो
# app_mysql.py में:

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 20,        # बढ़ाओ
    'max_overflow': 10,     # Add करो
    'pool_recycle': 1800,   # Lower करो
}
```

---

## 📊 MySQL vs PostgreSQL (Quick Reference)

```
Feature                MySQL          PostgreSQL
─────────────────────────────────────────────────
Setup difficulty       ⭐ Easy        ⭐⭐ Medium
Memory usage           50MB          80MB
Read performance       ⚡⚡⚡         ⚡⚡
Write performance      ⚡⚡          ⚡⚡⚡
Concurrent users       100+         100+
Backup                Built-in       Built-in
Free tier             ✅ YES         ✅ YES
For small teams       ✅ Perfect    ✅ Good
For large teams       ⚡ Good       ✅ Better
Cost (after free)      $3-15/mo      $5-20/mo
```

---

## 📈 Scaling Path

### Small Team (5-10 users):
```
└─ db.t3.micro
└─ 20 GB storage
└─ FREE TIER ✅
```

### Medium Team (50-100 users):
```
└─ db.t3.small
└─ 50 GB storage
└─ Multi-AZ enabled
└─ ~$30/month
```

### Large Team (500+ users):
```
└─ db.t3.medium या larger
└─ Read replicas
└─ ~$100/month
└─ Production ready
```

---

## 💰 Cost Breakdown

### Free Tier (12 months):
```
db.t3.micro:          FREE
20 GB storage:        FREE
Backup (7 days):      FREE
Data transfer:        1 GB/month FREE
─────────────────────────────────
TOTAL:                $0/month
```

### After Free Tier:
```
db.t3.micro:          ~$15/month
Storage (20 GB):      ~$2/month
Backup (extra):       ~$2/month
Data transfer:        ~$1/month
─────────────────────────────────
TOTAL:                ~$20/month
```

---

## ✅ Final Checklist

```
RDS Setup:
☐ MySQL 8.0 instance created
☐ Free tier selected
☐ db.t3.micro instance
☐ 20 GB storage
☐ Public access enabled
☐ Password saved
☐ Endpoint copied

Security:
☐ Security group: port 3306 open
☐ Strong password set
☐ Status: Available

EC2 Setup:
☐ MySQL client installed
☐ Connection tested
☐ Flask app uploaded
☐ requirements-mysql.txt installed
☐ .env file configured

Application:
☐ app_mysql.py copied to app.py
☐ Database tables created (auto)
☐ Default users added
☐ Website accessible
☐ Login works
☐ All features functional

Optimization:
☐ Connection pool configured
☐ Backups automatic
☐ Monitoring enabled
☐ Logs checked
```

---

## 🎉 Summary

```
✅ AWS RDS MySQL instance ready
✅ Flask app connected
✅ Database tables created
✅ Users authentication working
✅ Multi-user access enabled
✅ Production-ready setup

Total Time: ~45 minutes
Cost: FREE (Free Tier)
Users: 100+ concurrent
Reliability: Enterprise-grade
```

---

## 🚀 अब क्या करें?

```
1. ✅ MySQL Setup Complete
2. ✅ Flask Deployed
3. ✅ Website Live

Next Steps:
├─ Team को link दो
├─ Daily backups schedule करो (automatic है)
├─ Monitor करते रहो (CloudWatch)
└─ User feedback लो

Done! 🎊
```

---

## 📞 Quick Help

| Problem | Solution |
|---------|----------|
| Can't connect | Security group check (port 3306) |
| Access denied | Password reset RDS में |
| Slow performance | Connection pool tune करो |
| Need backup | RDS automatic + manual snapshot |
| Want to upgrade | Modify instance class |

---

**Yaar, MySQL completely ready है! 🐬🚀**

**बस 45 minutes में production-grade setup!**

**Happy Deploying! 🎉✨**
