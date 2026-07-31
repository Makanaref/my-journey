#!/bin/bash

PYTHON="/c/Users/Donk/AppData/Local/Programs/Python/Python314/python.exe"
PID=""

start_server() {
  $PYTHON -u app.py &
  PID=$!
  echo "Server started (PID: $PID)"
}

restart_server() {
  echo "Restarting..."
  kill $PID
  wait $PID 2>/dev/null
  start_server
}

touch .last_reload
start_server

while true; do
  sleep 5

  # check github (only act if fetch succeeds)
  if git fetch origin main --quiet 2>/dev/null; then
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main)
    if [ "$LOCAL" != "$REMOTE" ]; then
      echo "New update found on github..."
      git pull --quiet
      restart_server
      continue
    fi
  fi

  # check manual signal
  if [ ".reload" -nt ".last_reload" ] 2>/dev/null; then
    echo "Manual file change detected..."
    touch .last_reload
    restart_server
  fi
done
