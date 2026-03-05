Setup Guide
===========

Prerequisites
-------------

- **Python 3.12+**
- **UV** package manager (``curl -LsSf https://astral.sh/uv/install.sh | sh``)
- Or **Docker** for containerized deployment

Installation with UV
--------------------

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/mrqadeer/philo-coffee-shop.git
   cd philo-coffee-shop/backend

   # Install dependencies
   uv sync

   # Copy environment file
   cp .env.example .env

   # Run database migrations
   uv run alembic upgrade head

   # Seed the database
   uv run python -m app.seed

   # Start the server
   uv run python main.py

The API will be available at http://localhost:8000.

- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Docker Setup
------------

.. code-block:: bash

   # Build and run with Docker Compose
   docker compose up -d

   # Or pull from Docker Hub
   docker pull mrqadeer/philo-coffee-shop:latest
   docker run -p 8000:8000 mrqadeer/philo-coffee-shop:latest

Environment Variables
---------------------

Configure the application via ``.env`` file or environment variables:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Variable
     - Default
     - Description
   * - ``APP_NAME``
     - Philo Coffee Shop
     - Application display name
   * - ``DATABASE_URL``
     - sqlite:///./data/philo_coffee.db
     - SQLite connection string
   * - ``TAX_RATE``
     - 0.08
     - Tax rate applied to orders (8%)
   * - ``LOG_LEVEL``
     - INFO
     - Logging level (DEBUG, INFO, WARNING, ERROR)
   * - ``CORS_ORIGINS``
     - ["http://localhost:3000"]
     - JSON list of allowed CORS origins
   * - ``LOW_STOCK_THRESHOLD``
     - 10
     - Stock level that triggers inventory alerts
