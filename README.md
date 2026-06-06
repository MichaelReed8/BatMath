# BatMath

BatMath is a local baseball analytics app for calculating adjusted expected batted-ball outcomes using Statcast data. The current app has two parts:

- A Python backend that owns the database, Statcast ingestion, and DxBA calculations.
- A TypeScript React frontend that runs in a Vite development server and calls the Python backend over HTTP.

## Project Structure

```text
BatMath/
  BatMath.db                 # SQLite database used by the backend
  backend/
    api.py                   # FastAPI HTTP adapter
    Runner.py                # Optional CLI client
    requirements.txt         # Python backend dependencies
    Controller_Layer/        # Controller endpoints used by API/CLI
    Business_Layer/          # DxBA and slugging calculation logic
    Data_Layer/              # SQLite and pybaseball data access
    Models/                  # Internal request/result dataclasses
    Constants/               # Baseball event constants
  frontend/
    package.json             # Node/Vite scripts and dependencies
    vite.config.ts           # Dev server proxy config
    src/                     # React UI
```

The backend intentionally keeps the SQLite database at `BatMath/BatMath.db`. The data layer resolves that path directly, so you can start the backend from the project root without accidentally opening another `BatMath.db`.

## Install Dependencies

From the outer project directory:

```powershell
py -m pip install -r BatMath\backend\requirements.txt
cd BatMath\frontend
npm.cmd install
```

Use `npm.cmd` on Windows PowerShell if `npm` is blocked by the script execution policy.

## Start the Development Servers

Start the Python backend from the outer project directory:

```powershell
py -m uvicorn BatMath.backend.api:app --reload --host 127.0.0.1 --port 8000
```

Start the frontend in a second terminal:

```powershell
cd BatMath\frontend
npm.cmd run dev
```

Then open:

```text
http://127.0.0.1:5173
```

The Vite dev server serves the React app on port `5173`. API requests from the browser go to paths like `/api/dxba/calculate`. Vite proxies those `/api` requests to the FastAPI backend at `http://127.0.0.1:8000`, as configured in `frontend/vite.config.ts`.

## How Frontend Calls Reach the Backend

The request flow is:

```text
Browser UI
  -> Vite dev server at http://127.0.0.1:5173
  -> Vite proxy for /api/*
  -> FastAPI app at http://127.0.0.1:8000
  -> Controller_Layer
  -> Business_Layer
  -> Data_Layer
  -> BatMath.db
```

The frontend never talks directly to SQLite or pybaseball. It only calls HTTP endpoints exposed by FastAPI.

## API Endpoints

### Health Check

```http
GET /api/health
```

Response:

```json
{
  "status": "ok"
}
```

### Calculate DxBA

```http
POST /api/dxba/calculate
```

Request body:

```json
{
  "launch_angle": 20,
  "exit_velocity": 95,
  "spray_angle": -8,
  "angle_forgiveness": 2,
  "velocity_forgiveness": 2,
  "launch_forgiveness": 2
}
```

The forgiveness fields are optional at the API boundary. If they are omitted, FastAPI defaults all three to `2`.

Response:

```json
{
  "batting_average": 0.321,
  "slugging": 0.654,
  "samples": 42
}
```

Backend flow:

```text
api.py
  -> calculate_dxba(...)
  -> GetData(...)
  -> fetchData(...)
  -> SQLite query against DxBA
```

### Reset Data

```http
POST /api/data/reset
```

This drops user-defined SQLite tables and recreates the `DxBA` table. The frontend requires confirmation before calling this endpoint.

Response:

```json
{
  "success": true,
  "message": "DxBA table was cleared and recreated.",
  "rows_affected": 1
}
```

### Import Statcast Data

```http
POST /api/data/import
```

This calls the backend import path, pulls Statcast data through `pybaseball`, transforms it, and appends rows to the `DxBA` table.

Response:

```json
{
  "success": true,
  "message": "Statcast data import completed.",
  "rows_affected": 12345
}
```

This operation can take a while because it may fetch external Statcast data.

## Frontend Behavior

The React app is a local tool screen:

- The main form asks for launch angle, exit velocity, and spray angle.
- Forgiveness inputs are visible and default to `2`.
- Submit calls `POST /api/dxba/calculate`.
- Results show adjusted batting average, adjusted slugging, and sample count.
- Admin controls can reset the local table or import Statcast data.
- Reset uses a browser confirmation prompt because it is destructive.
- Import and calculation buttons show loading/status messages.

## Optional CLI Runner

The CLI is still available if you want to call the controller layer without the web frontend:

```powershell
py -m BatMath.backend.Runner
```

The CLI and HTTP API both use the same controller/business/data layers.

## Verification

Compile the backend:

```powershell
py -m compileall BatMath
```

Build the frontend:

```powershell
cd BatMath\frontend
npm.cmd run build
```

Check the live backend:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/health
```

Call the calculator manually:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/dxba/calculate `
  -ContentType "application/json" `
  -Body '{"launch_angle":20,"exit_velocity":95,"spray_angle":-8}'
```

That request omits forgiveness fields, so the backend uses the default value of `2` for all three.
