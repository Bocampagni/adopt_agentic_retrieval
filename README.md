# Agentic Chat

Full-stack AI chatbot: React frontend (Vite, react-query, Zustand) and FastAPI backend (LangGraph, OpenRouter). Conversation history is persisted in the browser. Ready to extend with agentic CSV retrieval later.

## Run

### Backend

Uses **uv** and a **Makefile**. The virtualenv is created at `backend/.venv` so your editor can use it.

```bash
cd backend
# Copy .env.example to .env and set OPENROUTER_API_KEY
make install   # create .venv and install deps
make run       # start the API
```

API: `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: `http://localhost:5173`

## Environment

| Variable | Where | Description |
|----------|--------|-------------|
| `OPENROUTER_API_KEY` | Backend | Required. Your OpenRouter API key. |
| `OPENROUTER_BASE_URL` | Backend | Optional. Default: `https://openrouter.ai/api/v1` |
| `VITE_API_URL` | Frontend | Optional. Backend URL. Default: `http://localhost:8000` |

Backend: copy `backend/.env.example` to `backend/.env` and set your key. Root `.env.example` lists all vars.

## Project layout

- **backend/** — FastAPI app, LangGraph chat graph, OpenRouter LLM. See `backend/README.md`.
- **frontend/** — React app, model selector, conversation history. See `frontend/README.md`.

Agentic CSV retrieval will be added later by extending the LangGraph graph and optionally the frontend.
