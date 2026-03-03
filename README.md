# Garden Planning App

A companion planting web app that helps you plan an aesthetically pleasing garden. Select your seeds, set your garden preferences, and get AI-powered recommendations for plant groupings, containers, and layout.

![Plan Page](docs/screenshot.png)


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

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` with your API key:

```
ANTHROPIC_API_KEY=your-api-key-here
```

Run the server:

```bash
uvicorn app.main:app --reload --port 8000
```

API docs available at [localhost:8000/docs](http://localhost:8000/docs).

### Frontend

```bash
cd frontend
npm install
npm run dev
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

## Testing

- **Backend:** `pytest tests/ -v`
- **Frontend:** Vitest (unit), Playwright (e2e)


## Future features

 - make images look like stardew valley