# Ledger — Billing Platform Frontend

A React frontend for the Subscription Management & Automated Billing FastAPI backend.

## Setup

```bash
npm install
cp .env.example .env   # adjust VITE_API_BASE_URL if your backend isn't on 127.0.0.1:8000
npm run dev
```

The app runs on **http://localhost:5173** by default. The backend's CORS config
only allows `localhost:3000`, `127.0.0.1:3000`, `localhost:5173`, `127.0.0.1:5173` —
so run the frontend on one of those, and make sure the FastAPI server is running
(`uvicorn app.main:app --reload`, default port 8000).

## Login note

The backend's `/auth/login` endpoint uses `OAuth2PasswordRequestForm`, so the
login request is sent as `application/x-www-form-urlencoded`, not JSON — this
is already handled in `src/services/authService.js`.

## Known backend gap

There is no `/auth/me` endpoint, so the frontend only knows the signed-in
user's **email** and **role** (decoded from the JWT) — no username or user ID
is available client-side after login. The UI shows the email in the topbar
accordingly.

## Structure

See `src/` — organized into `components/`, `pages/`, `layouts/`, `context/`,
`services/` (one file per backend resource), `routes/` (auth guards), `hooks/`,
and `utils/`.

## Build

```bash
npm run build
npm run preview
```
