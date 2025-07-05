#!/bin/bash
# Esperar a que dependencias estén listas, si las hay

exec python manage.py migrate
echo "Iniciando supervisord..."
exec supervisord -n