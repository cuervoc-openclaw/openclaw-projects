#!/bin/bash
# Auto-sync del workspace — se ejecuta vía cron
cd "$(dirname "$0")"
bash sync.sh 2>/dev/null
