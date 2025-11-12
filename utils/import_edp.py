import pandas as pd
from empresas.models import Empresa
from proyectos.models import Proyecto, CuadroControl
from actividades.models import Actividad
from noc.models import NoConformidad
from users.models import User
from datetime import datetime

# Ruta al archivo
excel = pd.ExcelFile('Ejemplo EDP.xlsx')

# 1️⃣ Crear empresa y proyecto
caratula = excel.parse('CARATULA EP ').fillna('')
cliente_nombre = caratula.iloc[0].get('Cliente', 'Cliente genérico')
empresa, _ = Empresa.objects.get_or_create(nombre=cliente_nombre)

responsable = User.objects.filter(is_superuser=True).first()  # o el usuario que quieras asignar

proyecto = Proyecto.objects.create(
    codigo='EDP001',
    nombre=caratula.iloc[0].get('Nombre Proyecto', 'Proyecto sin nombre'),
    cliente=empresa,
    responsable=responsable,
    supervisor=caratula.iloc[0].get('Supervisor', ''),
    fecha_inicio=datetime.today(),
    estado='en_ejecucion'
)

# 2️⃣ Importar actividades desde "EDP 001"
df_actividades = excel.parse('EDP 001').fillna('')
for _, row in df_actividades.iterrows():
    # Parsear fechas
    fecha_programada = None
    fecha_real = None
    
    if 'Fecha Programada' in row and row.get('Fecha Programada'):
        try:
            fecha_programada = pd.to_datetime(row['Fecha Programada']).date()
        except:
            pass
    
    if 'Fecha Real' in row and row.get('Fecha Real'):
        try:
            fecha_real = pd.to_datetime(row['Fecha Real']).date()
        except:
            pass
    
    # Obtener avance
    avance = 0
    if '% Avance' in row:
        try:
            avance = float(row['% Avance'])
        except:
            avance = 0
    
    # Determinar estado
    estado = 'pendiente'
    if avance >= 100:
        estado = 'completada'
    elif avance > 0:
        estado = 'en_ejecucion'
    
    Actividad.objects.create(
        proyecto=proyecto,
        item=str(row.get('Item', '')),
        descripcion=row.get('Descripción', '') or row.get('Actividad', ''),
        responsable=responsable,
        fecha_programada=fecha_programada,
        fecha_real=fecha_real,
        avance=avance,
        observaciones=row.get('Observaciones', ''),
        estado=estado
    )

# 3️⃣ Generar cuadro de control
control, _ = CuadroControl.objects.get_or_create(proyecto=proyecto)
control.actualizar()

# 4️⃣ Importar No Conformidades (NOC-1)
try:
    df_noc = excel.parse('NOC-1').fillna('')
    for idx, row in df_noc.iterrows():
        # Parsear fechas
        fecha_detectada = datetime.today().date()
        if 'Fecha Detectada' in row and row.get('Fecha Detectada'):
            try:
                fecha_detectada = pd.to_datetime(row['Fecha Detectada']).date()
            except:
                pass
        
        fecha_cierre = None
        if 'Fecha Cierre' in row and row.get('Fecha Cierre'):
            try:
                fecha_cierre = pd.to_datetime(row['Fecha Cierre']).date()
            except:
                pass
        
        # Determinar estado
        estado = 'abierta'
        if fecha_cierre:
            estado = 'cerrada'
        elif row.get('Estado', '').lower() == 'en proceso':
            estado = 'en_proceso'
        
        NoConformidad.objects.create(
            proyecto=proyecto,
            codigo=row.get('Código', f"NOC-{idx+1}"),
            descripcion=row.get('Descripción', ''),
            causa=row.get('Causa', ''),
            accion_correctiva=row.get('Acción Correctiva', ''),
            responsable=responsable,
            fecha_detectada=fecha_detectada,
            fecha_cierre=fecha_cierre,
            estado=estado
        )
except Exception as e:
    print(f"No se cargaron NOC: {e}")

print(f"Proyecto {proyecto.codigo} importado con {proyecto.actividades.count()} actividades.")
