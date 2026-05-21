# ⚡ Locker Tracker - Flask Web App - QUICK START

**Bilkul Simple! Bas 5 minutes में शुरू कर दो! 🚀**

---

## 🎯 क्या करना है?

Desktop App (Tkinter) को Web App (Flask) में convert किया है।  
अब **कोई भी, कहीं से भी, किसी device से** use कर सकता है।

---

## 🏃 5 Minute Setup (Windows)

### ✅ Step 1: Python Check करो

```bash
python --version
```

अगर नहीं है तो: https://python.org से download करो और install करो।

### ✅ Step 2: Project Files Download करो

1. सभी files एक folder में रखो: `locker-tracker-web`
2. Command prompt खोलो
3. उस folder में जाओ:

```bash
cd C:\Users\YourName\Desktop\locker-tracker-web
```

### ✅ Step 3: Virtual Environment बनाओ

```bash
python -m venv venv
venv\Scripts\activate
```

(अगर सफल है तो prompt में `(venv)` दिखेगा)

### ✅ Step 4: Dependencies Install करो

```bash
pip install -r requirements.txt
```

### ✅ Step 5: App चलाओ

```bash
python app.py
```

### ✅ Step 6: Browser में खोलो

```
http://localhost:5000
```

### ✅ Login करो

```
User ID: superadmin
Password: Admin@123
```

**बस! 🎉 Done!**

---

## 📱 अब 5-6 लोग कैसे use करें?

### Option 1: Same Network (LAN)

अगर सब एक office network में हैं:

1. **Command में यह run करो:**
```bash
python app.py
```

2. **अपना IP address find करो:**

```bash
ipconfig
```

`IPv4 Address` देखो (कुछ यूँ: `192.168.1.5`)

3. **सभी को यह link दो:**
```
http://192.168.1.5:5000
```

4. **सभी अपने devices से access कर सकते हैं! ✅**

---

### Option 2: AWS पर Deploy (Best! ⭐)

**Benefits:**
- ✅ Internet से anywhere से access
- ✅ 24/7 available रहता है
- ✅ हजारों लोग use कर सकते हैं
- ✅ Free tier available है AWS का

**How to:**
1. AWS account बनाओ (Free)
2. EC2 instance create करो
3. `DEPLOYMENT_GUIDE.md` file को follow करो

---

## 🔑 Default Users (सब login कर सकते हैं)

| User ID    | Password  | Role       | Permission |
|------------|-----------|------------|-----------|
| superadmin | Admin@123 | SuperAdmin | सब कुछ |
| admin01    | Admin@123 | Admin      | Assign/Release/Reports |
| oper01     | Oper@123  | Operator   | Assign/Release |
| viewer01   | View@123  | Viewer     | Reports only |

---

## 📁 Files की जानकारी

```
📦 locker-tracker-web/
│
├─ 📄 app.py                      ← Main application (यह run करो)
├─ 📄 requirements.txt            ← Dependencies
├─ 📄 DEPLOYMENT_GUIDE.md         ← AWS deploy करने के लिए
│
├─ 📁 templates/                  ← HTML pages
│  ├─ login.html                  ← Login page
│  ├─ dashboard.html              ← Home page
│  ├─ assign.html                 ← Locker assign करने के लिए
│  ├─ release.html                ← Locker release करने के लिए
│  ├─ employees.html              ← Employee search
│  ├─ reports.html                ← Reports
│  └─ base.html                   ← Common layout
│
└─ 📁 locker_tracker.db           ← Database (auto-create होगी)
```

---

## 🛠️ Features

✅ **Login System** - Role-based access control  
✅ **Dashboard** - Statistics और recent activities  
✅ **Locker Assignment** - Employees को locker assign करो  
✅ **Locker Release** - Lockers release करो  
✅ **Employee Search** - किसी भी employee को ढूंढो  
✅ **Reports** - Floor-wise और Audit reports  
✅ **Audit Log** - सभी actions का record  
✅ **Auto-refresh** - Dashboard हर 30 seconds में refresh  

---

## 🐛 Common Issues

### Issue: `No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use

**Solution 1:**
```bash
# किसी और port पर run करो
python app.py
# फिर browser में जाओ: http://localhost:5001
```

**Solution 2:**
```bash
# Windows में
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Database error

**Solution:**
```bash
# Database delete करो
del locker_tracker.db

# फिर से run करो
python app.py
```

---

## 🚀 Production Deploy (AWS)

**Super important है बड़े organization के लिए!**

Detailed guide के लिए: **`DEPLOYMENT_GUIDE.md`** पढ़ो

Quick steps:
1. AWS EC2 instance create करो
2. Python install करो
3. Project clone करो
4. `pip install -r requirements.txt`
5. Gunicorn + Nginx setup करो

**Result:** `http://yourdomain.com` से 5-6 लोग access कर सकते हैं! ✅

---

## 💾 Database

Default database **SQLite** है (`locker_tracker.db`)

अगर बहुत सारे users हैं तो PostgreSQL में upgrade कर सकते हो:

```python
# app.py में बदलो:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@hostname:5432/locker'
```

---

## 📊 Data Backup

Database को backup करना important है:

```bash
# Backup लो
copy locker_tracker.db locker_tracker_backup.db

# या daily automatic backup
# Windows Scheduler या cronjob से करो
```

---

## 🎓 Learning Path

1. **Basic:** `app.py` को समझो
2. **Intermediate:** `templates/` में HTML changes करो
3. **Advanced:** Database models या new features add करो

---

## 🤝 Customization

### Colors बदलना

`templates/base.html` में search करो:
```css
--primary: #4db8ff;  ← यह color
```

Apना color code use करो (eg: `#FF6B6B`)

### Users add करना

Database में directly add कर सकते हो:

```python
# app.py में जाओ, यह section find करो:

users = [
    User(user_id='newuser', user_name='नया यूजर', 
         password=generate_password_hash('Password@123'), user_role='Operator'),
]
```

---

## 📈 Next Steps

1. ✅ Local पर test करो (5 min में complete)
2. ✅ AWS पर deploy करो (1-2 hours)
3. ✅ Employees को share करो
4. ✅ Feedback लो
5. ✅ Improvements करते रहो

---

## 💬 Need Help?

Check करो:
1. Terminal में error message क्या है?
2. Browser console (F12 → Console tab)
3. `DEPLOYMENT_GUIDE.md` file
4. Code comments पढ़ो

---

## 🎉 Summary

| Feature | Desktop | Web |
|---------|---------|-----|
| LAN में share | ❌ | ✅ |
| Internet से access | ❌ | ✅ |
| Multi-user | Limited | ✅ |
| Installation | Kompleks | Simple (pip) |
| Cost | Free | Free (AWS Free Tier) |

**पहले locally test करो, फिर AWS पर deploy करो! 🚀**

---

## 🔐 Security Reminder

- ✅ `superadmin` password change करो (secret key भी)
- ✅ Database को backup रखो
- ✅ AWS पर SSL certificate लगाओ
- ✅ Regular updates करते रहो

---

**Happy coding! 💻✨**
