from flask import Flask, request

app = Flask(__name__)

uuid = "4e136eb7-cfa9-11f0-8eb1-000d3a4fd085"

@app.route("/")
def hello():
   return " you called \n"

# curl -d "text=Hello!&param2=value2" -X POST http://localhost:5000/echo
@app.route("/echo", methods=['POST'])
def echo():
   return "You said: " + request.form['text']


# curl -d "uuid=xxx" -X POST http://localhost:5000/uuid
@app.route("/uuid", methods=['POST'])
def idCheck():
   if 'uuid' not in request.form:
      return "Missing UUID parameter", 400
   myUUId = str(request.form['uuid'])
   if (myUUId == uuid):
      print("Yes!")
      return "Token validated successfully!"
   else:
      print("Failed Identifier")
      return "Token validation failed", 401

if __name__ == "__main__":
   app.run(host='0.0.0.0')