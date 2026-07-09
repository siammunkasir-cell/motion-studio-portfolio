#!/data/data/com.termux/files/usr/bin/bash
# Keepalive monitor for portfolio web service
# Runs in background independently of runit

cd /data/data/com.termux/files/home

while true; do
  curl -s -o /dev/null http://localhost:8080/ --connect-timeout 10 --max-time 15 2>/dev/null
  if [ $? -ne 0 ]; then
    logger -t keepalive "Portfolio DOWN at $(date), attempting restart..."
    sv restart portfolio 2>/dev/null || {
      cd /data/data/com.termux/files/home/portfolio && gunicorn --worker-class gthread --threads 4 --bind 0.0.0.0:8080 --workers 2 --timeout 120 app:app &
    }
  fi
  sleep 30
done
