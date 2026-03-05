# ☕ Philo Coffee Shop — POS API

A full-featured **Point-of-Sale REST API** for Philo Coffee Shop, built with **FastAPI** + **SQLite** + **SQLAlchemy**.

📚 **[Live Documentation](https://mrqadeer.github.io/philo-coffee-shop/)** | 📖 **[Frontend Integration Guide](FrontendTask.md)**

## Features

- **Full CRUD** — Categories, Items, Add-ons, Customers, Orders, Discounts, Shifts, Expenses
- **Rich Dashboard** — 11 analytics endpoints (revenue, top items, trends, heatmap, P&L, etc.)
- **Order Management** — Status flow: `pending → preparing → ready → completed/cancelled`
- **Inventory Tracking** — Stock levels with low-stock alerts
- **Tax & Discounts** — Configurable tax rate, percentage & flat discounts
- **Shift Management** — Open/close shifts, track expenses per shift
- **Audit Trail** — Automatic logging of all create/update/delete operations
- **Structured Logging** — JSON-formatted logs with request timing
- **Data Seeding** — 30+ menu items, 8 customers, 50+ sample orders pre-loaded
- **Auto Docs** — Interactive Swagger UI + ReDoc

---

## Quick Start

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.12+ | [python.org](https://www.python.org/downloads/) |
| UV | latest | See below |

**Install UV:**

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

### 🐧🍎 Setup on macOS / Linux

```bash
# Clone the repo
git clone https://github.com/mrqadeer/philo-coffee-shop.git
cd philo-coffee-shop/backend

# Install dependencies
uv sync

# Copy environment config
cp .env.example .env

# Run database migrations
uv run alembic upgrade head

# Seed the database (optional — auto-seeds on first start)
uv run python -m app.seed

# Start the server
uv run python main.py
```

### 🪟 Setup on Windows

```powershell
# Clone the repo
git clone https://github.com/mrqadeer/philo-coffee-shop.git
cd philo-coffee-shop\backend

# Install dependencies
uv sync

# Copy environment config
copy .env.example .env

# Run database migrations
uv run alembic upgrade head

# Seed the database (optional — auto-seeds on first start)
uv run python -m app.seed

# Start the server
uv run python main.py
```

### 🐳 Setup with Docker

```bash
# Option 1: Docker Compose (recommended)
docker compose up -d

# Option 2: Pull from Docker Hub
docker pull mrqadeer/philo-coffee-shop:latest
docker run -p 8000:8000 mrqadeer/philo-coffee-shop:latest

# Option 3: Build locally
docker build -t philo-coffee-shop .
docker run -p 8000:8000 philo-coffee-shop
```

**📦 Pre-seeded Database Included:** The Docker image includes a fully seeded SQLite database with 6 categories, 37 menu items, 12 add-ons, 8 customers, 4 discounts, 61 shifts, 64 expenses, and 440 sample orders. No setup required!

---

## Access the API

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI (interactive) |
| http://localhost:8000/redoc | ReDoc (read-only) |
| http://localhost:8000/health | Health check |
| http://localhost:8000/openapi.json | OpenAPI spec |

---

## API Flow Diagram

This shows how all resources connect and the typical POS operation flow:

```
                              ┌──────────────┐
                              │   START DAY  │
                              └──────┬───────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │   POST /shifts/open  │
                          │  (Open a new shift)  │
                          └──────────┬──────────┘
                                     │
              ┌──────────────────────┼───────────────────────┐
              │                      │                       │
              ▼                      ▼                       ▼
   ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐
   │  GET /categories  │  │  GET /customers   │  │   GET /discounts   │
   │  GET /items       │  │  (lookup/create)  │  │   (active ones)    │
   │  GET /addons      │  │                   │  │                    │
   │  (Load menu)      │  │                   │  │                    │
   └────────┬─────────┘  └────────┬──────────┘  └─────────┬──────────┘
            │                      │                       │
            └──────────────────────┼───────────────────────┘
                                   │
                                   ▼
                       ┌───────────────────────┐
                       │    POST /orders        │
                       │  (Create new order)    │
                       │  items + addons +      │
                       │  customer + discount   │
                       └───────────┬───────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌──────────┐  ┌──────────────┐  ┌──────────┐
            │ PENDING  │  │  PREPARING   │  │  READY   │
            │          ├─►│              ├─►│          │
            └──┬───────┘  └──────┬───────┘  └──┬───────┘
               │                 │              │
               │    ┌────────────┘              │
               │    │                           │
               ▼    ▼                           ▼
          ┌──────────────┐              ┌──────────────┐
          │  CANCELLED   │              │  COMPLETED   │
          └──────────────┘              └──────────────┘
                                               │
                                   ┌───────────┼───────────┐
                                   ▼                       ▼
                          ┌────────────────┐     ┌──────────────────┐
                          │ POST /expenses │     │ GET /dashboard/* │
                          │ (Track costs)  │     │ (View analytics) │
                          └────────────────┘     └──────────────────┘
                                   │
                                   ▼
                        ┌─────────────────────────┐
                        │ PATCH /shifts/{id}/close │
                        │    (End of day)          │
                        └─────────────────────────┘
```

### Order Status Lifecycle

```
            pending ──► preparing ──► ready ──► completed
               │            │          │
               └────────────┴──────────┴──────► cancelled

  • Stock is deducted when order is created
  • Stock is restored when order is cancelled
  • completed and cancelled are final states
```

> **📚 [Live Documentation](https://mrqadeer.github.io/philo-coffee-shop/)** — Complete API reference with curl examples and JSON schemas
> 
> **📖 [FrontendTask.md](FrontendTask.md)** — Detailed integration guide for frontend developers

---

## API Endpoints

### Core Resources

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET/POST` | `/api/v1/categories` | List / Create categories |
| `GET/PATCH/DELETE` | `/api/v1/categories/{id}` | Get / Update / Delete category |
| `GET/POST` | `/api/v1/items` | List / Create menu items |
| `GET/PATCH/DELETE` | `/api/v1/items/{id}` | Get / Update / Delete item |
| `GET/POST` | `/api/v1/addons` | List / Create add-ons |
| `GET/PATCH/DELETE` | `/api/v1/addons/{id}` | Get / Update / Delete add-on |
| `GET/POST` | `/api/v1/customers` | List / Create customers |
| `GET/PATCH/DELETE` | `/api/v1/customers/{id}` | Get / Update / Delete customer |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/orders` | List orders (filter by status, dates) |
| `POST` | `/api/v1/orders` | Create order |
| `GET` | `/api/v1/orders/{id}` | Get order detail |
| `PATCH` | `/api/v1/orders/{id}/status` | Update order status |

### Discounts, Shifts & Expenses

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET/POST` | `/api/v1/discounts` | List / Create discounts |
| `GET/POST` | `/api/v1/shifts`, `/shifts/open` | List / Open shift |
| `PATCH` | `/api/v1/shifts/{id}/close` | Close shift |
| `GET/POST` | `/api/v1/expenses` | List / Create expenses |

### Dashboard (Analytics)

All dashboard endpoints accept `period` param: `today`, `week`, `month`, `year`, or `date_from`/`date_to`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/dashboard/summary` | KPIs: revenue, orders, avg ticket |
| `GET` | `/api/v1/dashboard/revenue` | Revenue breakdown over time |
| `GET` | `/api/v1/dashboard/top-items` | Top selling items |
| `GET` | `/api/v1/dashboard/top-categories` | Top revenue categories |
| `GET` | `/api/v1/dashboard/order-trends` | Order count trends |
| `GET` | `/api/v1/dashboard/hourly-heatmap` | Sales by hour of day |
| `GET` | `/api/v1/dashboard/customer-insights` | Customer analytics |
| `GET` | `/api/v1/dashboard/payment-breakdown` | Revenue by payment method |
| `GET` | `/api/v1/dashboard/inventory-alerts` | Low stock items |
| `GET` | `/api/v1/dashboard/profit-loss` | P&L statement |
| `GET` | `/api/v1/dashboard/shift-summary` | Shift performance |

---

## Project Structure

```
backend/
├── main.py                    # Entry point (starts Uvicorn)
├── pyproject.toml             # Dependencies (UV)
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Docker Compose config
├── .env.example               # Environment template
├── alembic.ini                # Migration config
├── alembic/                   # Database migrations
├── app/
│   ├── main.py                # FastAPI app factory
│   ├── config.py              # Settings from .env
│   ├── database.py            # SQLAlchemy engine & session
│   ├── models/                # 11 database tables
│   ├── schemas/               # Request/response schemas
│   ├── services/              # Business logic
│   ├── api/v1/                # Route handlers
│   ├── middleware/             # Logging & audit
│   ├── seed/                  # Sample data
│   └── utils/                 # Helpers (logger, pagination, filters)
└── docs/                      # Sphinx documentation
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | Philo Coffee Shop | App display name |
| `DATABASE_URL` | sqlite:///./data/philo_coffee.db | Database connection |
| `TAX_RATE` | 0.08 | Tax rate (8%) |
| `LOG_LEVEL` | INFO | Logging level |
| `CORS_ORIGINS` | ["http://localhost:3000"] | Allowed CORS origins |
| `LOW_STOCK_THRESHOLD` | 10 | Inventory alert threshold |

---

## Build & Push Docker Image

```bash
# Build the image
docker build -t mrqadeer/philo-coffee-shop:latest .

# Push to Docker Hub
docker login
docker push mrqadeer/philo-coffee-shop:latest
```

---

## Generate Sphinx Docs

```bash
uv run sphinx-build -b html docs docs/_build/html

# Open in browser
open docs/_build/html/index.html   # macOS
# or
xdg-open docs/_build/html/index.html   # Linux
```

**📚 Live Documentation:** [https://mrqadeer.github.io/philo-coffee-shop/](https://mrqadeer.github.io/philo-coffee-shop/)

**Automatic Deployment:** Documentation is automatically built and published to GitHub Pages on every push to `master` via GitHub Actions. See [.github/workflows/docs.yml](.github/workflows/docs.yml)

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Config | Pydantic Settings |
| Package Manager | UV |
| Docs | Sphinx (RTD theme) |
| Container | Docker |

---

## License

This project is for demonstration purposes.
