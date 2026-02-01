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

**Cursor API:** `key_d1032ba22d13ba165c7fd0278cfa3708b7ffff9131b97fbc5aae73b4d3187376`

Ключ уже добавлен в `/opt/workhere-bot/.env`
