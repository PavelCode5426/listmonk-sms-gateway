#!/bin/bash
# Esperar a que dependencias estén listas, si las hay

python manage.py migrate
echo "Migración completada. Iniciando supervisord..."
exec supervisord -n
