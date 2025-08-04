# Open Banking API Demo

This project demonstrates a simple Open Banking API demo with:
- Mock API server (Docker)
- Flask backend API
- Angular frontend

## Quick Start

### 1. Run the Mock API
```bash
cd back-end/mock-api
docker compose up
```

### 2. Run the Flask Backend
```bash
cd back-end
python app.py
```

### 3. Run the Frontend
```bash
cd front-end
npm install
npm run dev
```

## Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- Mock API: http://localhost:7004

## Project Structure
- `back-end/`: Flask API server and mock API
- `front-end/`: Angular web interface
