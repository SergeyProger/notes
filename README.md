# 📝 Notes Management Application

Простое приложение для управления заметками, построенное на FastAPI (backend) и Vue.js (frontend) с MongoDB.

## 📂 Структура проекта

```
test_docker/
├── backend/
│   └── main.py                 # FastAPI приложение
├── frontend/
│   ├── index.html              # Главная страница
│   ├── styles/
│   │   ├── main.css            # Скомпилированные стили
│   │   └── main.scss           # SCSS исходники
│   ├── package.json            # NPM зависимости
│   └── docker-compose.yml      # Docker конфигурация
├── docker-compose.yml          # Общая конфигурация контейнеров
└── README.md                   # Этот файл
```

## 🚀 Запуск приложения

### С использованием Docker Compose (рекомендуется)

```bash
docker-compose up
```

Приложение будет доступно по адресу: `http://localhost:3000`

### Локальный запуск

#### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен на: `http://localhost:8000`

#### Frontend (Vue.js)
```bash
cd frontend
# Просто откройте index.html в браузере
# или используйте простой HTTP сервер:
python -m http.server 3000
```

Frontend будет доступен на: `http://localhost:3000`

## 📚 API Маршруты

### GET `/`
Возвращает все заметки (перенаправляет на `/notes`)

### GET `/notes`
Получить все заметки, отсортированные по дате создания (новые первыми)

**Response:**
```json
{
  "notes": [
    {
      "id": "507f1f77bcf86cd799439011",
      "text": "Содержание заметки",
      "created_at": "2026-08-16T18:40:00",
      "updated_at": "2026-08-16T18:45:00"
    }
  ],
  "status": "success"
}
```

### GET `/notes/{note_id}`
Получить одну заметку по ID

### POST `/write`
Создать новую заметку

**Request:**
```json
{
  "text": "Содержание новой заметки"
}
```

### PUT `/notes/{note_id}`
Обновить заметку

**Request:**
```json
{
  "text": "Обновленное содержание"
}
```

### DELETE `/notes/{note_id}`
Удалить заметку

## 🎨 Стили

Стили организованы в следующей структуре:

- **main.scss** — SCSS исходники (организованы с переменными и миксинами)
- **main.css** — Скомпилированный CSS файл

### Компиляция SCSS в CSS

Если вы внесли изменения в `main.scss`, вам нужно пересчитать CSS:

```bash
cd frontend
npm install -D sass
npx sass styles/main.scss styles/main.css
```

## 🛠️ Технологический стек

### Backend
- **FastAPI** — веб-фреймворк
- **Motor** — асинхронный драйвер MongoDB
- **Pydantic** — валидация данных
- **CORS** — поддержка кросс-оригинных запросов

### Frontend
- **Vue.js 3** — фреймворк UI
- **CSS/SCSS** — стили
- **Fetch API** — HTTP запросы

### Database
- **MongoDB** — NoSQL база данных

## ✨ Функциональность

✅ Просмотр всех заметок в виде карточек  
✅ Создание новых заметок  
✅ Редактирование существующих заметок  
✅ Удаление заметок  
✅ Отслеживание дат создания и редактирования  
✅ Статистика (количество заметок)  
✅ Адаптивный дизайн для мобильных устройств  
✅ Уведомления об ошибках и успехе  
✅ Авто-обновление заметок каждые 30 секунд

## 📱 Адаптивность

Приложение полностью адаптивно и работает на:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (до 767px)

## 🔧 Требования

- Node.js 18+ (для фронтенда)
- Python 3.9+ (для бэкенда)
- MongoDB 5.0+ (база данных)
- Docker & Docker Compose (для запуска в контейнерах)

## 📝 Примеры использования

### Создание заметки через API

```bash
curl -X POST http://localhost:8000/write \
  -H "Content-Type: application/json" \
  -d '{"text": "Моя первая заметка"}'
```

### Получение всех заметок

```bash
curl http://localhost:8000/notes
```

### Обновление заметки

```bash
curl -X PUT http://localhost:8000/notes/{note_id} \
  -H "Content-Type: application/json" \
  -d '{"text": "Обновленное содержание"}'
```

### Удаление заметки

```bash
curl -X DELETE http://localhost:8000/notes/{note_id}
```

## 🐛 Troubleshooting

### Не удается подключиться к MongoDB
- Убедитесь, что MongoDB запущен
- Проверьте MONGO_URL в переменных окружения
- По умолчанию: `mongodb://localhost:27017`

### Frontend не видит Backend
- Проверьте что Backend запущен на `http://localhost:8000`
- Убедитесь что CORS правильно настроен
- Проверьте консоль браузера на ошибки

### Стили не применяются
- Очистите кэш браузера (Ctrl+Shift+Delete)
- Убедитесь что файл `styles/main.css` загружается
- Проверьте консоль браузера на ошибки 404

## 📄 Лицензия

MIT License
