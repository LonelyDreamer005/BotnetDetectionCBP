from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Route to serve the main dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve images from results if needed directly
@app.route('/results/<path:filename>')
def custom_static(filename):
    return send_from_directory('results', filename)

if __name__ == '__main__':
    # Using host 0.0.0.0 for visibility and port 5000 as default
    app.run(debug=True, host='0.0.0.0', port=5000)
