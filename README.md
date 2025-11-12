# 🚀 EDP - Sistema de Ejecución de Proyectos

Sistema completo de gestión y seguimiento de proyectos desarrollado en Django con dashboard interactivo, API REST y gestión de actividades y no conformidades.

## Características

- **Gestión de Empresas**: Administración de clientes y empresas
- **Proyectos**: Control de proyectos con estados y seguimiento
- **Actividades**: Gestión de actividades por proyecto con avance
- **Cuadro de Control**: Seguimiento automático del avance global
- **No Conformidades (NOC)**: Registro y seguimiento de no conformidades
- **Dashboard**: Panel de control con métricas y gráficos
- **API REST**: API completa con Django REST Framework

## Estructura del Proyecto

```
edp/
├── edp_project/          # Configuración principal
├── users/                # App de usuarios (custom user model)
├── empresas/             # App de empresas/clientes
├── proyectos/            # App de proyectos y cuadros de control
├── actividades/          # App de actividades
├── noc/                  # App de no conformidades
├── dashboard/            # App del dashboard
├── templates/            # Templates globales
├── static/               # Archivos estáticos
├── media/                # Archivos de usuario
└── venv/                 # Entorno virtual
```

## Instalación

### 1. Clonar el repositorio y activar el entorno virtual

```bash
cd edp
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiar `.env.example` a `.env` y ajustar los valores:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales de base de datos.

### 4. Crear la base de datos en MariaDB

```bash
mysql -u root -p
CREATE DATABASE edp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

## Uso

### Acceso al sistema

- **Dashboard**: http://localhost:8000/dashboard/
- **Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

### Endpoints de la API

- `GET/POST /api/empresas/` - Listar/crear empresas
- `GET/POST /api/proyectos/` - Listar/crear proyectos
- `GET/POST /api/actividades/` - Listar/crear actividades
- `GET/POST /api/controles/` - Listar/crear cuadros de control
- `GET/POST /api/noc/` - Listar/crear no conformidades

## Tecnologías

- **Django 4.2+**: Framework web
- **Django REST Framework**: API REST
- **MariaDB/MySQL**: Base de datos
- **Bootstrap 5**: Frontend
- **Chart.js**: Gráficos
- **django-environ**: Gestión de variables de entorno

## Desarrollo

### Crear nuevas migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### Recolectar archivos estáticos

```bash
python manage.py collectstatic
```

### Ejecutar tests

```bash
python manage.py test
```

## Licencia

Proyecto privado - Todos los derechos reservados
