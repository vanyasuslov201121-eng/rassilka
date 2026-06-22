import os
import telebot
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"

CHANNEL_ID = "@cookieeditort"

CHAT_IDS = [
    "@Steal_a_Brainrota04",
    "@Steal_a_Brainrotah",
    "@Garden_a_grow",
    "@vyrastu_sad2",
    "@grow_a_gardenj_2",
    "@roblox_chat6767",
    "@AdoptMe_mist",
    "@Garden_a_growj",
    "@Roblox_ChatG",
    "@ukradi_breinrota10",
    "@AdoptMeFly"
]

bot = telebot.TeleBot(BOT_TOKEN)
last_sent_message_id = None

# ========== ТЕСТОВАЯ ОТПРАВКА ==========
def test_send():
    """Принудительная отправка тестового сообщения во все чаты"""
    print("\n🧪 ТЕСТОВАЯ РАССЫЛКА")
    print("-" * 40)
    
    success = 0
    for chat in CHAT_IDS:
        try:
            bot.send_message(chat, "🧪 Тест: Бот работает и может отправлять сообщения!")
            print(f"  ✅ Отправлено в {chat}")
            success += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"  ❌ Ошибка для {chat}: {e}")
    
    print("-" * 40)
    print(f"📊 Отправлено в {success} из {len(CHAT_IDS)} чатов\n")
    return success > 0

def quick_test():
    """Быстрая диагностика"""
    print("\n" + "="*50)
    print("🔍 ДИАГНОСТИКА")
    print("="*50)
    
    try:
        me = bot.get_me()
        print(f"✅ Бот: @{me.username}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    try:
        chat = bot.get_chat(CHANNEL_ID)
        print(f"✅ Канал: {chat.title}")
    except Exception as e:
        print(f"❌ Канал: {e}")
        return False
    
    print("="*50 + "\n")
    return True

def get_latest_post():
    try:
        messages = bot.get_chat_history(CHANNEL_ID, limit=1)
        for msg in messages:
            return msg
        return None
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return None

def send_to_all_chats(message):
    if not message:
        return False
    
    success_count = 0
    for chat in CHAT_IDS:
        try:
            if message.text:
                bot.send_message(chat, f"📢 {message.text}")
            elif message.photo:
                bot.send_photo(chat, message.photo[-1].file_id, caption=message.caption)
            else:
                bot.forward_message(chat, CHANNEL_ID, message.message_id)
            
            print(f"  ✅ {chat}")
            success_count += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"  ❌ {chat}: {e}")
    
    print(f"📊 Отправлено: {success_count}/{len(CHAT_IDS)}")
    return success_count > 0

def main():
    global last_sent_message_id
    
    if not quick_test():
        print("❌ Диагностика не пройдена")
        return
    
    # 👇 ТЕСТОВАЯ РАССЫЛКА
    print("🧪 Отправляю тестовое сообщение...")
    test_send()
    
    print("🚀 БОТ ЗАПУЩЕН!")
    print(f"📡 Канал: {CHANNEL_ID}")
    print(f"📨 Чатов: {len(CHAT_IDS)}")
    print("⏱️  Интервал: 80 секунд\n")
    
    while True:
        try:
            latest_post = get_latest_post()
            
            if latest_post:
                if last_sent_message_id is None or latest_post.message_id != last_sent_message_id:
                    print(f"\n📢 НОВЫЙ ПОСТ! ID: {latest_post.message_id}")
                    send_to_all_chats(latest_post)
                    last_sent_message_id = latest_post.message_id
                else:
                    print("⏳ Пост уже отправлен")
            else:
                print("⚠️ Нет постов в канале")
            
            time.sleep(80)
            
        except KeyboardInterrupt:
            print("\n🛑 Остановлено")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(80)

if __name__ == "__main__":
    main()
