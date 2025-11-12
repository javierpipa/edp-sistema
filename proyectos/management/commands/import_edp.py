import pandas as pd
from django.core.management.base import BaseCommand
from empresas.models import Empresa
from proyectos.models import Proyecto, CuadroControl
from actividades.models import Actividad
from noc.models import NoConformidad
from users.models import User
from datetime import datetime
from django.utils.dateparse import parse_date


class Command(BaseCommand):
    help = 'Importa datos desde un archivo Excel EDP'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Ruta al archivo Excel')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        
        try:
            excel = pd.ExcelFile(excel_file)
            self.stdout.write(self.style.SUCCESS(f'Archivo {excel_file} cargado correctamente'))
            
            # 1️⃣ Crear empresa y proyecto
            caratula = excel.parse('CARATULA EP ').fillna('')
            cliente_nombre = caratula.iloc[0].get('Cliente', 'Cliente genérico')
            empresa, created = Empresa.objects.get_or_create(nombre=cliente_nombre)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Empresa creada: {empresa.nombre}'))
            else:
                self.stdout.write(f'Empresa existente: {empresa.nombre}')
            
            # Obtener responsable
            responsable = User.objects.filter(is_superuser=True).first()
            if not responsable:
                self.stdout.write(self.style.ERROR('No hay superusuarios. Crea uno primero.'))
                return
            
            # Crear proyecto
            codigo_proyecto = caratula.iloc[0].get('Código', 'EDP001')
            nombre_proyecto = caratula.iloc[0].get('Nombre Proyecto', 'Proyecto sin nombre')
            
            proyecto, created = Proyecto.objects.get_or_create(
                codigo=codigo_proyecto,
                defaults={
                    'nombre': nombre_proyecto,
                    'cliente': empresa,
                    'responsable': responsable,
                    'supervisor': caratula.iloc[0].get('Supervisor', ''),
                    'fecha_inicio': datetime.today(),
                    'estado': 'en_ejecucion'
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Proyecto creado: {proyecto.codigo}'))
            else:
                self.stdout.write(self.style.WARNING(f'Proyecto ya existe: {proyecto.codigo}'))
            
            # 2️⃣ Importar actividades desde "EDP 001"
            try:
                df_actividades = excel.parse('EDP 001').fillna('')
                actividades_creadas = 0
                
                for idx, row in df_actividades.iterrows():
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
                    actividades_creadas += 1
                
                self.stdout.write(self.style.SUCCESS(f'{actividades_creadas} actividades importadas'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al importar actividades: {e}'))
            
            # 3️⃣ Generar cuadro de control
            control, created = CuadroControl.objects.get_or_create(proyecto=proyecto)
            control.actualizar()
            self.stdout.write(self.style.SUCCESS(f'Cuadro de control actualizado: {control.avance_global}%'))
            
            # 4️⃣ Importar No Conformidades (NOC-1)
            try:
                df_noc = excel.parse('NOC-1').fillna('')
                noc_creadas = 0
                
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
                    noc_creadas += 1
                
                self.stdout.write(self.style.SUCCESS(f'{noc_creadas} No Conformidades importadas'))
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'No se cargaron NOC: {e}'))
            
            # Resumen final
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write(self.style.SUCCESS(f'Proyecto {proyecto.codigo} importado exitosamente'))
            self.stdout.write(self.style.SUCCESS(f'Total actividades: {proyecto.actividades.count()}'))
            self.stdout.write(self.style.SUCCESS(f'Total NOC: {proyecto.noc.count()}'))
            self.stdout.write(self.style.SUCCESS(f'Avance global: {control.avance_global}%'))
            self.stdout.write(self.style.SUCCESS('='*50))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Archivo no encontrado: {excel_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error general: {e}'))
            import traceback
            traceback.print_exc()
