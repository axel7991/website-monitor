import requests
from bs4 import BeautifulSoup
import os
import json
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def fetch_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def save_content(content, filename="last_content.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def load_previous_content(filename="last_content.txt"):
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def get_changes(previous, current):
    previous_lines = set(previous.splitlines())
    current_lines = set(current.splitlines())
    added = current_lines - previous_lines
    removed = previous_lines - current_lines
    return added, removed

def save_change_history(url, added, removed):
    history_file = "change_history.json"
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append({
        "url": url,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lines_added": len(added),
        "lines_removed": len(removed)
    })

    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

def send_email(url, added, removed):
    subject = f"🔔 Change Detected on {url}"

    added_text = "\n".join(list(added)[:5]) or "None"
    removed_text = "\n".join(list(removed)[:5]) or "None"

    body = f"""
Website Change Monitor Alert 🔍

URL: {url}
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

CHANGES DETECTED:
Lines added: {len(added)}
Lines removed: {len(removed)}

NEW CONTENT (sample):
{added_text}

REMOVED CONTENT (sample):
{removed_text}

---
Sent by your Website Change Monitor
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("✅ Email alert sent!")
    except Exception as e:
        print(f"❌ Email failed: {e}")

def check_for_changes(url):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking {url}...")
    current = fetch_website(url)
    previous = load_previous_content()

    if previous is None:
        print("First time checking — saving content.")
        save_content(current)
        return

    if current != previous:
        added, removed = get_changes(previous, current)
        print(f"CHANGE DETECTED — {len(added)} lines added, {len(removed)} removed")
        save_change_history(url, added, removed)
        send_email(url, added, removed)
        save_content(current)
    else:
        print("No changes found.")

url = "https://news.ycombinator.com/newest"

check_for_changes(url)

schedule.every(1).hours.do(check_for_changes, url)

print("✅ Monitor running — checking every hour. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(60)