import os
import time
import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. ⚙️ جلب الإعدادات تلقائياً من Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# 2. 🌐 كود السيرفر الوهمي للبقاء حياً على Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Trading Bot is Active and running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# 3. 💬 دالة إرسال الرسائل إلى تليجرام
def send_telegram_message(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

# 4. 📊 عقل الروبوت: استراتيجية تداول حقيقية وسهلة (تعتمد على تغير السعر)
def trading_strategy_loop():
    send_telegram_message("🚀 **بدأت إستراتيجية التداول الحقيقية الآن!**\nيقوم الروبوت بمراقبة حركة السعر وإرسال الصفقات فوراً عند حدوث تغير حاد في السوق...")
    
    # متغير لحفظ السعر السابق لمقارنته بالسعر الجديد
    previous_price = None
    
    while True:
        try:
            # جلب السعر الحي للبيتكوين من Binance
            api_url = "https://binance.com"
            response = requests.get(api_url).json()
            current_price = float(response['price'])
            
            if previous_price is not None:
                # حساب نسبة التغير بين السعر الحالي والسابق
                price_change = current_price - previous_price
                
                # 📈 شرط الصعود: إذا ارتفع السعر بأكثر من 2 دولار في آخر 10 ثوانٍ
                if price_change >= 2.0:
                    msg = (
                        f"📈 **إشارة صعود حقيقية (شراء / BUY)**\n"
                        f"• **الزوج:** BTC/USDT\n"
                        f"• **سعر الدخول:** ${current_price:,}\n"
                        f"• **الحركة:** ارتفاع سريع بمقدار ${price_change:.2f}"
                    )
                    send_telegram_message(msg)
                
                # 📉 شرط الهبوط: إذا انخفض السعر بأكثر من 2 دولار في آخر 10 ثوانٍ
                elif price_change <= -2.0:
                    msg = (
                        f"📉 **إشارة هبوط حقيقية (بيع / -SELL)**\n"
                        f"• **الزوج:** BTC/USDT\n"
                        f"• **سعر الدخول:** ${current_price:,}\n"
                        f"• **الحركة:** انخفاض سريع بمقدار ${abs(price_change):.2f}"
                    )
                    send_telegram_message(msg)
            
            # حفظ السعر الحالي ليصبح هو السعر السابق في الفحص القادم
            previous_price = current_price
                
        except Exception as e:
            print(f"Error in trading loop: {e}")
            
        # فحص السوق كل 10 ثوانٍ بشكل مستمر
        time.sleep(10)

# تشغيل الاستراتيجية الحقيقية
trading_strategy_loop()
