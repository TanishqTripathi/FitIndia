import os
import json
import time
import requests
import threading
import subprocess
from flask import Flask, request, jsonify, render_template_string
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

# Initialize AI Agent
agent = Agent(model=Groq(id="llama-3.3-70b-versatile"))

app = Flask(__name__)

# Ensure 'text' folder exists
if not os.path.exists("text"):
    os.makedirs("text")

# HTML Template for the main page
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Description App</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <style>
        body { padding: 20px; background-color: #f0f8ff; }
        #output { margin-top: 20px; }
        .spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border-left-color: #09f;
            animation: spin 1s ease infinite;
            margin: 0 auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin-top: 50px;
        }
        .btn-primary {
            background-color: #007bff;
            border-color: #007bff;
        }
        .btn-info {
            background-color: #17a2b8;
            border-color: #17a2b8;
        }
        .btn-primary:hover, .btn-info:hover {
            opacity: 0.8;
        }
        .text-center {
            color: #007bff;
        }
    </style>
    <script src="https://js.puter.com/v2/"></script>
</head>
<body>
    <div class="container">
        <h2 class="text-center">UPLOAD IMAGE OF FOOD</h2>
        <div class="text-center my-4">
            <input type="file" id="imageUpload" accept="image/*" class="form-control-file">
        </div>
        <div class="text-center">
            <button id="submit" class="btn btn-primary" disabled>Describe Photo</button>
        </div>
        <div id="output" class="mt-3"></div>
        <div id="loadingText" class="text-center mt-3" style="display: none;">Loading nutritions info...</div>
        <div class="text-center mt-3">
            <a id="viewOutput" href="http://127.0.0.1:5000/" class="btn btn-info" style="display: none;">View Food Nutrition</a>
        </div>
    </div>

    <script>
        const imageUpload = document.getElementById('imageUpload');
        const submitButton = document.getElementById('submit');
        const outputDiv = document.getElementById('output');
        const loadingText = document.getElementById('loadingText');
        const viewOutputButton = document.getElementById('viewOutput');

        function showSpinner() {
            const spinner = document.createElement('div');
            spinner.classList.add('spinner');
            outputDiv.innerHTML = '';
            outputDiv.appendChild(spinner);
        }

        function hideSpinner() { outputDiv.innerHTML = ''; }

        imageUpload.addEventListener('change', function () {
            submitButton.disabled = !this.files.length;
        });

        submitButton.onclick = function () {
            if (imageUpload.files.length === 0) return;
            showSpinner();
            const file = imageUpload.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function () {
                const imageData = reader.result;
                submitButton.disabled = true;
                puter.ai.chat("Describe this image", imageData)
                    .then(response => {
                        hideSpinner();
                        submitButton.disabled = false;
                        let description = response.message.content;  // Extract only "content"
                        outputDiv.innerText = 'Image Description: ' + description;

                        // Send to Flask for saving
                        fetch('/save_description', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ description: description })
                        }).then(res => res.json()).then(data => {
                            console.log(data);
                            // Show loading text and enable view output button after 7 seconds
                            loadingText.style.display = 'block';
                            setTimeout(() => {
                                loadingText.style.display = 'none';
                                viewOutputButton.style.display = 'block';
                            }, 7000);
                        }).catch(error => console.error('Error:', error));
                    })
                    .catch(error => {
                        hideSpinner();
                        submitButton.disabled = false;
                        console.error('Error:', error);
                        outputDiv.innerText = 'Error in getting description';
                    });
            };
        };
    </script>
</body>
</html>
"""

# HTML Template for displaying the content of output.txt
output_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Text from File</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f8ff;
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 100%;
            position: relative;
        }
        .close-button {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 20px;
            cursor: pointer;
            background-color: #dc3545;
            color: white;
            padding: 5px 10px;
            border: none;
            border-radius: 5px;
        }
        .content {
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }
        h1 {
            color: #007bff;
            margin-bottom: 20px;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Food Nutrition</h1>
        <pre class="content">{{ text }}</pre>
        <a href="/shutdown">
            <button class="close-button">X</button>
        </a>
        <div class="footer">
            <p>Powered by FitIndia</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the HTML page."""
    return render_template_string(html_code)

