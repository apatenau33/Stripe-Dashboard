# Stripe Payments Dashboard

A full-stack dashboard that pulls payment data from the Stripe API, stores it locally, and serves it through a REST API to a React front end.

Built as a portfolio project. Runs against Stripe test data.

![Dashboard](docs/screenshot.png)

## What it does

- Pulls payments from the Stripe API and stores them in SQLite
- Upserts on the Stripe payment ID, so repeat syncs never duplicate rows
- Serves the data over a FastAPI REST API with date filtering and limits
- Displays summary metrics and a transaction table in a React front end

## Stack

**Backend:** Python, FastAPI, SQLite
**Frontend:** React, Vite
**External:** Stripe API

## Setup

Requires Python 3.11+ and Node.js 18+.

### 1. Backend

Install dependencies:

    pip install -r requirements.txt

Create a `.env` file in the project root:

    STRIPE_API_KEY=sk_test_your_key_here

Load the data — this step is required before the dashboard will show anything:

    python sync.py

Start the API:

    python api.py

Runs on `http://127.0.0.1:8000`. Interactive docs at `/docs`.

### 2. Frontend

Install dependencies:

    cd frontend
    npm install

Create `frontend/.env` (see `.env.example`):

    VITE_API_URL=http://127.0.0.1:8000

Start it:

    npm run dev

Open `http://localhost:5173`.

## API

| Endpoint | Description |
|---|---|
| `GET /api/payments` | Payment records. Optional `start`, `end` (ISO dates) and `limit` (max 500). |
| `GET /api/summary` | Gross volume, transaction count, average payment, total records, last sync time. |

## Demo mode

If `VITE_API_URL` is not set, the front end falls back to a bundled JSON snapshot in `src/`. This lets the dashboard be deployed as a static site without a live backend.

## Project structure

    api.py             FastAPI application and endpoints
    database.py        SQLite schema and connection handling
    sync.py            Fetches from Stripe and upserts into the database
    fetch_payments.py  Stripe API client
    helpers.py         Retry logic and logging
    frontend/          React + Vite dashboard

## Notes

The SQLite database and `.env` are gitignored. Run `python sync.py` after cloning to populate the database.