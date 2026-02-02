import httpx
from app.config import settings

async def send_telegram_notification(message: str):
    if not settings.TELEGRAM_BOT_TOKEN:
        return
        
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
        
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=data, timeout=5.0)
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")
