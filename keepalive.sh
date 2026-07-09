#!/data/data/com.termux/files/usr/bin/bash
# Keepalive monitor for portfolio web service
# - Checks local gunicorn every 30s
# - Pings Render every 10min to prevent cold starts

cd /data/data/com.termux/files/home

RENDER_URL="https://creativestudio-5vs3.onrender.com/"
count=0

while true; do
  # Local health check
  curl -s -o /dev/null http://localhost:8080/ --connect-timeout 10 --max-time 15 2>/dev/null
  if [ $? -ne 0 ]; then
    logger -t keepalive "Portfolio DOWN at $(date), attempting restart..."
    sv restart portfolio 2>/dev/null || {
      cd /data/data/com.termux/files/home/portfolio && gunicorn --worker-class gthread --threads 4 --bind 0.0.0.0:8080 --workers 2 --timeout 120 app:app &
    }
  fi

  # Ping Render every 10 minutes (20 iterations * 30s)
  count=$(( (count + 1) % 20 ))
  if [ $count -eq 0 ]; then
    curl -s -o /dev/null "$RENDER_URL" --connect-timeout 15 --max-time 20 2>/dev/null
  fi

  sleep 30
done
