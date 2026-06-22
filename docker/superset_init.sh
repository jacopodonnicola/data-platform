#!/bin/bash
set -e

# inizializza solo se è il primo avvio
if [ ! -f /app/superset_home/.initialized ]; then
    echo "Prima inizializzazione di Superset..."
    superset db upgrade
    superset fab create-admin \
        --username supersetadmin \
        --firstname supersetadmin \
        --lastname supersetadmin \
        --email supersetadmin@superset.com \
        --password supersetadmin
    superset init
    touch /app/superset_home/.initialized
    echo "Inizializzazione completata."
else
    echo "Superset già inizializzato, skip setup."
fi

# avvia Superset
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger
