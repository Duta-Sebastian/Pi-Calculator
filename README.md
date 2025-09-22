# Pi Calculator API

A Flask-based REST API that calculates π using the Monte Carlo method with asynchronous processing.

## How it works

The API uses the Monte Carlo method to estimate π by simulating random dart throws at a unit square with an inscribed circle. The ratio of darts landing inside the circle approximates π/4.

## Quick Start

1. Clone the repository
2. Run with Docker Compose:

```bash
docker-compose up
```

This will start:
- **Web API** on http://localhost:5000
- **Swagger documentation** at http://localhost:5000/swagger/
- **Flower monitoring** at http://localhost:5555
- **Redis** for task queue management

## API Usage

### Start calculation
```
GET /pi/calculate?n=5
```
Returns a `task_id` for tracking progress.

### Check progress
```
GET /pi/progress?task_id=your-task-id
```
Returns current state and progress. When `state` is "FINISHED", the `result` field contains your π value.

## Parameters

- `n`: Number of decimal places (1-200)
- Higher values take longer but provide more accuracy

## Architecture

- **Flask** with Flask-RESTX for API and documentation
- **Celery** for asynchronous task processing
- **Redis** as message broker and result backend
- **Gunicorn** as WSGI server
- **Docker Compose** for easy deployment

## Health Check

```
GET /health/health
```

## Development

The application uses Python 3.13 and uv for dependency management. All services run in Docker containers with proper health checks and restart policies.