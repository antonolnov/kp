# Сервер WorkHere КП Bot

## Доступ к серверу

- **IP:** 217.26.27.252
- **User:** root
- **Password:** o3R6HU&MqNzC

## SSH подключение

```bash
ssh root@217.26.27.252
```

## Расположение бота

```
/opt/workhere-bot/
```

## Управление сервисом

```bash
# Статус
systemctl status workhere-bot

# Перезапуск
systemctl restart workhere-bot

# Остановка
systemctl stop workhere-bot

# Логи
journalctl -u workhere-bot -f
```

## Конфигурация

Файл `.env` находится в `/opt/workhere-bot/.env`

```bash
nano /opt/workhere-bot/.env
```

После изменения конфигурации перезапустите бот:
```bash
systemctl restart workhere-bot
```

## Telegram Bot

- **Token:** 8289166080:AAEKdsZJpCH4X6YNhGod3_AUs4oOEFQvWK0
- **Username:** найти в @BotFather

## API ключи

Для AI-анализа транскрибаций нужен OpenAI API ключ.

Добавьте в `/opt/workhere-bot/.env`:
```
OPENAI_API_KEY=sk-ваш_ключ_openai
```

Затем перезапустите:
```bash
systemctl restart workhere-bot
```

Без ключа бот использует базовый анализ (извлекает данные из текста без AI).
