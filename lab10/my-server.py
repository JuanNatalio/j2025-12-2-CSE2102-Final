from flask import Flask, request, jsonify
import jwt
import datetime
import uuid

app = Flask(__name__)
SECRET_KEY = "secret"

@app.route("/")
def hello():
    return "JWT Token Service\n"

@app.route("/token", methods=['GET'])
def get_token():
    payload = {
        "jti": str(uuid.uuid4()),
        "user_id": 1,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

@app.route("/verify", methods=['POST'])
def verify_token():
    token = request.form.get('token')
    
    if not token:
        return jsonify({"error": "Missing token"}), 400
    
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"status": "valid", "payload": decoded}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@app.route("/protected", methods=['POST'])
def protected_resource():
    token = request.form.get('token')
    
    if not token:
        return jsonify({"error": "Missing token"}), 401
    
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({
            "message": "Access granted to protected resource",
            "user_id": decoded.get("user_id")
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
