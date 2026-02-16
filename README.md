# TaskPulse Demo Guide

## Prerequisites
- Python 3.10+ installed
- Ports 5000 (backend) and 3000 (frontend) available

## Start Servers
1. Backend (API)
   - In PowerShell:
     - `cd mini-task-manager`
     - Dev: `python -m backend.app`
     - Prod: `python -m backend.prod_server`
   - Backend runs at `http://127.0.0.1:5000/`
2. Frontend (static pages)
   - In another PowerShell:
     - `cd mini-task-manager`
     - `python -m http.server 3000 --directory frontend`
   - Frontend runs at `http://127.0.0.1:3000/`

## Login
1. Open `http://127.0.0.1:3000/login-page.html`
2. Enter:
   - Username: `admin`
   - Password: `password`
3. On success, a JWT token is stored in browser localStorage.

## Add Task (Reflects on Kanban & Schedule)
1. Go to Kanban: `http://127.0.0.1:3000/kanban-Board.html`
2. Click “Add Task” → opens the modal.
3. Fill title, project, priority, due date/time, description.
4. Click “Create Task”.
   - This calls `POST /api/tasks` with your JWT.
   - You will be redirected back to Kanban.
5. Kanban renders tasks dynamically by status and updates counts.
6. Open Schedule Dashboard: `http://127.0.0.1:3000/schedule-dashboard.html` to see totals updated.

## Delete Task
1. From Kanban, click a task card to open details.
2. Task Details loads `/api/tasks/:id`.
3. Click the close/delete icon to remove the task.
4. You return to Kanban; counts and lists reflect removal on reload.

## Overview, Team, Analytics
- Overview: `http://127.0.0.1:3000/overview.html`
  - Uses `/api/overview` and `/api/analytics` for totals and latest tasks.
- Team: `http://127.0.0.1:3000/team.html`
  - Uses `/api/team` for members, roles, availability.
- Analytics: `http://127.0.0.1:3000/analytics.html`
  - Uses `/api/analytics` for totals, weekly created, by-status, by-priority.

## Backend API Summary
- Auth:
  - `POST /api/login` → `{ access_token, user }`
  - Use `Authorization: Bearer <token>`
- Tasks:
  - `POST /api/tasks` → create
  - `GET /api/tasks?limit=50` → list
  - `GET /api/tasks/:id` → get
  - `PUT /api/tasks/:id` → update
  - `DELETE /api/tasks/:id` → delete
  - `PATCH /api/tasks/:id/status` → move across columns
- Dashboard:
  - `GET /api/overview`, `GET /api/stats`, `GET /api/analytics`, `GET /api/team`

## Run Automated Tests (Backend)
1. Install pytest (user site):
   - `python -m pip install --user pytest`
2. Run:
   - `cd mini-task-manager`
   - `python -m pytest backend/test -vv -s`
3. The suite creates a task, lists tasks, and deletes it.

## Troubleshooting
- If login fails:
  - Ensure backend is running at `http://127.0.0.1:5000`.
  - Restart browsers or clear localStorage.
- If API calls fail with 401:
  - Token may be expired/missing; log in again.
- If ports are in use:
  - Change ports or stop conflicting processes.

## Demo Flow (Presentation)
1. Start both servers.
2. Login and show token saved.
3. Create a task in modal; show it on Kanban.
4. Open Schedule; show updated totals.
5. Open task details; delete it; show Kanban reflects removal.
6. Visit Overview, Team, Analytics; show live data from API.

## Scale To 100+ Users
- Use production server on Windows:
  - `python -m backend.prod_server`
- Use PostgreSQL:
  - Set `DATABASE_URL=postgresql://user:password@host:5432/dbname`
  - Ensure the database exists and reachable.
- Configure JWT:
  - Set `JWT_SECRET_KEY` to a strong 32+ byte secret.
- Connection pooling:
  - Pool size and overflow are configured in app.
- Caching:
  - Listing and analytics endpoints are cached to reduce load.
