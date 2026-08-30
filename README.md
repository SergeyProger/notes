# 📝 Notes Management Application

A simple note management application built with FastAPI (backend) and Vue.js (frontend) with MongoDB.

## 📂 Project structure

```
test_docker/
├── backend/
│   └── main.py                 # FastAPI application
├── frontend/
│   ├── index.html              # Main page
│   ├── styles/
│   │   └── main.scss           # SCSS sources
│   ├── package.json            # NPM dependencies
│   └── docker-compose.yml      # Docker configuration
├── docker-compose.yml          # Overall container configuration
└── README.md                   # This file
```

## 🚀 Running the application

### Using Docker Compose (recommended)

```bash
docker-compose up
```

The application will be available at: `http://localhost:3000`

### Running locally

#### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`

#### Frontend (Vue.js)
```bash
cd frontend
# Simply open index.html in a browser
# or use a simple HTTP server:
python -m http.server 3000
```

The frontend will be available at: `http://localhost:3000`

## 📚 API routes

### GET `/`
Returns all notes (redirects to `/notes`)

### GET `/notes`
Get all notes sorted by creation date (newest first)

**Response:**
```json
{
  "notes": [
    {
      "id": "507f1f77bcf86cd799439011",
      "text": "Note content",
      "title": "Note title",
      "created_at": "2026-08-16T18:40:00",
      "updated_at": "2026-08-16T18:45:00"
    }
  ],
  "status": "success"
}
```

### GET `/notes/{note_id}`
Get a single note by ID

### POST `/write`
Create a new note

**Request:**
```json
{
  "text": "New note content"
}
```

### PUT `/notes/{note_id}`
Update a note

**Request:**
```json
{
  "text": "Updated content"
}
```

### DELETE `/notes/{note_id}`
Delete a note

## 🎨 Styles

The styles are organized in the following structure:

- **main.scss** — SCSS sources (organized with variables and mixins)
- **main.css** — Compiled CSS file

### Compiling SCSS into CSS

If you made changes to `main.scss`, you need to recompile the CSS:

```bash
cd frontend
npm install -D sass
npx sass styles/main.scss styles/main.css
```

## 🛠️ Technology stack

### Backend
- **FastAPI** — web framework
- **Motor** — asynchronous MongoDB driver
- **Pydantic** — data validation
- **CORS** — cross-origin request support

### Frontend
- **Vue.js 3** — UI framework
- **CSS/SCSS** — styles
- **Fetch API** — HTTP requests

### Database
- **MongoDB** — NoSQL database

## ✨ Features

✅ View all notes as cards  
✅ Create new notes  
✅ Edit existing notes  
✅ Delete notes  
✅ Track creation and edit dates  
✅ Statistics (note count)  
✅ Responsive design for mobile devices  
✅ Error and success notifications  
✅ Auto-refresh of notes every 30 seconds

## 📱 Responsiveness

The application is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (up to 767px)

## 🔧 Requirements

- Node.js 18+ (for the frontend)
- Python 3.9+ (for the backend)
- MongoDB 5.0+ (database)
- Docker & Docker Compose (to run in containers)

## 📝 Usage examples

### Creating a note via the API

```bash
curl -X POST http://localhost:8000/write \
  -H "Content-Type: application/json" \
  -d '{"text": "My first note"}'
```

### Getting all notes

```bash
curl http://localhost:8000/notes
```

### Updating a note

```bash
curl -X PUT http://localhost:8000/notes/{note_id} \
  -H "Content-Type: application/json" \
  -d '{"text": "Updated content"}'
```

### Deleting a note

```bash
curl -X DELETE http://localhost:8000/notes/{note_id}
```

## 🐛 Troubleshooting

### Cannot connect to MongoDB
- Make sure MongoDB is running
- Check MONGO_URL in the environment variables
- Default: `mongodb://localhost:27017`

### The frontend does not see the backend
- Check that the backend is running at `http://localhost:8000`
- Make sure CORS is configured correctly
- Check the browser console for errors

### Styles are not applied
- Clear the browser cache (Ctrl+Shift+Delete)
- Make sure the `styles/main.css` file is being loaded
- Check the browser console for 404 errors

## 📄 License

MIT License
