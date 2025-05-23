#!/bin/bash

# Navigate to the project directory
cd /home/pi/work/stock_trading_bot

# Check if Flask app is already running on port 5000
PID=$(pgrep -f "python src/web/app.py")

if [ -n "$PID" ]; then
  echo "Flask app is already running with PID(s): $PID. Killing process(es)..."
  kill $PID
  # Give a moment for the process to terminate
  sleep 2
  echo "Process(es) killed."
else
  echo "No running Flask app found on port 5000."
fi

# Activate the virtual environment and start the Flask app in the background
echo "Starting Flask app..."
source venv/bin/activate && python src/web/app.py &
disown

echo "Flask app started in the background." 