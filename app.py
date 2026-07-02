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
        self.wfile.write(b"Trading Bot is Active and Live!")

def run_render_server():
    # سيتعرف الكود فوراً على المنفذ المفتوح من المنصة
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# تشغيل السيرفر تلقائياً في الخلفية لمنع ظهور علامة الإكس الحمراء
threading.Thread(target=run_render_server, daemon=True).start()

# 2. ⚙️ جلب توكن تليجرام ورقم الحساب تلقائياً من إعدادات Render الدقيقة
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("تنبيه: التوكن أو الآيدي غير متوفرين في الإعدادات!")
        return
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

# 3. 📊 عقل الروبوت لفحص الأسواق (يبدأ بالعمل فوراً بشكل دائم)
def trading_strategy_loop():
    # إرسال رسالة الترحيب والانطلاق المؤكدة
    send_telegram_message("🤖 تم تشغيل الروبوت بنجاح واكتمل الربط! وبدأت مراقبة الأسواق الآن...")
    
    while True:
        try:
            # جلب أسعار السوق الحية من Binance كمثال
            api_url = "https://binance.com"
            response = requests.get(api_url).json()
            current_price = float(response['price'])
            
            # فحص شروط استراتيجية التداول الخاصة بكم (محاكاة لإرسال الإشارات)
            last_digit = int(str(int(current_price))[-1])
            
            if last_digit == 7:
                msg = f"📈 **إشارة صعود (شراء)**\nالزوج: BTC/USDT\nالسعر الحالي: ${current_price:,}"
                send_telegram_message(msg)
            elif last_digit == 3:
                msg = f"📉 **إشارة هبوط (بيع)**\nالزوج: BTC/USDT\nالسعر الحالي: ${current_price:,}"
                send_telegram_message(msg)
                
        except Exception as e:
            print(f"Error in trading loop: {e}")
            
        time.sleep(10) # فحص مستمر كل 10 ثوانٍ

# إطلاق عقل الروبوت للتداول
trading_strategy_loop()
