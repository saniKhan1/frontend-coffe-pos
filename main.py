"""Entry-point script for running the Philo Coffee Shop POS API."""

import uvicorn


def main():
    """Start the Uvicorn server."""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
