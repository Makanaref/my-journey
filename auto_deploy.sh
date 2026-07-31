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

  if git fetch origin main --quiet 2>/dev/null; then
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main)
    BASE=$(git merge-base HEAD origin/main)

    if [ "$LOCAL" = "$REMOTE" ]; then
      : # up to date, nothing to do
    elif [ "$LOCAL" = "$BASE" ]; then
      # remote is ahead of local -> safe to pull
      echo "New update found on github, pulling..."
      if git pull --quiet 2>/dev/null; then
        echo "Pull succeeded, restarting..."
        restart_server
      else
        echo "Pull failed (network issue), will retry next cycle."
      fi
      continue
    fi
    # else: local is ahead of remote (unpushed commits) -> do nothing, just wait for manual push
  fi

  if [ ".reload" -nt ".last_reload" ] 2>/dev/null; then
    echo "Manual file change detected..."
    touch .last_reload
    restart_server
  fi
done
