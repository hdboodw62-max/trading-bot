import os
import time
import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. 🌐 كود السيرفر الوهمي للبقاء حياً على Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Super Sensitive Bot is Active!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# 2. ⚙️ جلب الإعدادات تلقائياً من Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

# 3. 📊 استراتيجية فائقة الحساسية لإجبار البوت على الإرسال فوراً
def trading_strategy_loop():
    # رسالة ترحيبية فورية للتأكد من نجاح التحديث
    send_telegram_message("🔔 **تم تشغيل رادار الفحص السريع والمستمر!**\nسيبدأ الروبوت الآن بضخ الإشارات فوراً مع أي حركة بسيطة في السوق للتأكد من عمل الربط...")
    
    previous_price = None
    
    while True:
        try:
            # جلب سعر البيتكوين الحي من Binance
            api_url = "https://binance.com"
            response = requests.get(api_url).json()
            current_price = float(response['price'])
            print(f"Current Bitcoin Price: {current_price}") # لجعل السجلات تتحرك أمامك دائماً
            
            if previous_price is not None:
                price_change = current_price - previous_price
                
                # شرط صعود فائق الحساسية (أي ارتفاع أكبر من صفر)
                if price_change > 0:
                    msg = (
                        f"📈 **إشارة صعود لحظية (شراء / BUY)**\n"
                        f"• **الزوج:** BTC/USDT\n"
                        f"• **السعر:** ${current_price:,}\n"
                        f"• **الحركة:** صعود طفيف بمقدار ${price_change:.2f}"
                    )
                    send_telegram_message(msg)
                
                # شرط هبوط فائق الحساسية (أي انخفاض أصغر من صفر)
                elif price_change < 0:
                    msg = (
                        f"📉 **إشارة هبوط لحظية (بيع / SELL)**\n"
                        f"• **الزوج:** BTC/USDT\n"
                        f"• **السعر:** ${current_price:,}\n"
                        f"• **الحركة:** هبوط طفيف بمقدار ${abs(price_change):.2f}"
                    )
                    send_telegram_message(msg)
            
            previous_price = current_price
                    
        except Exception as e:
            print(f"Error in trading loop: {e}")
            
        # فحص سريع ومستمر كل 10 ثوانٍ
        time.sleep(10)

# إطلاق الروبوت
trading_strategy_loop()
