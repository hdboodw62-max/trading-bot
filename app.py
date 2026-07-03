import os
import time
import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. 🌐 كود السيرفر الوهمي المطور لفتح المنفذ 10000 تلقائياً وإرضاء موقع Render ومنع علامة الـ X
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Super Sensitive Bot is Active and Live!")

def run_render_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# تشغيل السيرفر تلقائياً في الخلفية لمنع توقف الموقع وتحويله للأخضر
threading.Thread(target=run_render_server, daemon=True).start()

# 2. ⚙️ جلب توكن تليجرام ورقم الحساب تلقائياً من إعدادات البيئة في Render
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

# 3. 📊 استراتيجية فائقة الحساسية لإجبار البوت على الإرسال الفوري اللحظي
def trading_strategy_loop():
    # رسالة ترحيبية فورية تظهر في تليجرام بمجرد نجاح التحديث الأخضر
    send_telegram_message("🔔 **تم تشغيل رادار الفحص اللحظي فائق الحساسية بنجاح!**\nسيبدأ الروبوت الآن بضخ الإشارات فوراً مع أي حركة بسيطة في السوق لتأكيد نجاح الربط...")
    
    previous_price = None
    
    while True:
        try:
            # جلب سعر البيتكوين الحي من منصة Binance العالمية
            api_url = "https://binance.com"
            response = requests.get(api_url).json()
            current_price = float(response['price'])
            
            if previous_price is not None:
                price_change = current_price - previous_price
                
                # شرط صعود فائق الحساسية (مع أي ارتفاع للبيتكوين)
                if price_change > 0:
                    msg = (
                        f"📈 **إشارة صعود لحظية (شراء / BUY)**\n"
                        f"• **الزوج:** BTC/USDT\n"
                        f"• **السعر الحالي:** ${current_price:,}\n"
                        f"• **الحركة:** صعود طفيف بمقدار ${price_change:.2f}"
                    )
                    send_telegram_message(msg)
                
                # شرط هبوط فائق الحساسية (مع أي انخفاض للبيتكوين)
                elif price_change < 0:
                    msg = (
                        f"📉 **إشارة هبوط لحظية (بيع / SELL)**\n"
                        f"• **الزوج:** BTC/USDT\n"
                        f"• **السعر الحالي:** ${current_price:,}\n"
                        f"• **الحركة:** هبوط طفيف بمقدار ${abs(price_change):.2f}"
                    )
                    send_telegram_message(msg)
            
            previous_price = current_price
                    
        except Exception as e:
            print(f"Error in trading loop: {e}")
            
        # فحص سريع جداً ومستمر كل 10 ثوانٍ
        time.sleep(10)

# إطلاق الروبوت
trading_strategy_loop()
