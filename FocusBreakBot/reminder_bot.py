
# ███▄ ▄███▓▓█████  ███▄    █  ▄▄▄        ██████▓██   ██▓
#▓██▒▀█▀ ██▒▓█   ▀  ██ ▀█   █ ▒████▄    ▒██    ▒ ▒██  ██▒
#▓██    ▓██░▒███   ▓██  ▀█ ██▒▒██  ▀█▄  ░ ▓██▄    ▒██ ██░
#▒██    ▒██ ▒▓█  ▄ ▓██▒  ▐▌██▒░██▄▄▄▄██   ▒   ██▒ ░ ▐██▓░
#▒██▒   ░██▒░▒████▒▒██░   ▓██░ ▓█   ▓██▒▒██████▒▒ ░ ██▒▓░
#░ ▒░   ░  ░░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ██▒▒▒
#░  ░      ░ ░ ░  ░░ ░░   ░ ▒░  ▒   ▒▒ ░░ ░▒  ░ ░▓██ ░▒░
#░      ░      ░      ░   ░ ░   ░   ▒   ░  ░  ░  ▒ ▒ ░░
#       ░      ░  ░         ░       ░  ░      ░  ░ ░
#                                                ░ ░

# reminder_bot.py
# Python-Telegram-Bot 13.15 ile uyumludur.

import os
import logging
import requests
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv

# ---------------- .env ----------------
load_dotenv()
TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")
PRAYER_API_URL = os.getenv(
    "VERCEL_PRAYER_TIME_API_URL",
    "https://vakit.vercel.app/api/timesFromCoordinates?lat=41.0082&lng=28.9784"
)

# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("log.txt", encoding="utf-8")]
)
log = logging.getLogger("FocusBreak")

# ---------------- Globals ----------------
bot = Bot(token=TOKEN)
scheduler = None
running = False
TZ = "Europe/Istanbul"

# ---------------- Utils ----------------
def send_message(text):
    """Telegram'a mesaj gönder ve logla."""
    try:
        bot.send_message(chat_id=CHAT_ID, text=text)
        log.info(f"Gönderildi: {text}")
    except Exception as e:
        log.error(f"Mesaj gönderilemedi: {e}")

def clear_prayer_jobs():
    """Namaz joblarını temizle."""
    if scheduler:
        for job in list(scheduler.get_jobs()):
            if job.id.startswith("prayer_"):
                try:
                    scheduler.remove_job(job.id)
                except JobLookupError:
                    pass

def send_eye_reminder():
    send_message("👀 Gözlerini dinlendir — kısa bir mola ver.")

# ---------------- Namaz Vakitleri ----------------
def fetch_prayer_times():
    try:
        resp = requests.get(PRAYER_API_URL, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        if "times" not in data:
            raise ValueError(f"Beklenmeyen API formatı: {data}")
        today_key = sorted(data["times"].keys())[0]
        vakitler = data["times"][today_key]
        isimler = ["imsak", "gunes", "ogle", "ikindi", "aksam", "yatsi"]
        return dict(zip(isimler, vakitler))
    except Exception as e:
        log.error(f"Namaz vakitleri alınamadı: {e}")
        return {}

def schedule_prayer_alerts():
    if scheduler is None:
        return
    clear_prayer_jobs()
    times = fetch_prayer_times()
    today = datetime.now()
    for key, t_str in times.items():
        try:
            vakit_dt = datetime.combine(today.date(), datetime.strptime(t_str, "%H:%M").time())
            alert_dt = vakit_dt - timedelta(minutes=40)
            if alert_dt > datetime.now():
                job_id = f"prayer_{today.strftime('%Y%m%d')}_{key}"
                scheduler.add_job(
                    send_message, 'date',
                    run_date=alert_dt,
                    args=[f"🕌 {key.capitalize()} vakti yaklaşıyor — {t_str}"],
                    id=job_id, replace_existing=True
                )
        except Exception as e:
            log.error(f"{key} planlanırken hata: {e}")

# ---------------- Scheduler ----------------
def start_scheduler():
    global scheduler, running
    if running:
        return
    scheduler = BackgroundScheduler(timezone=TZ)
    scheduler.start()
    scheduler.add_job(send_eye_reminder, 'interval', hours=1,
                      next_run_time=datetime.now(), id="eye_reminder", replace_existing=True)
    schedule_prayer_alerts()
    scheduler.add_job(schedule_prayer_alerts, 'cron', hour=0, minute=5,
                      id="daily_refresh", replace_existing=True)
    running = True
    log.info("Hatırlatıcılar başlatıldı.")

def stop_scheduler():
    global scheduler, running
    if scheduler:
        clear_prayer_jobs()
        try:
            scheduler.shutdown(wait=False)
        except Exception:
            pass
    scheduler = None
    running = False
    log.info("Hatırlatıcılar durduruldu.")

# ---------------- Telegram Komutları ----------------
def cmd_start(update, context):
    log.info(f"/start komutu: {update.effective_user.username}")
    start_scheduler()
    update.message.reply_text("▶️ Hatırlatıcılar başlatıldı.")

def cmd_break(update, context):
    log.info(f"/break komutu: {update.effective_user.username}")
    stop_scheduler()
    update.message.reply_text("⏸️ Hatırlatıcılar durduruldu.")

def cmd_stop(update, context):
    log.info(f"/stop komutu: {update.effective_user.username} -> program kapanıyor.")
    update.message.reply_text("🛑 Program kapatılıyor…")
    stop_scheduler()
    os._exit(0)

# ---------------- Main ----------------
def main():
    month_names = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    now = datetime.now()
    today = f"{now.day} {month_names[now.month - 1]} {now.year}"
    startup_msg = (
        f"💠 FocusBreak — {today}\n\n"
        "Komutlar:\n"
        "• /start — Hatırlatıcıları başlat\n"
        "• /break — Hatırlatıcıları durdur\n"
        "• /stop — Programı kapat"
    )
    send_message(startup_msg)

    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", cmd_start))
    dp.add_handler(CommandHandler("break", cmd_break))
    dp.add_handler(CommandHandler("stop", cmd_stop))

    updater.start_polling()
    log.info("Bot başladı ve komutları dinliyor.")
    updater.idle()

if __name__ == "__main__":
    main()
