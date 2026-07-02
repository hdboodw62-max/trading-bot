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
        self.wfile.write(b"Professional Trading Bot is Active!")

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

# 4. 📊 عقل الروبوت: إستراتيجية تداول دقيقة تعتمد على حركة الأسعار الحقيقية
def trading_strategy_loop():
    send_telegram_message("⚙️ **تم تفعيل رادار التداول الاحترافي الحقيقي!**\nالروبوت يقوم الآن بتحليل الاتجاه اللحظي لزوج BTC/USDT وإرسال صفقات دقيقة...")
    
    prices_history = []
    
    while True:
        try:
            # جلب آخر الأسعار الحية للبيتكوين من Binance
            api_url = "https://binance.com"
            response = requests.get(api_url).json()
            current_price = float(response['price'])
            
            # حفظ السعر في الذاكرة لعمل متوسط حسابي دقيق
            prices_history.append(current_price)
            if len(prices_history) > 10:  # الاحتفاظ بآخر 10 قراءات فقط لحساب الاتجاه
                prices_history.pop(0)
            
            if len(prices_history) >= 5:
                # حساب متوسط السعر للفترة السابقة (Moving Average مصغر)
                average_price = sum(prices_history[:-1]) / len(prices_history[:-1])
                
                # 📈 إشارة صعود دقيقة: إذا اخترق السعر الحالي المتوسط للأعلى بفارق ملحوظ
                if current_price > (average_price + 5.0):
                    msg = (
                        f"🎯 **إشارة صعود دقيقة (شراء / BUY)**\n"
                        f"• **الزوج:** BTC/USDT\n"
                        f"• **سعر الدخول:** ${current_price:,}\n"
                        f"• **الاتجاه:** اختراق إيجابي صاعد فوق المتوسط اللحظي السعري"
                    )
                    send_telegram_message(msg)
                    # تنظيف الذاكرة مؤقتاً لتجنب تكرار الإشارة لنفس الحركة
                    prices_history = [current_price]
                
                # 📉 إشارة هبوط دقيقة: إذا كسر السعر الحالي المتوسط للأسفل بفارق ملحوظ
                elif current_price < (average_price - 5.0):
                    msg = (
                        f"🎯 **إشارة هبوط دقيقة (بيع / SELL)**\n"
                        f"• **الزوج:** BTC/USDT\n"
                        f"• **سعر الدخول:** ${current_price:,}\n"
                        f"• **الاتجاه:** كسر سلبي هابط تحت المتوسط اللحظي السعري"
                    )
                    send_telegram_message(msg)
                    prices_history = [current_price]
                    
        except Exception as e:
            print(f"Error in trading loop: {e}")
            
        # فحص وتحليل دقيق للسوق كل 10 ثوانٍ
        time.sleep(10)

# إطلاق الروبوت الحقيقي
trading_strategy_loop()
