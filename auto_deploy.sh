#!/bin/bash

PYTHON="/c/Users/Donk/AppData/Local/Programs/Python/Python314/python.exe"
IPFS="/c/Users/Donk/kubo/ipfs"
PID=""
IPFS_PID=""

start_ipfs() {
  if ! curl -s -o /dev/null -X POST http://127.0.0.1:5001/api/v0/version; then
    "$IPFS" daemon &
    IPFS_PID=$!
    echo "IPFS daemon started (PID: $IPFS_PID)"
    sleep 3
  else
    echo "IPFS daemon already running"
  fi
}

start_server() {
  $PYTHON -u app.py &
  PID=$!
  echo "Server started (PID: $PID)"
}

restart_server() {
  echo "Restarting..."
  if [ -n "$PID" ]; then
    taskkill //F //T //PID "$PID" 2>/dev/null
  fi
  for p in $(tasklist //FI "IMAGENAME eq python.exe" //FO CSV //NH 2>/dev/null | tr -d '"' | cut -d, -f2); do
    if [ "$p" != "$PID" ]; then
      port_owner=$(netstat -ano 2>/dev/null | grep ":8080" | grep "LISTENING" | awk '{print $5}' | grep -x "$p")
      if [ -n "$port_owner" ]; then
        echo "Killing leftover python.exe on port 8080 (PID $p)"
        taskkill //F //T //PID "$p" 2>/dev/null
      fi
    fi
  done
  start_server
}

touch .last_reload
start_ipfs
start_server

while true; do
  sleep 5

  if [ -n "$IPFS_PID" ] && ! kill -0 $IPFS_PID 2>/dev/null; then
    echo "IPFS daemon died, restarting it..."
    start_ipfs
  fi

  if git fetch origin main --quiet 2>/dev/null; then
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main)
    BASE=$(git merge-base HEAD origin/main)

    if [ "$LOCAL" = "$REMOTE" ]; then
      :
    elif [ "$LOCAL" = "$BASE" ]; then
      echo "New update found on github, pulling..."
      if git pull --quiet 2>/dev/null; then
        echo "Pull succeeded, restarting..."
        restart_server
      else
        echo "Pull failed (network issue), will retry next cycle."
      fi
      continue
    fi
  fi

  if [ ".reload" -nt ".last_reload" ] 2>/dev/null; then
    echo "Manual file change detected..."
    touch .last_reload
    restart_server
  fi
done
