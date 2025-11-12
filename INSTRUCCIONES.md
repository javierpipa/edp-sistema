# Instrucciones Finales de Configuración

## Sistema EDP completamente implementado ✓

Se ha creado el sistema completo con:
- ✓ Custom User Model
- ✓ Apps modulares (users, empresas, proyectos, actividades, noc, dashboard)
- ✓ Modelos de negocio completos
- ✓ Admin configurado
- ✓ API REST con DRF
- ✓ Dashboard con gráficos
- ✓ Templates con Bootstrap
- ✓ Configuración con variables de entorno

## Pasos para finalizar la configuración

### 1. Crear la base de datos

```bash
mysql -u root -pdbrootdevel -e "CREATE DATABASE IF NOT EXISTS edp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 2. Activar el entorno virtual

```bash
source venv/bin/activate
```

### 3. Crear y aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crear superusuario

```bash
python manage.py createsuperuser
```

### 5. Iniciar el servidor

```bash
python manage.py runserver
```

## Accesos al sistema

Una vez iniciado el servidor:

- **Dashboard**: http://localhost:8000/dashboard/
- **Admin**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/

## Endpoints de la API

### Empresas
- `GET /api/empresas/` - Listar todas las empresas
- `POST /api/empresas/` - Crear nueva empresa
- `GET /api/empresas/{id}/` - Ver detalle de empresa
- `PUT /api/empresas/{id}/` - Actualizar empresa
- `DELETE /api/empresas/{id}/` - Eliminar empresa

### Proyectos
- `GET /api/proyectos/` - Listar todos los proyectos
- `POST /api/proyectos/` - Crear nuevo proyecto
- `GET /api/proyectos/{id}/` - Ver detalle de proyecto
- `PUT /api/proyectos/{id}/` - Actualizar proyecto
- `DELETE /api/proyectos/{id}/` - Eliminar proyecto

### Actividades
- `GET /api/actividades/` - Listar todas las actividades
- `POST /api/actividades/` - Crear nueva actividad
- `GET /api/actividades/{id}/` - Ver detalle de actividad
- `PUT /api/actividades/{id}/` - Actualizar actividad
- `DELETE /api/actividades/{id}/` - Eliminar actividad

### Cuadros de Control
- `GET /api/controles/` - Listar todos los cuadros de control
- `POST /api/controles/` - Crear nuevo cuadro de control
- `GET /api/controles/{id}/` - Ver detalle de cuadro de control
- `PUT /api/controles/{id}/` - Actualizar cuadro de control
- `DELETE /api/controles/{id}/` - Eliminar cuadro de control

### No Conformidades
- `GET /api/noc/` - Listar todas las no conformidades
- `POST /api/noc/` - Crear nueva no conformidad
- `GET /api/noc/{id}/` - Ver detalle de no conformidad
- `PUT /api/noc/{id}/` - Actualizar no conformidad
- `DELETE /api/noc/{id}/` - Eliminar no conformidad

## Estructura de Datos

### Empresa
```json
{
  "nombre": "Empresa Ejemplo",
  "rut": "12345678-9",
  "contacto": "Juan Pérez",
  "correo": "contacto@empresa.com"
}
```

### Proyecto
```json
{
  "codigo": "PROJ-001",
  "nombre": "Proyecto Ejemplo",
  "cliente": 1,
  "responsable": 1,
  "supervisor": "María González",
  "fecha_inicio": "2024-01-01",
  "fecha_termino": "2024-12-31",
  "estado": "en_ejecucion"
}
```

### Actividad
```json
{
  "proyecto": 1,
  "item": "ACT-001",
  "descripcion": "Descripción de la actividad",
  "responsable": 1,
  "fecha_programada": "2024-06-01",
  "fecha_real": null,
  "avance": 50.00,
  "observaciones": "Observaciones opcionales",
  "estado": "en_ejecucion"
}
```

### No Conformidad
```json
{
  "proyecto": 1,
  "codigo": "NOC-001",
  "descripcion": "Descripción de la no conformidad",
  "causa": "Causa identificada",
  "accion_correctiva": "Acción correctiva propuesta",
  "responsable": 1,
  "fecha_detectada": "2024-06-15",
  "fecha_cierre": null,
  "estado": "abierta"
}
```

## Comandos útiles

### Crear datos de prueba (opcional)
```bash
python manage.py shell
```

```python
from users.models import User
from empresas.models import Empresa
from proyectos.models import Proyecto, CuadroControl

# Crear empresa de prueba
empresa = Empresa.objects.create(
    nombre="Empresa Test",
    rut="12345678-9",
    contacto="Juan Pérez",
    correo="test@empresa.com"
)

# Crear proyecto de prueba
user = User.objects.first()
proyecto = Proyecto.objects.create(
    codigo="TEST-001",
    nombre="Proyecto de Prueba",
    cliente=empresa,
    responsable=user,
    fecha_inicio="2024-01-01",
    estado="en_ejecucion"
)

# Crear cuadro de control
control = CuadroControl.objects.create(proyecto=proyecto)
```

### Recolectar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

### Crear backup de la base de datos
```bash
mysqldump -u root -pdbrootdevel edp_db > backup_edp.sql
```

### Restaurar backup
```bash
mysql -u root -pdbrootdevel edp_db < backup_edp.sql
```

## Notas importantes

1. **Seguridad**: En producción, cambia el `SECRET_KEY` y establece `DEBUG=False`
2. **Base de datos**: El sistema está configurado para usar MariaDB local
3. **Custom User**: Se implementó un modelo de usuario personalizado desde el inicio
4. **Variables de entorno**: Todas las configuraciones sensibles están en `.env`
5. **Modularidad**: Cada funcionalidad está en su propia app independiente

## Próximos pasos sugeridos

1. Agregar autenticación JWT para la API
2. Implementar permisos granulares por rol
3. Agregar exportación a Excel/PDF de reportes
4. Implementar notificaciones por email
5. Agregar tests unitarios y de integración
6. Configurar CI/CD
7. Dockerizar la aplicación

## Soporte

Para cualquier problema, revisar:
- Logs de Django en la consola
- Configuración en `.env`
- Estado de la base de datos MariaDB
- Permisos de archivos y directorios
