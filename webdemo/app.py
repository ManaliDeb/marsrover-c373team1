from flask import Flask, request, jsonify, render_template
import sys
sys.path.insert(0, '..')  # Ensure marsrover package is importable
from marsrover.controller import Mission

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/rover', methods=['POST'])
def rover_api():
    data = request.json
    input_lines = data.get('input', '').splitlines()
    mission = Mission()
    try:
        output = list(mission.run_io_lines(input_lines))
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