@app.route('/save_description', methods=['POST'])
def save_description():
    """Save AI-generated description to a file"""
    try:
        data = request.get_json()
        received_description = data.get("description", "")

        if not received_description:
            return jsonify({"error": "No description provided"}), 400

        # Save with a unique filename
        file_count = len(os.listdir("text")) + 1
        filename = f"text/description_{file_count}.txt"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(received_description)

        return jsonify({"message": "Description saved", "file": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_latest_description', methods=['GET'])
def get_latest_description():
    """Fetch latest saved description"""
    try:
        files = sorted(os.listdir("text"), reverse=True)
        if not files:
            return jsonify({"description": "No description available."})

        latest_file = os.path.join("text", files[0])
        with open(latest_file, "r", encoding="utf-8") as file:
            return jsonify({"description": file.read().strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run_server', methods=['GET'])
def run_server():
    """Run the server.py script"""
    try:
        print("Running server.py on port 5000...")  # Add logging
        subprocess.Popen(["python", "server.py"])
        return jsonify({"message": "Server is running on port 5000"}), 200
    except Exception as e:
        print(f"Error running server.py: {e}")  # Add logging
        return jsonify({"error": str(e)}), 500

@app.route('/get_server_output', methods=['GET'])
def get_server_output():
    """Fetch the output from server.py"""
    try:
        with open("nutr_data/output.txt", "r", encoding="utf-8") as file:
            output = file.read().strip()
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/output')
def display_output():
    """Display the content of output.txt"""
    try:
        with open("nutr_data/output.txt", "r", encoding="utf-8") as file:
            text = file.read().strip()
        return render_template_string(output_html, text=text)
    except Exception as e:
        return f"Error: {e}"

@app.route('/shutdown')
def shutdown():
    """Shutdown the Flask server"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

# Function to start Flask Server in a separate thread
def start_server():
    app.run(debug=False, port=8081, use_reloader=False)

# Function for Server 2 to start *only after a new file is created*
def wait_for_new_file():
    print("\n⏳ Waiting for Server 1 to generate a text file...")

    existing_files = set(os.listdir("text"))  # Initial state

    while True:
        time.sleep(2)  # Check every 2 seconds
        current_files = set(os.listdir("text"))
        new_files_detected = current_files - existing_files  # Detect new file

        if new_files_detected:
            print("✅ New description file detected! Starting Server 2...")
            break

    # Now call process_description()
    process_description()

# Function for Server 2 to fetch and process the description
def process_description():
    api_response = requests.get("http://localhost:8081/get_latest_description")
    if api_response.status_code == 200:
        latest_saved_prompt = api_response.json().get("description", "No description available.")
    else:
        latest_saved_prompt = "Error fetching description"

    print("\n📝 Latest Description:", latest_saved_prompt)

    if latest_saved_prompt and "Error" not in latest_saved_prompt:
        formatted_prompt = (
            f"Find the food name and quantity, and give calories, carbs, protein, and fat. "
            f"Don't use approximately or any other words, just give only the nutrition details simply:\n"
            f"{latest_saved_prompt}"
        )
        response_obj = agent.run(formatted_prompt)

        # Output response
        nutrition_data = response_obj.content.strip()
        print(nutrition_data)

        # Ensure 'nutr_data' folder exists
        os.makedirs("nutr_data", exist_ok=True)

        # Remove any existing files in 'nutr_data' folder
        for file in os.listdir("nutr_data"):
            file_path = os.path.join("nutr_data", file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Save output to a new file
        filename = "nutr_data/output.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(nutrition_data)

        # Run server.py after saving the output file
        print("Running server.py on port 5000...")
        subprocess.Popen(["python", "server.py"])

# Start Flask Server (Server 1) in a separate thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Start waiting for new file (Server 2 logic)
wait_for_new_file()