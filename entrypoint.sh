#!/bin/bash
# entrypoint.sh

# バックグラウンドでPythonのWebSocketサーバーを起動
python /var/www/html/websocket_server.py &

# Apacheをフォアグラウンドで起動
apache2-foreground