Architecture
============

Project Structure
-----------------

.. code-block:: text

   backend/
   ├── main.py                    # Entry point - starts Uvicorn server
   ├── pyproject.toml             # Project config & dependencies (UV)
   ├── Dockerfile                 # Multi-stage Docker build
   ├── docker-compose.yml         # Docker Compose setup
   ├── .env.example               # Environment variables template
   ├── alembic.ini                # Alembic migration config
   ├── alembic/                   # Database migrations
   │   ├── env.py
   │   └── versions/
   ├── app/
   │   ├── main.py                # FastAPI app factory + lifespan
   │   ├── config.py              # Pydantic Settings (.env loading)
   │   ├── database.py            # SQLAlchemy engine & session
   │   ├── models/                # SQLAlchemy ORM models (11 tables)
   │   │   ├── category.py
   │   │   ├── item.py
   │   │   ├── addon.py
   │   │   ├── customer.py
   │   │   ├── order.py           # Order, OrderItem, OrderItemAddon
   │   │   ├── discount.py
   │   │   ├── shift.py
   │   │   ├── expense.py
   │   │   └── audit_log.py
   │   ├── schemas/               # Pydantic request/response schemas
   │   │   ├── common.py
   │   │   ├── category.py
   │   │   ├── item.py
   │   │   ├── addon.py
   │   │   ├── customer.py
   │   │   ├── order.py
   │   │   ├── discount.py
   │   │   ├── shift.py
   │   │   ├── expense.py
   │   │   └── dashboard.py
   │   ├── services/              # Business logic layer
   │   │   ├── category_service.py
   │   │   ├── item_service.py
   │   │   ├── addon_service.py
   │   │   ├── customer_service.py
   │   │   ├── order_service.py
   │   │   ├── discount_service.py
   │   │   ├── shift_service.py
   │   │   ├── expense_service.py
   │   │   └── dashboard_service.py
   │   ├── api/v1/                # API route handlers
   │   │   ├── router.py          # Aggregated v1 router
   │   │   ├── categories.py
   │   │   ├── items.py
   │   │   ├── addons.py
   │   │   ├── customers.py
   │   │   ├── orders.py
   │   │   ├── discounts.py
   │   │   ├── shifts.py
   │   │   ├── expenses.py
   │   │   └── dashboard.py
   │   ├── middleware/
   │   │   ├── request_logging.py # Request/response logging
   │   │   └── audit.py           # CUD operation audit trail
   │   ├── seed/
   │   │   ├── seed_data.py       # Comprehensive seed data
   │   │   └── __main__.py        # CLI: python -m app.seed
   │   └── utils/
   │       ├── logger.py          # JSON structured logging
   │       ├── pagination.py      # Generic pagination helper
   │       └── filters.py         # Date range & grouping helpers
   └── docs/                      # Sphinx documentation
       ├── conf.py
       ├── index.rst
       ├── setup.rst
       ├── architecture.rst
       └── api/
           ├── endpoints.rst
           └── schemas.rst


Design Principles
-----------------

**Layered Architecture:**
The application follows a clean layered architecture:

1. **Routes** (``api/v1/``) — HTTP handling, request parsing, response formatting
2. **Services** (``services/``) — Business logic, validations, transactions
3. **Models** (``models/``) — Database schema and relationships
4. **Schemas** (``schemas/``) — Input validation and output serialization

**Key Design Decisions:**

- **SQLite with WAL mode** — Write-Ahead Logging for concurrent read performance
- **Foreign keys enforced** — Data integrity via SQLite pragmas
- **Idempotent seeding** — ``seed_database()`` checks if data exists before seeding
- **Auto-generated order IDs** — Pattern: ``PHI-YYYYMMDD-XXXX``
- **Configurable tax rate** — Via ``TAX_RATE`` environment variable
- **Stock management** — ``stock_qty = -1`` means unlimited stock
- **Audit trail** — Middleware automatically logs all CUD operations


Database Tables
---------------

11 tables total:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Table
     - Description
   * - ``categories``
     - Menu categories (Hot Coffee, Pastries, etc.)
   * - ``items``
     - Menu items with prices and stock
   * - ``addons``
     - Add-on extras (syrups, milk alternatives)
   * - ``customers``
     - Customer profiles with order stats
   * - ``orders``
     - Order headers with totals and status
   * - ``order_items``
     - Line items per order
   * - ``order_item_addons``
     - Addons per order line item
   * - ``discounts``
     - Percentage or flat discount definitions
   * - ``shifts``
     - Cash register shifts (open/close)
   * - ``expenses``
     - Business expenses linked to shifts
   * - ``audit_logs``
     - Automatic CUD operation audit trail


Order Flow
----------

.. code-block:: text

   pending → preparing → ready → completed
       ↓         ↓         ↓
       └─────────┴─────────┴──→ cancelled

   • Stock is deducted when order is created
   • Stock is restored when order is cancelled
   • completed and cancelled are final states


API Flow Diagram
----------------

This diagram shows the typical POS operational flow — from opening a shift
through taking orders to closing at end of day:

.. code-block:: text

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


Data Relationship Diagram
-------------------------

How all database entities relate to each other:

.. code-block:: text

   ┌──────────────┐       ┌──────────────┐
   │  CATEGORIES  │──────<│    ITEMS     │
   │              │ 1:N   │              │
   └──────────────┘       └──────┬───────┘
                                 │ referenced in
                                 ▼
   ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
   │  CUSTOMERS   │──────<│   ORDERS     │>──────│  DISCOUNTS   │
   │  (optional)  │ 1:N   │              │ N:1   │              │
   └──────────────┘       └──────┬───────┘       └──────────────┘
                                 │                ┌──────────────┐
                                 │ N:1            │   SHIFTS     │
                                 │>───────────────│              │
                                 │ 1:N            └──────┬───────┘
                                 ▼                       │ 1:N
                          ┌──────────────┐               ▼
                          │ ORDER_ITEMS  │        ┌──────────────┐
                          └──────┬───────┘        │  EXPENSES    │
                                 │ 1:N            └──────────────┘
                                 ▼
                          ┌────────────────────┐  ┌──────────────┐
                          │ ORDER_ITEM_ADDONS  │─>│   ADDONS     │
                          └────────────────────┘  └──────────────┘


Dashboard Analytics Flow
------------------------

The dashboard endpoints aggregate data from orders, items, customers,
shifts, and expenses to provide rich analytics:

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │                  DASHBOARD ANALYTICS                     │
   ├─────────────────────────────────────────────────────────┤
   │                                                         │
   │  /summary ─────────► KPI cards (revenue, orders, avg)   │
   │  /revenue ─────────► Line/bar chart (time series)       │
   │  /top-items ───────► Bar chart (ranked items)           │
   │  /top-categories ──► Bar chart (ranked categories)      │
   │  /order-trends ────► Line chart (volume over time)      │
   │  /hourly-heatmap ──► Heatmap grid (24h × 7d)           │
   │  /customer-insights► Customer stats + top customers     │
   │  /payment-breakdown► Pie/donut chart (cash/card/mobile) │
   │  /inventory-alerts ► Alert list (low/out of stock)      │
   │  /profit-loss ─────► P&L statement with breakdown       │
   │  /shift-summary ───► Shift table (revenue, expenses)    │
   │                                                         │
   │  All endpoints accept: start_date, end_date             │
   │  Default period: last 30 days                           │
   └─────────────────────────────────────────────────────────┘
