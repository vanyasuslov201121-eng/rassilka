import os
import telebot
import time

# ТОКЕН вашего бота-администратора канала
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Если переменная окружения не задана, используем токен напрямую (для локального тестирования)
if not BOT_TOKEN:
    BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"  # Вставьте сюда токен для теста

# Ваш канал, откуда берем посты
CHANNEL_ID = "@cookieeditort"

# ВСЕ чаты для рассылки (обновленный список)
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

# Храним ID последнего отправленного поста
last_sent_message_id = None

# ========== ДИАГНОСТИКА ==========
def quick_test():
    """Быстрая диагностика перед запуском"""
    print("\n" + "="*50)
    print("🔍 БЫСТРАЯ ПРОВЕРКА")
    print("="*50)
    
    # 1. Проверяем токен
    try:
        me = bot.get_me()
        print(f"✅ Бот: @{me.username} (ID: {me.id})")
    except Exception as e:
        print(f"❌ Ошибка токена: {e}")
        print("   Проверьте правильность BOT_TOKEN")
        return False
    
    # 2. Проверяем канал
    try:
        chat = bot.get_chat(CHANNEL_ID)
        print(f"✅ Канал: {chat.title} ({CHANNEL_ID})")
    except Exception as e:
        print(f"❌ Ошибка канала: {e}")
        print("   Проверьте:")
        print("   - Правильно ли написан @канал")
        print("   - Бот - администратор канала")
        print("   - У бота есть права на чтение сообщений")
        return False
    
    # 3. Проверяем посты в канале
    try:
        messages = bot.get_chat_history(CHANNEL_ID, limit=3)
        count = 0
        for msg in messages:
            count += 1
            print(f"   📝 Пост {count}: {msg.text[:50] if msg.text else 'медиа'} (ID: {msg.message_id})")
        
        if count == 0:
            print("   ⚠️ В канале нет постов!")
            print("   Опубликуйте хотя бы 1 пост в канале")
        else:
            print(f"   ✅ Найдено {count} постов")
    except Exception as e:
        print(f"   ❌ Ошибка чтения постов: {e}")
    
    # 4. Проверяем чаты (первые 5 для скорости)
    print("\n📨 ПРОВЕРКА ЧАТОВ:")
    available = 0
    for chat in CHAT_IDS[:5]:  # Проверяем первые 5
        try:
            info = bot.get_chat(chat)
            available += 1
            print(f"  ✅ {chat} - доступен")
        except Exception as e:
            print(f"  ❌ {chat} - ОШИБКА: {e}")
    
    if len(CHAT_IDS) > 5:
        print(f"  ... и еще {len(CHAT_IDS) - 5} чатов")
    
    print("-" * 40)
    print(f"📊 Проверено {min(5, len(CHAT_IDS))} чатов")
    print("="*50 + "\n")
    return True

def get_latest_post():
    """Получает самый последний пост из канала"""
    try:
        messages = bot.get_chat_history(CHANNEL_ID, limit=1)
        for msg in messages:
            return msg
        return None
    except Exception as e:
        print(f"⚠️ Ошибка при получении поста: {e}")
        return None

def send_to_all_chats(message):
    """Отправляет сообщение во все чаты из списка"""
    if not message:
        print("❌ Нет сообщения для отправки")
        return False
    
    success_count = 0
    
    for chat in CHAT_IDS:
        try:
            # Отправляем текст, если есть
            if message.text:
                bot.send_message(chat, f"📢 {message.text}")
            # Отправляем медиа, если есть
            elif message.photo:
                bot.send_photo(chat, message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                bot.send_video(chat, message.video.file_id, caption=message.caption)
            elif message.document:
                bot.send_document(chat, message.document.file_id, caption=message.caption)
            else:
                # Просто пересылаем
                bot.forward_message(chat, CHANNEL_ID, message.message_id)
            
            print(f"  ✅ Отправлено в {chat}")
            success_count += 1
            time.sleep(0.3)  # Задержка между чатами
            
        except Exception as e:
            print(f"  ❌ Ошибка для {chat}: {e}")
    
    print(f"📊 Отправлено в {success_count} из {len(CHAT_IDS)} чатов")
    return success_count > 0

def check_all_chats():
    """Проверяет доступность всех чатов перед запуском"""
    print("\n🔍 ПРОВЕРКА ВСЕХ ЧАТОВ:")
    print("-" * 40)
    
    available = 0
    for chat in CHAT_IDS:
        try:
            bot.get_chat(chat)
            print(f"  ✅ {chat} - доступен")
            available += 1
        except Exception as e:
            print(f"  ❌ {chat} - ОШИБКА: {e}")
    
    print("-" * 40)
    print(f"📊 Доступно: {available} из {len(CHAT_IDS)} чатов\n")
    return available

def main():
    global last_sent_message_id
    
    # Запускаем диагностику
    if not quick_test():
        print("❌ Диагностика не пройдена. Исправьте ошибки и перезапустите бота.")
        return
    
    print("🚀 БОТ ЗАПУЩЕН!")
    print(f"📡 Канал: {CHANNEL_ID}")
    print(f"📨 Всего чатов: {len(CHAT_IDS)}")
    print("⏱️  Интервал: 80 секунд")
    print("🔄 Ожидание первого поста...\n")
    
    # Проверяем все чаты
    check_all_chats()
    
    while True:
        try:
            # Получаем последний пост
            latest_post = get_latest_post()
            
            if latest_post:
                # Если это новый пост (еще не отправляли)
                if last_sent_message_id is None or latest_post.message_id != last_sent_message_id:
                    print(f"\n📢 НОВЫЙ ПОСТ! ID: {latest_post.message_id}")
                    print(f"📝 Текст: {latest_post.text[:100] if latest_post.text else 'медиа'}")
                    print("-" * 40)
                    
                    # Отправляем во все чаты
                    send_to_all_chats(latest_post)
                    
                    # Запоминаем ID отправленного поста
                    last_sent_message_id = latest_post.message_id
                    print(f"💾 Пост сохранен (ID: {last_sent_message_id})")
                else:
                    print(f"⏳ Пост уже отправлен. Ждем 80 секунд...")
            else:
                print("⚠️ Не удалось получить пост из канала")
            
            # Ждем 80 секунд перед следующей проверкой
            time.sleep(80)
            
        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен пользователем")
            break
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            time.sleep(80)

# ЗАПУСК
if __name__ == "__main__":
    main()
