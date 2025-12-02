# j2025-12-2-CSE2102-Final

A simple Flask web service that validates security tokens (UUIDs).

## Setup

Install dependencies:
```bash
pip install flask httpx
```

## Running the Server

Start the Flask server:
```bash
python my-server.py
```

The server runs on `http://localhost:5000`

## Testing

### Run Unit Tests
```bash
python test_server.py
```

### Run Functional Tests
First start the server, then in another terminal:
```bash
python test_functional.py
```

### Run Manual Tests
```bash
python my-calls.py
```

### Test with curl

Valid token (should return 200):
```bash
curl -d "uuid=4e136eb7-cfa9-11f0-8eb1-000d3a4fd085" -X POST http://localhost:5000/uuid
```

Invalid token (should return 401):
```bash
curl -d "uuid=wrong-token" -X POST http://localhost:5000/uuid
```