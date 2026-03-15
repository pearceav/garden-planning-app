# Garden Planning App

A companion planting web app that helps you plan an aesthetically pleasing garden. Select your seeds, set your garden preferences, and get AI-powered recommendations for plant groupings, containers, and layout.

![Plan Page](docs/plan.png)


## Tech Stack

- **Frontend:** SvelteKit + TypeScript
- **Backend:** Python / FastAPI
- **AI:** Anthropic Claude API
- **Storage:** Browser localStorage (no database)

## Project Structure

```
garden-planning-app/
├── backend/           # FastAPI server
├── frontend/          # SvelteKit app
├── docs/              # Implementation plans
├── seeds.txt          # Master seed list by category
├── plant-care.txt     # Plant spacing, soil, sun, water requirements
└── boxes.txt          # Container types and recommendations
```

## Local Development

Tested with **Git Bash on Windows 11**. Should also work in PowerShell or WSL with minor path adjustments.

### Prerequisites

- Python 3.10+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com/)

### 1. Backend

Open a Git Bash terminal:

```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```
ANTHROPIC_API_KEY=your-api-key-here
```

Start the server:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API will be running at [localhost:8000](http://localhost:8000). Interactive docs at [localhost:8000/docs](http://localhost:8000/docs).

### 2. Frontend

Open a second Git Bash terminal:

```bash
cd frontend
npm install
npm run dev
```

The app will be running at [localhost:5173](http://localhost:5173).

### Running both together

You need both servers running at the same time. Open two Git Bash terminals:

| Terminal | Command | URL |
|---|---|---|
| 1 (Backend) | `cd backend && source venv/Scripts/activate && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` | localhost:8000 |
| 2 (Frontend) | `cd frontend && npm run dev` | localhost:5173 |

> **Note:** On macOS/Linux, use `source venv/bin/activate` instead of `source venv/Scripts/activate`.

### Making changes

- **Frontend:** Vite hot-reloads automatically — just save the file and the browser updates.
- **Backend:** Uvicorn does **not** auto-reload by default. After editing Python files, stop the server (`Ctrl+C`) and restart it. Or start it with `--reload` to enable auto-reload during development:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## API

| Endpoint | Method | Description |
|---|---|---|
| `/api/seeds` | GET | Returns seeds grouped by category |
| `/api/garden/plan` | POST | Takes selected seeds + preferences, returns AI recommendations |

## Features

- **Seed Selection** — Browse seeds by category (fruits, veggies, herbs, flowers) and select what you want to grow
- **Garden Preferences** — Set yard dimensions, sun exposure, and preferred bed types
- **AI Garden Plans** — Claude generates companion planting groups with container recommendations and an SVG layout diagram with proportional bed dimensions
- **Saved Gardens** — Save plans to localStorage; browse and load them from the sidebar, or delete them from the plan view
- **Bloom Schedule** — See which plants bloom in spring, summer, and fall

## Documentation

Detailed implementation plans live in the [docs/](docs/) folder:

- [Backend Plan](docs/BACKEND-PLAN.md) — FastAPI architecture, endpoints, Claude prompt strategy, and data models
- [Frontend Plan](docs/FRONTEND-PLAN.md) — SvelteKit components, stores, pages, and UI flow
- [Sidebar Plan](docs/SIDEBAR-PLAN.md) — Saved gardens sidebar design
- [Bed Layout Plan](docs/BED-LAYOUT-PLAN.md) — Plant quantities and perimeter flower placement

## Testing

- **Backend:** `pytest tests/ -v`
- **Frontend:** Vitest (unit), Playwright (e2e)


## Future features

 - make images look like stardew valley ( done)
 - make a hover over each garden bed and show the water needs