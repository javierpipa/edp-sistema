#!/bin/bash

# Script de configuración inicial del proyecto EDP

echo "=========================================="
echo "Configuración inicial del proyecto EDP"
echo "=========================================="

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Crear base de datos
echo ""
echo "Creando base de datos en MariaDB..."
mysql -u root -pdbrootdevel -e "CREATE DATABASE IF NOT EXISTS edp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if [ $? -eq 0 ]; then
    echo "✓ Base de datos creada exitosamente"
else
    echo "✗ Error al crear la base de datos"
    exit 1
fi

# Crear migraciones
echo ""
echo "Creando migraciones..."
python manage.py makemigrations

# Aplicar migraciones
echo ""
echo "Aplicando migraciones..."
python manage.py migrate

if [ $? -eq 0 ]; then
    echo "✓ Migraciones aplicadas exitosamente"
else
    echo "✗ Error al aplicar migraciones"
    exit 1
fi

# Crear superusuario
echo ""
echo "=========================================="
echo "Crear superusuario"
echo "=========================================="
python manage.py createsuperuser

echo ""
echo "=========================================="
echo "Configuración completada!"
echo "=========================================="
echo ""
echo "Para iniciar el servidor ejecuta:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Accesos:"
echo "  - Dashboard: http://localhost:8000/dashboard/"
echo "  - Admin: http://localhost:8000/admin/"
echo "  - API: http://localhost:8000/api/"
echo ""
