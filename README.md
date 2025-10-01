# Mars Rover Kata – Team 1

## Overview
This project implements the Mars Rover kata in Python, supporting both command-line and web-based demos.

## Requirements
- Python 3.10+
- (For web demo) Flask (`pip install -r webdemo/requirements.txt`)

## CLI Usage
Run the CLI demo with:
```bash
python run_io.py
```
Paste your input (plateau size, rover positions, commands), then press Ctrl+D to run.

Or, use an input file:
```bash
python run_io.py < input.txt
```

## Web-Based Demo
To run the web visualization:
```bash
pip install -r webdemo/requirements.txt
python webdemo/app.py --host=0.0.0.0
```
Then open the provided URL (e.g., `http://localhost:5000` or your Codespace URL) in your browser.

Enter your Mars Rover input in the form and see the final rover positions visualized on a grid.

## Project Structure
- `marsrover/` – Core logic
- `run_io.py` – CLI entry point
- `webdemo/` – Flask app and frontend for web demo
- `adr/` – Architectural Decision Records

## Testing
Run tests with:
```bash
pytest
```
