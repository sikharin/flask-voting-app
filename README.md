# 🗳️ Flask Voting App

แอปพลิเคชันให้คะแนนผลงานผ่านเว็บ เหมาะสำหรับใช้งานในงานแข่งขันหรืองานประกวดที่ต้องการให้กรรมการให้คะแนนออนไลน์ และแสดงผลแบบ Dashboard

---

## ✅ ฟีเจอร์

- ให้คะแนนผลงาน 5 เกณฑ์
- บันทึกคะแนนลง Google Sheets อัตโนมัติ
- ป้องกันการโหวตซ้ำ
- มีหน้า Dashboard แสดงคะแนนรวมพร้อมกราฟ
- รองรับบนมือถือ

---

## 📁 โครงสร้างโปรเจกต์

```
flask-voting-app/
├── app.py                      # Flask backend
├── requirements.txt            # รายการ dependencies
├── templates/                  # HTML template ทั้งหมด
│   ├── score_form.html
│   ├── dashboard.html
│   └── already_voted.html
```

---

## ▶️ วิธีรันโปรเจคด้วย `python3 app.py`

### 🔧 1. เตรียม Environment

สร้าง Virtual Environment (แนะนำ)

```bash
python3 -m venv venv
source venv/bin/activate
```

ติดตั้ง dependencies:

```bash
pip install -r requirements.txt
```

### 📄 2. ตั้งค่าตัวแปร Environment สำหรับ Google Sheets API

ในระบบของคุณ ให้กำหนดตัวแปรนี้:

```bash
export GOOGLE_CREDENTIALS_JSON='{"type": "...", ... }'  # วาง JSON string ของ Google service account credentials
```

> 💡 หากคุณใช้ `.env` + `python-dotenv` สามารถโหลดจากไฟล์แทนได้

### 🚀 3. รันเซิร์ฟเวอร์

```bash
python3 app.py
```

เปิดเบราว์เซอร์แล้วเข้า:

```
http://localhost:8080
```

---

## 📊 ส่วนของแอป

- `/score?project=1&judge=1` → ให้คะแนนเฉพาะผลงาน
- `/dashboard` → สรุปคะแนนทุกผลงานพร้อมกราฟ

---

## 🧠 ผู้พัฒนา

โดย [Sikharin Suwannatee](https://github.com/sikharin)  
ใช้งานจริงในกิจกรรมแข่งขันเชิงนวัตกรรม / มหาวิทยาลัย

---

## 📄 License

MIT License
