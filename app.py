import os
import time
import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. ⚙️ إعدادات تليجرام الخاصة بكم (تُجلب تلقائياً من إعدادات البيئة في Render)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# 2. 🌐 كود السيرفر الوهمي لتشغيل البوت مجاناً على Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running successfully!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"Server started on port {port}")
    server.serve_forever()

# تشغيل سيرفر الويب في الخلفية لمنع توقف Render
threading.Thread(target=run_server, daemon=True).start()

# 3. 💬 دالة إرسال الرسائل إلى تليجرام
def send_telegram_message(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")

# 4. 📊 دالة جلب الأسعار وفحص الاستراتيجية (مثال باستخدام سعر البيتكوين كمؤشر)
def trading_strategy_loop():
    # نرسل رسالة ترحيبية للتأكد أن البوت اتصل بتليجرام بنجاح
    send_telegram_message("🤖 تم تشغيل الروبوت بنجاح! وبدأت مراقبة الأسواق الآن...")
    
    while True:
        try:
            # جلب سعر البيتكوين كمثال حي من منصة Binance مجاناً وبدون حساب
            api_url = "https://binance.com"
            response = requests.get(api_url).json()
            current_price = float(response['price'])
            
            # --- 🛠️ استراتيجية وهمية للفحص (يمكنكم تعديل الشروط لاحقاً) ---
            last_digit = int(str(int(current_price))[-1])
            
            if last_digit == 7: # شرط صعود وهمي للفحص والتجربة
                msg = f"📈 **إشارة صعود (شراء)**\nالزوج: BTC/USDT\nالسعر الحالي: ${current_price:,}"
                send_telegram_message(msg)
                
            elif last_digit == 3: # شرط هبوط وهمي للفحص والتجربة
                msg = f"📉 **إشارة هبوط (بيع)**\nالزوج: BTC/USDT\nالسعر الحالي: ${current_price:,}"
                send_telegram_message(msg)
                
        except Exception as e:
            print(f"Error in trading loop: {e}")
            
        # يفحص السوق كل 10 ثوانٍ
        time.sleep(10)

# تشغيل عقل الروبوت والاستراتيجية في الخلفية
trading_strategy_loop()
