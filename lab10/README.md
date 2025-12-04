# Lab 10 - JWT Token Service

A simple Flask service that generates and verifies JWT (JSON Web Tokens).

## Setup

Create and activate virtual environment:
```bash
python -m venv .
source bin/activate
```

Install dependencies:
```bash
bin/pip install Flask PyJWT httpx
```

## Running the Server

Start the Flask server:
```bash
bin/python my-server.py
```

The server runs on `http://localhost:5000`

## Testing

### Run Unit Tests
```bash
bin/python test_server.py
```

### Run Functional Tests
First start the server, then in another terminal:
```bash
bin/python test_functional.py
```

### Run the Demo Client
```bash
bin/python my-calls.py
```

## Manual Testing with curl

Get a token:
```bash
curl http://localhost:5000/token
```

Verify a token:
```bash
curl -d "token=YOUR_TOKEN_HERE" -X POST http://localhost:5000/verify
```

Access protected resource:
```bash
curl -d "token=YOUR_TOKEN_HERE" -X POST http://localhost:5000/protected
```
