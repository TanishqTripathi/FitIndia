from flask import Flask, render_template_string, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)

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
        .restart-button {
            position: absolute;
            top: 10px;
            left: 10px;
            font-size: 20px;
            cursor: pointer;
            background-color: #28a745;
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
        <a href="/restart">
            <button class="restart-button">Upload New Image</button>
        </a>
        <div class="footer">
            <p>Powered by FITINDIA</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def display_text():
    try:
        with open('nutr_data/output.txt', 'r') as f:
            text = f.read()
        return render_template_string(output_html, text=text)
    except FileNotFoundError:
        return "File not found.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/shutdown')
def shutdown():
    os._exit(0)
    return "Server shutting down..."

@app.route('/restart')
def restart():
    subprocess.Popen(["python", "run_servers.py"])
    return redirect("http://127.0.0.1:8081")

if __name__ == '__main__':
    app.run(debug=False, port=5000)