from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML + JavaScript Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>API Addition</title>
</head>
<body>
  <h1>Addition API Frontend</h1>
  
  <input type="number" id="num1" placeholder="Enter first number" />
  <input type="number" id="num2" placeholder="Enter second number" />
  <br><br>

  <button onclick="useGET()">Add with GET</button>
  <button onclick="usePOST()">Add with POST</button>

  <h2 id="result"></h2>

  <script>
    function useGET() {
      const num1 = document.getElementById("num1").value;
      const num2 = document.getElementById("num2").value;

      fetch(`/api/add?num1=${num1}&num2=${num2}`)
        .then(res => res.json())
        .then(data => {
          if (data.result !== undefined) {
            document.getElementById("result").innerText = "Result (GET): " + data.result;
          } else {
            document.getElementById("result").innerText = "Error: " + data.error;
          }
        })
        .catch(err => console.error(err));
    }

    function usePOST() {
      const num1 = document.getElementById("num1").value;
      const num2 = document.getElementById("num2").value;

      fetch("/api/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ num1: num1, num2: num2 })
      })
        .then(res => res.json())
        .then(data => {
          if (data.result !== undefined) {
            document.getElementById("result").innerText = "Result (POST): " + data.result;
          } else {
            document.getElementById("result").innerText = "Error: " + data.error;
          }
        })
        .catch(err => console.error(err));
    }
  </script>
</body>
</html>
"""

# Home route (renders the frontend)
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

# Unified route handling both GET and POST
@app.route("/api/add", methods=["GET", "POST"])
def add():
    try:
        if request.method == "GET":
            num1 = int(request.args.get("num1"))
            num2 = int(request.args.get("num2"))
        else:
            data = request.get_json()
            num1 = int(data.get("num1"))
            num2 = int(data.get("num2"))

        return jsonify({"result": num1 + num2})
    except (TypeError, ValueError, KeyError):
        return jsonify({"error": "Invalid or missing input"}), 400

if __name__ == "__main__":
    app.run(debug=True)
