## Сервис интеграции с 1С ЗУП

### Подготовка

- Скопировать `.env.example` как `.env`;
- Заполнить `.env`;
- Внести изменения в конфигурацию HAproxy из файла `haproxy.example.cfg`;
- Внести изменения в `docker-compose.yml`: смонтировать логи сервиса в директорию с остальными логами системы.

### Развертывание

```bash
docker-compose up --build -d
```

### Проверка

Проверить работоспособность можно при помощи GET-метода `/ping`, возвращает строку `pong`. Действие записывается в лог-файл сервиса.
