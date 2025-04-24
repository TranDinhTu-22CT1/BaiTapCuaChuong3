import os
import shutil
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

DB_FILE = "database/Tu.sqlite3"
BACKUP_FOLDER = "backup"

if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Gửi mail thành công.")
    except Exception as e:
        print(f"Gửi mail thất bại: {e}")

def backup_database():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_FOLDER, f"backup_{now}.sqlite3")

    try:
        shutil.copy(DB_FILE, backup_file)
        print(f"Backup thành công: {backup_file}")
        send_email(
            subject="Backup thành công",
                body=f"Thao tác thành công vào lúc {now}.\nFile được lưu với tên: {backup_file}"
        )
    except Exception as e:
        print(f"Backup Lỗi: {e}")
        send_email(
            subject="Backup Lỗi",
            body=f"Lỗi trong quá trình backup:\n{e}"
        )

schedule.every().day.at("00:00").do(backup_database)

print("Chờ xíu nào... Nữa đêm thông báo sẽ được gửi...")

while True:
    schedule.run_pending()
    time.sleep(60)
