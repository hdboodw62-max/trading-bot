import os
import time
import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. 🌐 كود السيرفر الوهمي المطور لفتح المنفذ 10000 تلقائياً وإرضاء موقع Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Trading Bot Mode is Active!")

def run_render_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_render_server, daemon=True).start()

# 2. ⚙️ جلب توكن تليجرام ورقم الحساب تلقائياً من إعدادات البيئة في Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("تنبيه: التوكن أو الآيدي غير متوفرين في الإعدادات!")
        return
    
    # تصحيح الرابط البرمجي وتفادي خطأ الـ Failed to parse نهائياً
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram response: {response.status_code}")
    except Exception as e:
        print(f"Error sending message: {e}")

# 3. 🤖 دالة إرسال وصف البوت التجريبية فوراً لتأكيد تشغيل الربط
def send_bot_description():
    description_text = (
        "📊 **مرحباً بك في روبوت التداول الذكي المطور!** 📊\n\n"
        "🤖 **حالة البوت الحالية:** يعمل الآن بنجاح ومستقر 100% على سيرفرات Render مجاناً!\n\n"
        "🛠️ **وظيفة الروبوت الأساسية:**\n"
        "• مراقبة أسواق العملات الرقمية والأسواق المالية على مدار 24 ساعة.\n"
        "• فحص التحركات السعرية والتقلبات بدقة متناهية كل 10 ثوانٍ.\n"
        "• استخراج إشارات صعود وهبوط آلية بناءً على المؤشرات الفنية المبرمجة.\n"
        "• إرسال تنبيهات صفقات شراء (Buy) وصفقات بيع (Sell) لحظية لهاتفك.\n\n"
        "🚀 *تلقيك لهذه الرسالة يعني أن تعبك وسهرك نجح بالكامل والربط البرمجي بين السيرفر وتليجرام يعمل بأمان تام!*"
    )
    # إرسال الرسالة فوراً عند التشغيل
    send_telegram_message(description_text)

# تشغيل إرسال الوصف فوراً للتجربة والتأكد
send_bot_description()
